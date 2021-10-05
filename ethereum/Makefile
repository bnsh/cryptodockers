CRYPTOCURRENCY_ROOT="/cryptocurrency"
CRYPTOCURRENCY="ethereum"
RPCPORT="8545"

all:

build:
	docker build -t "binesh/$(CRYPTOCURRENCY)_node" .

run: build
	docker container run -it --rm -v "$(CRYPTOCURRENCY_ROOT)/$(CRYPTOCURRENCY):/home/$(CRYPTOCURRENCY)" -p "127.0.0.1:$(RPCPORT):$(RPCPORT)/tcp" "binesh/$(CRYPTOCURRENCY)_node" /bin/bash

daemon: build
	docker container stop `docker container ls -a | grep "binesh/$(CRYPTOCURRENCY)_node" | sed -e 's/[ 	][ 	]*/	/g' | cut -d'	' -f1` || /bin/true
	docker container run -d --rm -v "$(CRYPTOCURRENCY_ROOT)/$(CRYPTOCURRENCY):/home/$(CRYPTOCURRENCY)" -p "127.0.0.1:$(RPCPORT):$(RPCPORT)/tcp" "binesh/$(CRYPTOCURRENCY)_node"

attach:
	docker exec -it `docker container ls -a | grep "binesh/$(CRYPTOCURRENCY)_node" | sed -e 's/[ 	][ 	]*/	/g' | cut -d'	' -f1` /bin/bash

stop:
	docker container stop `docker container ls -a | grep "binesh/$(CRYPTOCURRENCY)_node" | sed -e 's/[ 	][ 	]*/	/g' | cut -d'	' -f1` || /bin/true

clean:
	docker image rm -f "binesh/$(CRYPTOCURRENCY)_node"

cache: build
	docker container run -it --rm -v "$(CRYPTOCURRENCY_ROOT):/cryptocurrency" "binesh/$(CRYPTOCURRENCY)_node" /usr/bin/rsync -av --progress --delete --exclude=".$(CRYPTOCURRENCY)/" "/home/$(CRYPTOCURRENCY)/" "/cryptocurrency/$(CRYPTOCURRENCY)/"
	docker container run -it --rm -v "$(CRYPTOCURRENCY_ROOT):/cryptocurrency" "binesh/$(CRYPTOCURRENCY)_node" /usr/bin/rsync -av --progress --delete --exclude=".$(CRYPTOCURRENCY)/" "/home/$(CRYPTOCURRENCY)/" "/cryptocurrency/pristine/$(CRYPTOCURRENCY)/"
	docker container run -it --rm -v "$(CRYPTOCURRENCY_ROOT):/cryptocurrency" "binesh/$(CRYPTOCURRENCY)_node" /bin/sh -c '/bin/mkdir -p "/cryptocurrency/$(CRYPTOCURRENCY)/.$(CRYPTOCURRENCY)" "/cryptocurrency/pristine/$(CRYPTOCURRENCY)/.$(CRYPTOCURRENCY)/"; /bin/chown "$(CRYPTOCURRENCY):$(CRYPTOCURRENCY)" "/cryptocurrency/$(CRYPTOCURRENCY)/.$(CRYPTOCURRENCY)" "/cryptocurrency/pristine/$(CRYPTOCURRENCY)/.$(CRYPTOCURRENCY)/"'
