# Raspberry Pi Notes

So, first, all this is based on [Ubuntu Desktop 21.04 for Raspberry Pi](https://ubuntu.com/download/raspberry-pi) It *needs* to be 21.04, *not* 21.10! Unfortunately, 21.10 seems to have [an issue with Docker](https://forum.storj.io/t/ubuntu-21-10-os-update-problem-with-the-node/15763).

After installing Ubuntu on the Pi, do

1. `sudo apt update -y` _# Took 30.697s_
2. `sudo apt upgrade -y` _# Took 15m30.042s_
3. `sudo apt install -y git` _# Took 15.614s_
4. `mkdir -p "${HOME}/src/"`
5. `cd "${HOME}/src/"`
6. `git clone https://github.com/bnsh/cryptodockers.git` _# Took 0.558s_
7. ```sudo apt install -y `cat ${HOME}/src/cryptodockers/raspberrypi/apt-packages.txt` ``` _# Took 2m20.794s_
8. `sudo python3 -m pip install -U -r ${HOME}/src/cryptodockers/raspberrypi/requirements.txt` _# Took 2m17.157s_
9. ```sudo addgroup "`id -nu`" docker```
10. ```sudo /sbin/shutdown -r now```
11. \# **Copy local-demo.mk to local.mk and adjust parameters to your needs. The only thing that might need changing is USERNAME.**
12. ```sudo mkdir -p /cryptocurrency``` # **If you have an external hard drive, there are additional steps here!** (Also, if you adjusted the "CRYPTOCURRENCY_ROOT" in local.mk, then this directory will need to be the same as whatever you specified there.)
13. ```sudo rm -f /etc/nginx/sites-enabled/default /etc/nginx/sites-enabled/cryptoproxy```
14. ```sudo cp -p "${HOME}/src/cryptodockers/nginx/cryptoproxy" /etc/nginx/sites-available/cryptoproxy```
15. ```sudo ln -s /etc/nginx/sites-available/cryptoproxy /etc/nginx/sites-enabled/cryptoproxy```
16. ```sudo cp -p "${HOME}/src/cryptodockers/nginx/bitcoin.conf" /etc/nginx/snippets/```
17. ```sudo cp -p "${HOME}/src/cryptodockers/nginx/ethereum.conf" /etc/nginx/snippets/```
18. ```sudo systemctl restart nginx```
19. \# **If** this is a bitcoin node:
20. ```( cd "${HOME}/src/cryptodockers/bitcoin" && make build-force )``` _# Took 162m5.510s_
21. ```( cd "${HOME}/src/cryptodockers/bitcoin" && make cache )```
22. ```( cd "${HOME}/src/cryptodockers/bitcoin" && make bitcoin.conf )```
23. ```sudo cp -p "${HOME}/src/cryptodockers/bitcoin/bitcoin.conf" /etc/supervisor/conf.d/```
24. \# **If** this is an ethereum node:
25. ```( cd "${HOME}/src/cryptodockers/ethereum-pi" && make build-force )``` _# Took 10m7.479s_
26. ```( cd "${HOME}/src/cryptodockers/ethereum-pi" && make cache )```
27. ```( cd "${HOME}/src/cryptodockers/ethereum-pi" && make ethereum.conf )```
28. ```sudo cp -p "${HOME}/src/cryptodockers/ethereum-pi/ethereum.conf" /etc/supervisor/conf.d/```
29. ```sudo /sbin/shutdown -r now```
