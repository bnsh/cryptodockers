
# Raspberry Pi Notes

So, first, all this is based on [Ubuntu Desktop 21.04 for Raspberry Pi](https://ubuntu.com/download/raspberry-pi) It *needs* to be 21.04, *not* 21.10! Unfortunately, 21.10 seems to have [an issue with Docker](https://forum.storj.io/t/ubuntu-21-10-os-update-problem-with-the-node/15763).

After installing Ubuntu on the Pi, do

1. `sudo apt update -y` _# Took 30.697s_
2. `sudo apt upgrade -y` _# Took 15m30.042s_
3. `sudo apt install -y git` _# Took 15.614s_
4. `mkdir -p "${HOME}/src/"`
5. `cd src`
6. `git clone https://github.com/bnsh/cryptodockers.git` _# Took 0.558s_
7. ```sudo apt install -y `cat ${HOME}/src/cryptodockers/raspberrypi/apt-packages.txt` ``` _# Took 2m20.794s_
8. `sudo python3 -m pip install -U -r ${HOME}/src/cryptodockers/raspberrypi/requirements.txt` _# Took 2m17.157s_
9. ```sudo addgroup "`id -nu`" docker```
10. ```sudo /sbin/shutdown -r now```
11. **Copy local-demo.mk to local.mk and adjust parameters to your needs. The only thing that might need changing is USERNAME.**
12. ```sudo mkdir -p /cryptocurrency``` **If you have an external hard drive, there are additional steps here!** (Also, if you adjusted the "CRYPTOCURRENCY_ROOT" in local.mk, then this directory will need to be the same as whatever you specified there.)
13. **If** this is a bitcoin node:
14. ```( cd "${HOME}/src/cryptodockers/bitcoin" && make build-force )``` _# Took xxxs_
15. ```( cd "${HOME}/src/cryptodockers/bitcoin" && make cache )```
16. ```( cd "${HOME}/src/cryptodockers/bitcoin" && make daemon )```
17. ```( cd "${HOME}/src/cryptodockers/bitcoin" && make attach )```
18. Really there's a bunch of things to do from here.
19. **If** this is an ethereum node:
20. ```( cd "${HOME}/src/cryptodockers/ethereum-pi" && make build-force )``` _# Took xxxs_
21. ```( cd "${HOME}/src/cryptodockers/ethereum-pi" && make cache )```
22. ```( cd "${HOME}/src/cryptodockers/ethereum-pi" && make daemon )```
23. ```( cd "${HOME}/src/cryptodockers/ethereum-pi" && make attach )```
24. Really there's a bunch of things to do from here.
