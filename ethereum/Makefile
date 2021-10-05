include ../local.mk
CRYPTOCURRENCY=ethereum
RPCPORT=8545

all:

build:
	docker image ls -a | grep "$(USERNAME)/$(CRYPTOCURRENCY)_node" || docker build -t "$(USERNAME)/$(CRYPTOCURRENCY)_node" .

build-force:
	docker build -t "$(USERNAME)/$(CRYPTOCURRENCY)_node" .

run: build
	docker container run -it --rm -v "$(CRYPTOCURRENCY_ROOT)/$(CRYPTOCURRENCY):/home/$(CRYPTOCURRENCY)" -p "127.0.0.1:$(RPCPORT):$(RPCPORT)/tcp" "$(USERNAME)/$(CRYPTOCURRENCY)_node" /bin/bash

daemon: build
	docker container stop `docker container ls -a | grep "$(USERNAME)/$(CRYPTOCURRENCY)_node" | sed -e 's/[ 	][ 	]*/	/g' | cut -d'	' -f1` || true
	docker container run -d --rm -v "$(CRYPTOCURRENCY_ROOT)/$(CRYPTOCURRENCY):/home/$(CRYPTOCURRENCY)" -p "127.0.0.1:$(RPCPORT):$(RPCPORT)/tcp" "$(USERNAME)/$(CRYPTOCURRENCY)_node"

attach:
	docker exec -it `docker container ls -a | grep "$(USERNAME)/$(CRYPTOCURRENCY)_node" | sed -e 's/[ 	][ 	]*/	/g' | cut -d'	' -f1` /bin/bash

stop:
	docker container stop `docker container ls -a | grep "$(USERNAME)/$(CRYPTOCURRENCY)_node" | sed -e 's/[ 	][ 	]*/	/g' | cut -d'	' -f1` || true

clean:
	docker image rm -f "$(USERNAME)/$(CRYPTOCURRENCY)_node"

cache: build
	docker container run -it --rm -v "$(CRYPTOCURRENCY_ROOT):/cryptocurrency" "$(USERNAME)/$(CRYPTOCURRENCY)_node" /usr/bin/rsync -av --progress --delete --exclude=".$(CRYPTOCURRENCY)/" "/home/$(CRYPTOCURRENCY)/" "/cryptocurrency/$(CRYPTOCURRENCY)/"
	docker container run -it --rm -v "$(CRYPTOCURRENCY_ROOT):/cryptocurrency" "$(USERNAME)/$(CRYPTOCURRENCY)_node" /usr/bin/rsync -av --progress --delete --exclude=".$(CRYPTOCURRENCY)/" "/home/$(CRYPTOCURRENCY)/" "/cryptocurrency/pristine/$(CRYPTOCURRENCY)/"
	docker container run -it --rm -v "$(CRYPTOCURRENCY_ROOT):/cryptocurrency" "$(USERNAME)/$(CRYPTOCURRENCY)_node" /bin/sh -c '/bin/mkdir -p "/cryptocurrency/$(CRYPTOCURRENCY)/.$(CRYPTOCURRENCY)" "/cryptocurrency/pristine/$(CRYPTOCURRENCY)/.$(CRYPTOCURRENCY)/"; /bin/chown "$(CRYPTOCURRENCY):$(CRYPTOCURRENCY)" "/cryptocurrency/$(CRYPTOCURRENCY)/.$(CRYPTOCURRENCY)" "/cryptocurrency/pristine/$(CRYPTOCURRENCY)/.$(CRYPTOCURRENCY)/"'
