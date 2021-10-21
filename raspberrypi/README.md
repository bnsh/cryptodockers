# Raspberry Pi Notes

So, first, all this is based on [Ubuntu Desktop 21.10 for Raspberry Pi](https://ubuntu.com/download/raspberry-pi)

After installing Ubuntu on the Pi, do

1. `sudo su -` 
2. `apt update -y`
3. `apt upgrade -y`
4. (exit out of root)
5. `mkdir -p src/`
6. `cd src`
7. `git clone https://github.com/bnsh/cryptodockers.git`
8. ```sudo apt install -y `cat ${HOME}/src/cryptodockers/raspberrypi/apt-packages.txt```
9. `sudo python3 -m pip install -U -r ${HOME}/src/cryptodockers/raspberrypi/requirements.txt`
10. ```sudo addgroup "`id -nu`" docker` ```

Actually. I'll probably turn all this into a Makefile.