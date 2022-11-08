import os

from tinydb import TinyDB, Query
from tinydb.operations import set


def is_multi_fp_collection():
    return __query_flag("COLLECT_MULTIPLE_FP")


def set_multi_fp_collection(is_multi):
    __set_flag("COLLECT_MULTIPLE_FP", is_multi)


def is_fp_ready():
    return __query_flag("FP_READY")


def set_fp_ready(ready_state):
    __set_flag("FP_READY", ready_state)


def is_rw_done():
    return __query_flag("RW_DONE")


def set_rw_done():
    __set_flag("RW_DONE", True)


def get_fp_path():
    dir_name = "fingerprints" if is_multi_fp_collection() else "fingerprint"
    return os.path.join(os.path.abspath(os.path.curdir), dir_name)


def collect_fingerprint():
    with open(get_fp_path() + "/fp.txt", "r") as file:
        fp = file.readline().replace("[", "").replace("]", "").replace(" ", "")
    # print("Collected FP.")
    return fp


def initialize_storage():
    db = __get_storage()
    db.drop_tables()  # reset database to start from scratch
    db.insert({"key": "COLLECT_MULTIPLE_FP", "value": False})
    db.insert({"key": "FP_READY", "value": False})
    db.insert({"key": "RW_DONE", "value": False})


def __get_storage():
    return TinyDB(os.path.join(os.path.abspath(os.path.curdir), "storage.json"))


def __query_flag(key):
    flag = __get_storage().get(Query().key == str(key))
    assert flag is not None
    # print("{} is {}".format(key, flag["value"]))
    return flag["value"]


def __set_flag(key, value):
    __get_storage().update(set("value", value), Query().key == str(key))
    # print("Set {} to {}".format(key, value))
