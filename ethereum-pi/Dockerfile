FROM ubuntu:20.04

LABEL maintainer="Binesh Bannerjee <binesh_binesh@hotmail.com>"

ENV TZ=US/Eastern
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN \
	groupadd -r ethereum \
	&& useradd -m -r -s /bin/bash -g ethereum ethereum \
	&& apt-get update -y \
	&& apt-get install -y \
		build-essential \
		supervisor \
		supervisor-doc \
		rsync \
		sudo \
		git \
		vim \
		wget \
	&& wget -O /tmp/go.linux-arm64.tar.gz https://golang.org/dl/go1.17.2.linux-arm64.tar.gz \
	&& rm -rf /usr/local/go && tar -C /usr/local -xzf /tmp/go.linux-arm64.tar.gz \
	&& ln -s /usr/local/go/bin/go /usr/local/bin/go \
	&& ln -s /usr/local/go/bin/gofmt /usr/local/bin/gofmt \
	&& echo "ethereum ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-ethereum \
	&& /bin/true

RUN mkdir -p /home/ethereum/src/
RUN git clone https://github.com/ethereum/go-ethereum.git /home/ethereum/src/go-ethereum
RUN ( cd /home/ethereum/src/go-ethereum && perl -p -i -e 's/ci.go install/ci.go install -arch arm64/g' Makefile && make geth )

RUN find /home/ethereum -print0 | xargs -0 chown ethereum:ethereum

COPY supervisor.d /etc/supervisor/conf.d

EXPOSE 8545

USER root

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
