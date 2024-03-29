# Raspberry Pi Notes

So, first, all this is based on [Ubuntu Desktop 22.04 for Raspberry Pi](https://ubuntu.com/download/raspberry-pi)

After installing Ubuntu on the Pi, do

1. `sudo apt update -y` _# Took 30.697s_
2. `sudo apt upgrade -y` _# Took 15m30.042s_
3. `sudo apt install -y git` _# Took 15.614s_
4. `mkdir -p "${HOME}/src/"`
5. `cd "${HOME}/src/"`
6. `git clone https://github.com/bnsh/cryptodockers.git` _# Took 0.558s_
7. ```sudo apt install -y `cat ${HOME}/src/cryptodockers/raspberrypi/apt-packages.txt` ``` _# Took 2m20.794s_
8. sudo python3 "${HOME}/src/cryptodockers/raspberrypi/get-pip.py"
9. `sudo python3 -m pip install -U -r ${HOME}/src/cryptodockers/raspberrypi/requirements.txt` _# Took 2m17.157s_
10. ```sudo addgroup "`id -nu`" docker```
11. ```sudo addgroup --system supervisord```
12. ```sudo addgroup "`id -nu`" supervisord```
13. ```sudo cp -p "${HOME}/src/cryptodockers/raspberrypi/root.conf" /etc/supervisor/conf.d/root.conf```
14. ```sudo cp -p "${HOME}/src/cryptodockers/raspberrypi/chown-socket.conf" /etc/supervisor/conf.d/chown-socket.conf```
15. ```sudo /sbin/shutdown -r now```
16. \# **Copy local-demo.mk to local.mk and adjust parameters to your needs. The only thing that might need changing is USERNAME.**
17. ```sudo mkdir -p /cryptocurrency``` # **If you have an external hard drive, there are additional steps here!** (Also, if you adjusted the "CRYPTOCURRENCY_ROOT" in local.mk, then this directory will need to be the same as whatever you specified there.)
18. ```sudo rm -f /etc/nginx/sites-enabled/default /etc/nginx/sites-enabled/cryptoproxy```
19. ```sudo cp -p "${HOME}/src/cryptodockers/nginx/cryptoproxy" /etc/nginx/sites-available/cryptoproxy```
20. ```sudo ln -s /etc/nginx/sites-available/cryptoproxy /etc/nginx/sites-enabled/cryptoproxy```
21. ```sudo cp -p "${HOME}/src/cryptodockers/nginx/bitcoin.conf" /etc/nginx/snippets/```
22. ```sudo cp -p "${HOME}/src/cryptodockers/nginx/ethereum.conf" /etc/nginx/snippets/```
23. ```sudo systemctl restart nginx```
24. \# **If** this is a bitcoin node:
25. ```( cd "${HOME}/src/cryptodockers/bitcoin" && make build-force )``` _# Took 162m5.510s_
26. ```( cd "${HOME}/src/cryptodockers/bitcoin" && make cache )```
27. ```( cd "${HOME}/src/cryptodockers/bitcoin" && make bitcoin.conf )```
28. ```sudo cp -p "${HOME}/src/cryptodockers/bitcoin/bitcoin.conf" /etc/supervisor/conf.d/```
29. \# **If** this is an ethereum node:
30. ```( cd "${HOME}/src/cryptodockers/ethereum-pi" && make build-force )``` _# Took 10m7.479s_
31. ```( cd "${HOME}/src/cryptodockers/ethereum-pi" && make cache )```
32. ```( cd "${HOME}/src/cryptodockers/ethereum-pi" && make ethereum.conf )```
33. ```sudo cp -p "${HOME}/src/cryptodockers/ethereum-pi/ethereum.conf" /etc/supervisor/conf.d/```
34. ```sudo /sbin/shutdown -r now```
35. \# **If** this is an nervos node:
36. ```( cd "${HOME}/src/cryptodockers/nervos" && make build-force )``` _# Took 169m35.080s_
37. ```( cd "${HOME}/src/cryptodockers/nervos" && make cache )```
38. ```( cd "${HOME}/src/cryptodockers/nervos" && make nervos.conf )```
39. ```sudo cp -p "${HOME}/src/cryptodockers/nervos/nervos.conf" /etc/supervisor/conf.d/```
40. ```sudo /sbin/shutdown -r now```
