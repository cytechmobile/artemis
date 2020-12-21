# functions for update processing
from datetime import datetime
from datetime import timedelta
from ipaddress import ip_network as str2ip
from typing import List
from typing import Tuple

from envvars import HISTORIC


class MformatValidator:
    def __init__(self):
        self.msg = None
        self.mformat_fields = [
            "service",
            "type",
            "prefix",
            "path",
            "communities",
            "timestamp",
            "peer_asn",
        ]
        self.type_values = {"A", "W"}
        self.community_keys = {"asn", "value"}
        self.optional_fields_init = {"communities": []}

    def validate(self, msg):
        self.msg = msg
        if not self.valid_dict():
            return False

        self.add_optional_fields()

        for func in self.valid_generator():
            if not func():
                return False

        return True

    def valid_dict(self):
        if not isinstance(self.msg, dict):
            return False
        return True

    def add_optional_fields(self):
        for field in self.optional_fields_init:
            if field not in self.msg:
                self.msg[field] = self.optional_fields_init[field]

    def valid_fields(self):
        if any(field not in self.msg for field in self.mformat_fields):
            return False
        return True

    def valid_prefix(self):
        try:
            str2ip(self.msg["prefix"])
        except Exception:
            return False
        return True

    def valid_service(self):
        if not isinstance(self.msg["service"], str):
            return False
        return True

    def valid_type(self):
        if self.msg["type"] not in self.type_values:
            return False
        return True

    def valid_path(self):
        if self.msg["type"] == "A" and not isinstance(self.msg["path"], list):
            return False
        return True

    def valid_communities(self):
        if not isinstance(self.msg["communities"], list):
            return False
        for comm in self.msg["communities"]:
            if not isinstance(comm, dict):
                return False
            if self.community_keys - set(comm.keys()):
                return False
        return True

    def valid_timestamp(self):
        if not isinstance(self.msg["timestamp"], float):
            return False
        if HISTORIC == "false" and datetime.utcfromtimestamp(
            self.msg["timestamp"]
        ) < datetime.utcnow() - timedelta(hours=1, minutes=30):
            return False
        if datetime.utcfromtimestamp(self.msg["timestamp"]) > datetime.utcnow():
            return False
        return True

    def valid_peer_asn(self):
        if not isinstance(self.msg["peer_asn"], int):
            return False
        return True

    def valid_generator(self):
        yield self.valid_fields
        yield self.valid_prefix
        yield self.valid_service
        yield self.valid_type
        yield self.valid_path
        yield self.valid_communities
        yield self.valid_timestamp
        yield self.valid_peer_asn


def __remove_prepending(seq: List[int]) -> Tuple[List[int], bool]:
    """
    Method to remove prepending ASs from AS path.
    """
    last_add = None
    new_seq = []
    for x in seq:
        if last_add != x:
            last_add = x
            new_seq.append(x)

    is_loopy = False
    if len(set(seq)) != len(new_seq):
        is_loopy = True
    return new_seq, is_loopy


def __clean_loops(seq: List[int]) -> List[int]:
    """
    Method to remove loops from AS path.
    """
    # use inverse direction to clean loops in the path of the traffic
    seq_inv = seq[::-1]
    new_seq_inv = []
    for x in seq_inv:
        if x not in new_seq_inv:
            new_seq_inv.append(x)
        else:
            x_index = new_seq_inv.index(x)
            new_seq_inv = new_seq_inv[: x_index + 1]
    return new_seq_inv[::-1]


def clean_as_path(path: List[int]) -> List[int]:
    """
    Method for loop and prepending removal.
    """
    (clean_path, is_loopy) = __remove_prepending(path)
    if is_loopy:
        clean_path = __clean_loops(clean_path)
    return clean_path
