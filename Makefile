all:

push:
	/usr/bin/rsync -avz -e ssh --progress --delete --exclude=RCS/ $(HOME)/src/cryptodockers/ cablemodem.hex21.com:src/cryptodockers/
	/usr/bin/rsync -avz -e ssh --progress --delete --exclude=RCS/ $(HOME)/src/cryptodockers/ p1gen2.home.hex21.com:src/cryptodockers/
	/usr/bin/rsync -avz -e ssh --progress --delete --exclude=RCS/ $(HOME)/src/cryptodockers/ raspberrypi.home.hex21.com:src/cryptodockers/
	/usr/bin/rsync -avz -e ssh --progress --delete --exclude=RCS/ $(HOME)/src/cryptodockers/ raspberrypi2.home.hex21.com:src/cryptodockers/
	/usr/bin/rsync -avz -e ssh --progress --delete --exclude=RCS/ $(HOME)/src/cryptodockers/ cryptocurrency.home.hex21.com:src/cryptodockers/
