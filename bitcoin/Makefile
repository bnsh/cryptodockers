all:

build:
	docker build -t binesh/bitcoin_node .

run: build
	docker container run -it --rm -v /cryptocurrency/bitcoin:/home/bitcoin -p 8332:8332 binesh/bitcoin_node /bin/bash

daemon: build
	docker container stop `docker container ls -a | grep binesh/bitcoin_node | sed -e 's/[ 	][ 	]*/	/g' | cut -d'	' -f1` || /bin/true
	docker container run -d --rm -v /cryptocurrency/bitcoin:/home/bitcoin -p 8332:8332 binesh/bitcoin_node

attach:
	docker exec -it `docker container ls -a | grep binesh/bitcoin_node | sed -e 's/[ 	][ 	]*/	/g' | cut -d'	' -f1` /bin/bash

stop:
	docker container stop `docker container ls -a | grep binesh/bitcoin_node | sed -e 's/[ 	][ 	]*/	/g' | cut -d'	' -f1` || /bin/true

clean:
	docker image rm -f binesh/bitcoin_node

cache: build
	docker container run -it --rm -v /cryptocurrency:/cryptocurrency binesh/bitcoin_node /usr/bin/rsync -av --progress --delete --exclude=.bitcoin/ /home/bitcoin/ /cryptocurrency/bitcoin/
	docker container run -it --rm -v /cryptocurrency:/cryptocurrency binesh/bitcoin_node /usr/bin/rsync -av --progress --delete --exclude=.bitcoin/ /home/bitcoin/ /cryptocurrency/pristine/bitcoin/
	docker container run -it --rm -v /cryptocurrency:/cryptocurrency binesh/bitcoin_node /bin/sh -c '/bin/mkdir -p /cryptocurrency/bitcoin/.bitcoin /cryptocurrency/pristine/bitcoin/.bitcoin/; /bin/chown bitcoin:bitcoin /cryptocurrency/bitcoin/.bitcoin /cryptocurrency/pristine/bitcoin/.bitcoin/'
