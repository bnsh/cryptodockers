all:

push:
	/usr/bin/rsync -avz -e ssh --progress --delete --exclude=RCS/ $(HOME)/src/cryptocurrency-docker/ cablemodem.hex21.com:src/cryptocurrency-docker/
	/usr/bin/rsync -avz -e ssh --progress --delete --exclude=RCS/ $(HOME)/src/cryptocurrency-docker/ p1gen2.home.hex21.com:src/cryptocurrency-docker/
	/usr/bin/rsync -avz -e ssh --progress --delete --exclude=RCS/ $(HOME)/src/cryptocurrency-docker/ raspberrypi.home.hex21.com:src/cryptocurrency-docker/
	/usr/bin/rsync -avz -e ssh --progress --delete --exclude=RCS/ $(HOME)/src/cryptocurrency-docker/ raspberrypi2.home.hex21.com:src/cryptocurrency-docker/
