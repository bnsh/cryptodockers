# Raspberry Pi Notes

So, first, all this is based on [Ubuntu Desktop 21.04 for Raspberry Pi](https://ubuntu.com/download/raspberry-pi) It *needs* to be 21.04, *not* 21.10! Unfortunately, 21.10 seems to have [an issue with Docker](https://forum.storj.io/t/ubuntu-21-10-os-update-problem-with-the-node/15763).

After installing Ubuntu on the Pi, do

1. `sudo su -` 
2. `apt update -y`
3. `apt upgrade -y`
4. `apt install -y git`
5. (exit out of root)
6. `mkdir -p src/`
7. `cd src`
8. `git clone https://github.com/bnsh/cryptodockers.git`
9. ```sudo apt install -y `cat ${HOME}/src/cryptodockers/raspberrypi/apt-packages.txt` ```
   *non-super users should _not_ be able to capture packets.*
10. `sudo python3 -m pip install -U -r ${HOME}/src/cryptodockers/raspberrypi/requirements.txt`
11. ```sudo addgroup "`id -nu`" docker```
12. ```sudo /sbin/shutdown -r now```
13. **Copy local-demo.mk to local.mk and adjust parameters to your needs. Probably the only thing that might need changing is USERNAME.**
14. ```sudo mkdir -p /cryptocurrency``` **If you have an external hard drive, there are additional steps here!** (Also, if you adjusted the "CRYPTOCURRENCY_ROOT" in local.mk, then this directory will need to be the same as whatever you specified there.)
15. **If** this is a bitcoin node:
16. ```( cd "${HOME}/src/cryptodockers/bitcoin" && make build-force )```
17. ```( cd "${HOME}/src/cryptodockers/bitcoin" && make cache )```
18. ```( cd "${HOME}/src/cryptodockers/bitcoin" && make daemon )```
19. ```( cd "${HOME}/src/cryptodockers/bitcoin" && make attach )```
20. **If** this is an ethereum node:
21. ```( cd "${HOME}/src/cryptodockers/ethereum-pi" && make build-force )```
22. ```( cd "${HOME}/src/cryptodockers/ethereum-pi" && make cache )```
23. ```( cd "${HOME}/src/cryptodockers/ethereum-pi" && make daemon )```
24. ```( cd "${HOME}/src/cryptodockers/ethereum-pi" && make attach )```

Actually. I'll probably turn all this into a Makefile. And, `apt-packages.txt` and `requirements.txt` are a giant mess. I need to slim those down to the minimum requirements.
