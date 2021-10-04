all:

build:
	docker build -t binesh/ethereum_node .

run: build
	docker container run -it --rm -v /cryptocurrency/ethereum:/home/ethereum -p 8545:8545 binesh/ethereum_node /bin/bash

daemon: build
	docker container stop `docker container ls -a | grep binesh/ethereum_node | sed -e 's/[ 	][ 	]*/	/g' | cut -d'	' -f1` || /bin/true
	docker container run -d --rm -v /cryptocurrency/ethereum:/home/ethereum -p 8545:8545 binesh/ethereum_node

attach:
	docker exec -it `docker container ls -a | grep binesh/ethereum_node | sed -e 's/[ 	][ 	]*/	/g' | cut -d'	' -f1` /bin/bash

stop:
	docker container stop `docker container ls -a | grep binesh/ethereum_node | sed -e 's/[ 	][ 	]*/	/g' | cut -d'	' -f1` || /bin/true

clean:
	docker image rm -f binesh/ethereum_node

cache: build
	docker container run -it --rm -v /cryptocurrency:/cryptocurrency binesh/ethereum_node /usr/bin/rsync -av --progress --delete --exclude=.ethereum/ /home/ethereum/ /cryptocurrency/ethereum/
	docker container run -it --rm -v /cryptocurrency:/cryptocurrency binesh/ethereum_node /usr/bin/rsync -av --progress --delete --exclude=.ethereum/ /home/ethereum/ /cryptocurrency/pristine/ethereum/
	docker container run -it --rm -v /cryptocurrency:/cryptocurrency binesh/ethereum_node /bin/sh -c '/bin/mkdir -p /cryptocurrency/ethereum/.ethereum /cryptocurrency/pristine/ethereum/.ethereum/; /bin/chown ethereum:ethereum /cryptocurrency/ethereum/.ethereum /cryptocurrency/pristine/ethereum/.ethereum/'
