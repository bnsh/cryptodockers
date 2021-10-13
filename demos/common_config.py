#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""This is stuff that is common to all the bitcoin demos."""

import os
import configparser

def grab_config():
    config = configparser.ConfigParser()
    localmkfn = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../local.mk"))
    with open(localmkfn, "rt", encoding="utf-8") as cfp:
        config.read_string(f"[DEFAULT]\n{cfp.read():s}\n")
    return config["DEFAULT"]
