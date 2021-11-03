#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""This will be the handler for copying the cookie from the docker instance"""

import os
import io
import tarfile
import tempfile
from subprocess import check_call
import docker
from common_config import grab_config

def grab_cookie():
    config = grab_config()
    username = config["USERNAME"]
    name = f"{username}/bitcoin_node:latest"
    client = docker.from_env()
    cookie = None
    for container in client.containers.list():
        if name in set(container.image.attrs["RepoTags"]):
            stream, dummy_stat = container.get_archive("/home/bitcoin/.bitcoin/.cookie")
            tarbin = b"".join(chunk for chunk in stream)
            with tarfile.open(mode="r", fileobj=io.BytesIO(tarbin)) as tarf:
                cookiefile = tarf.getmember(".cookie")
                cookie = tarf.extractfile(cookiefile).read().decode("utf-8")
    return cookie

def main():
    # scp -p -f /wherever/whatever
    cookie = grab_cookie()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpfn = os.path.join(tmpdir, "cookie")
        with open(tmpfn, "wt", encoding="utf-8") as cfp:
            cfp.write(cookie)
        check_call([
            "/usr/bin/env",
            "scp",
            "-p",
            "-f",
            tmpfn
        ])

if __name__ == "__main__":
    main()
