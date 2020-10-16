import argparse
import os
import time

import _pybgpstream
import redis
from kombu import Connection
from kombu import Consumer
from kombu import Exchange
from kombu import Producer
from kombu import Queue
from kombu import uuid
from netaddr import IPAddress
from netaddr import IPNetwork
from utils import get_logger
from utils import key_generator
from utils import load_json
from utils import mformat_validator
from utils import normalize_msg_path
from utils import ping_redis
from utils import RABBITMQ_URI
from utils import REDIS_HOST
from utils import REDIS_PORT

# install as described in https://bgpstream.caida.org/docs/install/pybgpstream

START_TIME_OFFSET = 3600  # seconds
log = get_logger()
redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
DEFAULT_MON_TIMEOUT_LAST_BGP_UPDATE = 60 * 60


class BGPStreamKafka:
    def __init__(
        self,
        prefixes_file=None,
        kafka_host=None,
        kafka_port=None,
        kafka_topic="openbmp.bmp_raw",
        start=0,
        end=0,
        autoconf=False,
    ):
        self.prefixes = load_json(prefixes_file)
        assert self.prefixes is not None
        self.kafka_host = kafka_host
        self.kafka_port = kafka_port
        self.kafka_topic = kafka_topic
        self.start = start
        self.end = end
        self.autoconf = autoconf
        self.autoconf_goahead = False

    def handle_autoconf_update_goahead_reply(self, message):
        message.ack()
        self.autoconf_goahead = True

    def run_bgpstream(self):
        """
        Retrieve all records related to a list of prefixes
        https://bgpstream.caida.org/docs/api/pybgpstream/_pybgpstream.html

        :param prefixes_file: <str> input prefix json
        :param kafka_host: <str> kafka host
        :param kafka_port: <int> kafka_port
        :param kafka_topic: <str> kafka topic
        :param start: <int> start timestamp in UNIX epochs
        :param end: <int> end timestamp in UNIX epochs (if 0 --> "live mode")

        :return: -
        """

        # add /0 if autoconf
        if self.autoconf:
            self.prefixes.append("0.0.0.0/0")
            self.prefixes.append("::/0")

        # create a new bgpstream instance and a reusable bgprecord instance
        stream = _pybgpstream.BGPStream()

        # set kafka data interface
        stream.set_data_interface("kafka")

        # set host connection details
        stream.set_data_interface_option(
            "kafka", "brokers", "{}:{}".format(self.kafka_host, self.kafka_port)
        )

        # set topic
        stream.set_data_interface_option("kafka", "topic", self.kafka_topic)

        # filter prefixes
        for prefix in self.prefixes:
            stream.add_filter("prefix", prefix)

        # filter record type
        stream.add_filter("record-type", "updates")

        # filter based on timing (if end=0 --> live mode)
        stream.add_interval_filter(self.start, self.end)

        # set live mode
        stream.set_live_mode()

        # start the stream
        stream.start()

        with Connection(RABBITMQ_URI) as connection:
            exchange = Exchange(
                "bgp-update", channel=connection, type="direct", durable=False
            )
            exchange.declare()
            producer = Producer(connection)
            validator = mformat_validator()
            while True:
                # get next record
                try:
                    rec = stream.get_next_record()
                except BaseException:
                    continue
                if (rec.status != "valid") or (rec.type != "update"):
                    continue

                # get next element
                try:
                    elem = rec.get_next_elem()
                except BaseException:
                    continue

                while elem:
                    if elem.type in {"A", "W"}:
                        redis.set(
                            "bgpstreamkafka_seen_bgp_update",
                            "1",
                            ex=int(
                                os.getenv(
                                    "MON_TIMEOUT_LAST_BGP_UPDATE",
                                    DEFAULT_MON_TIMEOUT_LAST_BGP_UPDATE,
                                )
                            ),
                        )
                        this_prefix = str(elem.fields["prefix"])
                        service = "bgpstreamkafka|{}".format(str(rec.collector))
                        type_ = elem.type
                        if type_ == "A":
                            as_path = elem.fields["as-path"].split(" ")
                            communities = [
                                {
                                    "asn": int(comm.split(":")[0]),
                                    "value": int(comm.split(":")[1]),
                                }
                                for comm in elem.fields["communities"]
                            ]
                        else:
                            as_path = []
                            communities = []
                        timestamp = float(rec.time)
                        if timestamp == 0:
                            timestamp = time.time()
                            log.debug("fixed timestamp: {}".format(timestamp))

                        peer_asn = elem.peer_asn

                        for prefix in self.prefixes:
                            base_ip, mask_length = this_prefix.split("/")
                            our_prefix = IPNetwork(prefix)
                            if (
                                IPAddress(base_ip) in our_prefix
                                and int(mask_length) >= our_prefix.prefixlen
                            ):
                                msg = {
                                    "type": type_,
                                    "timestamp": timestamp,
                                    "path": as_path,
                                    "service": service,
                                    "communities": communities,
                                    "prefix": this_prefix,
                                    "peer_asn": peer_asn,
                                }
                                try:
                                    if validator.validate(msg):
                                        msgs = normalize_msg_path(msg)
                                        for msg in msgs:
                                            key_generator(msg)
                                            log.debug(msg)
                                            if self.autoconf:
                                                if (
                                                    str(our_prefix)
                                                    in ["0.0.0.0/0", "::/0"]
                                                    and msg["type"] == "W"
                                                ):
                                                    # ignore irrelevant withdrawals
                                                    # not matching configured prefixes
                                                    break
                                                self.autoconf_goahead = False
                                                correlation_id = uuid()
                                                callback_queue = Queue(
                                                    uuid(),
                                                    durable=False,
                                                    auto_delete=True,
                                                    max_priority=4,
                                                    consumer_arguments={
                                                        "x-priority": 4
                                                    },
                                                )
                                                producer.publish(
                                                    msg,
                                                    exchange="",
                                                    routing_key="configuration.rpc.autoconf-update",
                                                    reply_to=callback_queue.name,
                                                    correlation_id=correlation_id,
                                                    retry=True,
                                                    declare=[
                                                        Queue(
                                                            "configuration.rpc.autoconf-update",
                                                            durable=False,
                                                            max_priority=4,
                                                            consumer_arguments={
                                                                "x-priority": 4
                                                            },
                                                        ),
                                                        callback_queue,
                                                    ],
                                                    priority=4,
                                                    serializer="ujson",
                                                )
                                                with Consumer(
                                                    connection,
                                                    on_message=self.handle_autoconf_update_goahead_reply,
                                                    queues=[callback_queue],
                                                    accept=["ujson"],
                                                ):
                                                    while not self.autoconf_goahead:
                                                        connection.drain_events()
                                            producer.publish(
                                                msg,
                                                exchange=exchange,
                                                routing_key="update",
                                                serializer="ujson",
                                            )
                                    else:
                                        log.warning(
                                            "Invalid format message: {}".format(msg)
                                        )
                                except BaseException:
                                    log.exception(
                                        "Error when normalizing BGP message: {}".format(
                                            msg
                                        )
                                    )
                                break
                    try:
                        elem = rec.get_next_elem()
                    except BaseException:
                        continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BGPStream Kafka Monitor")
    parser.add_argument(
        "-p",
        "--prefixes",
        type=str,
        dest="prefixes_file",
        default=None,
        help="Prefix(es) to be monitored (json file with prefix list)",
    )
    parser.add_argument(
        "--kafka_host", type=str, dest="kafka_host", default=None, help="kafka host"
    )
    parser.add_argument(
        "--kafka_port", type=str, dest="kafka_port", default=None, help="kafka port"
    )
    parser.add_argument(
        "--kafka_topic",
        type=str,
        dest="kafka_topic",
        default="openbmp.bmp_raw",
        help="kafka topic",
    )
    parser.add_argument(
        "-a",
        "--autoconf",
        dest="autoconf",
        action="store_true",
        help="Use the feed from this kafka BMP route collector to build the configuration",
    )

    args = parser.parse_args()

    ping_redis(redis)

    start_time = int(time.time()) - START_TIME_OFFSET
    # Bypass for https://github.com/FORTH-ICS-INSPIRE/artemis/issues/411#issuecomment-661325802
    if "BGPSTREAM_TIMESTAMP_BYPASS" in os.environ:
        log.warn(
            "Using BGPSTREAM_TIMESTAMP_BYPASS, meaning BMP timestamps are thrown away from BGPStream"
        )
        start_time = 0

    try:
        bgpstreamkafka_instance = BGPStreamKafka(
            args.prefixes_file,
            args.kafka_host,
            int(args.kafka_port),
            args.kafka_topic,
            start_time,
            0,
            args.autoconf,
        )
        bgpstreamkafka_instance.run_bgpstream()
    except Exception:
        log.exception("exception")
    except KeyboardInterrupt:
        pass
