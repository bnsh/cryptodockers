include ../local.mk
CRYPTOCURRENCY=bitcoin
RPCPORT=8332

all:

build:
	docker image ls -a | grep "$(USERNAME)/$(CRYPTOCURRENCY)_node" || docker build -t "$(USERNAME)/$(CRYPTOCURRENCY)_node" .

build-force:
	docker build -t "$(USERNAME)/$(CRYPTOCURRENCY)_node" .

# # I'm commenting these out, because _ultimately_ we'll run the $(CRYPTOCURRENCY)_node via supervisor, and it'll make sure things stay _up_...
# # If you run them directly, they'll interfere with each other, since _both_ will be trying to write to $(CRYPTOCURRENCY_ROOT)..
# run: build
# 	docker container run -it --rm -v "$(CRYPTOCURRENCY_ROOT)/$(CRYPTOCURRENCY):/home/$(CRYPTOCURRENCY)" -p "127.0.0.1:$(RPCPORT):$(RPCPORT)/tcp" "$(USERNAME)/$(CRYPTOCURRENCY)_node" /bin/bash

$(CRYPTOCURRENCY).conf: build $(CRYPTOCURRENCY).conf.tmpl
	\
		CRYPTOCURRENCY="$(CRYPTOCURRENCY)" \
		CRYPTOCURRENCY_ROOT="$(CRYPTOCURRENCY_ROOT)" \
		RPCPORT="$(RPCPORT)" \
		USERNAME="$(USERNAME)" \
		envsubst < $(CRYPTOCURRENCY).conf.tmpl > $(CRYPTOCURRENCY).conf

# # I'm commenting these out, because _ultimately_ we'll run the $(CRYPTOCURRENCY)_node via supervisor, and it'll make sure things stay _up_...
# # If you run them directly, they'll interfere with each other, since _both_ will be trying to write to $(CRYPTOCURRENCY_ROOT)..
# daemon: build
# 	docker container stop `docker container ls -a | grep "$(USERNAME)/$(CRYPTOCURRENCY)_node" | sed -e 's/[ 	][ 	]*/	/g' | cut -d'	' -f1` || true
# 	docker container run -d --rm -v "$(CRYPTOCURRENCY_ROOT)/$(CRYPTOCURRENCY):/home/$(CRYPTOCURRENCY)" -p "127.0.0.1:$(RPCPORT):$(RPCPORT)/tcp" "$(USERNAME)/$(CRYPTOCURRENCY)_node"

# This is safe to run even when being run via supervisor.
attach:
	docker exec -it `docker container ls -a | grep "$(USERNAME)/$(CRYPTOCURRENCY)_node" | sed -e 's/[ 	][ 	]*/	/g' | cut -d'	' -f1` /bin/bash

# # I'm commenting these out, because _ultimately_ we'll run the $(CRYPTOCURRENCY)_node via supervisor, and it'll make sure things stay _up_...
# # If you run them directly, they'll interfere with each other, since _both_ will be trying to write to $(CRYPTOCURRENCY_ROOT)..
# stop:
# 	docker container stop `docker container ls -a | grep "$(USERNAME)/$(CRYPTOCURRENCY)_node" | sed -e 's/[ 	][ 	]*/	/g' | cut -d'	' -f1` || true

# # I'm commenting these out, because _ultimately_ we'll run the $(CRYPTOCURRENCY)_node via supervisor, and it'll make sure things stay _up_...
# # If you run clean while supervisor is running... *Might* cause problems... I didn't want to test this. You probably shouldn't either.
# clean:
# 	docker image rm -f "$(USERNAME)/$(CRYPTOCURRENCY)_node"

cache: build
	docker container run -it --rm -v "$(CRYPTOCURRENCY_ROOT):/cryptocurrency" "$(USERNAME)/$(CRYPTOCURRENCY)_node" /bin/sh -c '/bin/mkdir -p "/cryptocurrency/$(CRYPTOCURRENCY)/.$(CRYPTOCURRENCY)" "/cryptocurrency/pristine/$(CRYPTOCURRENCY)/.$(CRYPTOCURRENCY)/"; /bin/chown "$(CRYPTOCURRENCY):$(CRYPTOCURRENCY)" "/cryptocurrency/$(CRYPTOCURRENCY)/.$(CRYPTOCURRENCY)" "/cryptocurrency/pristine/$(CRYPTOCURRENCY)/.$(CRYPTOCURRENCY)/"'
	docker container run -it --rm -v "$(CRYPTOCURRENCY_ROOT):/cryptocurrency" "$(USERNAME)/$(CRYPTOCURRENCY)_node" /usr/bin/rsync -av --progress --delete --exclude=".$(CRYPTOCURRENCY)/" "/home/$(CRYPTOCURRENCY)/" "/cryptocurrency/$(CRYPTOCURRENCY)/"
	docker container run -it --rm -v "$(CRYPTOCURRENCY_ROOT):/cryptocurrency" "$(USERNAME)/$(CRYPTOCURRENCY)_node" /usr/bin/rsync -av --progress --delete --exclude=".$(CRYPTOCURRENCY)/" "/home/$(CRYPTOCURRENCY)/" "/cryptocurrency/pristine/$(CRYPTOCURRENCY)/"
