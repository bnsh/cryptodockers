#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""This is stuff that is common to all the bitcoin demos."""

import os
from functools import reduce

import configparser

def search_for_configfn():
    candidates = [
        os.path.join(os.path.realpath(path), fname)
        for path in reversed([os.path.dirname(os.path.realpath(__file__))] + list(reduce(lambda acc, x: acc + [acc[-1] + "/" + x], os.getcwd().split("/")[1:], ["/"])) + ["/secrets"])
        for fname in ("local.mk",)
    ]
    candidates = [cand for cand in candidates if os.path.exists(cand)]
    return candidates[0]

def grab_config(configfn=None):
    config = configparser.ConfigParser()
    configfn = configfn or search_for_configfn()
    with open(configfn, "rt", encoding="utf-8") as cfp:
        config.read_string(f"[DEFAULT]\n{cfp.read():s}\n")
    return config["DEFAULT"]
