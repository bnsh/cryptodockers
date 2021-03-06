FROM ubuntu:20.04

LABEL maintainer="Binesh Bannerjee <binesh_binesh@hotmail.com>"

ENV TZ=US/Eastern
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN \
	groupadd -r bitcoin \
	&& useradd -m -r -s /bin/bash -g bitcoin bitcoin \
	&& apt-get update -y \
	&& apt-get install -y \
		build-essential \
		bsdmainutils \
		autoconf \
		libtool \
		pkg-config \
		supervisor \
		supervisor-doc \
		rsync \
		libboost-dev \
		libboost-system-dev \
		libboost-filesystem-dev \
		libboost-test-dev \
		libevent-dev \
		sudo \
		git \
		vim \
	&& echo "bitcoin ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-bitcoin \
	&& /bin/true

RUN mkdir -p /home/bitcoin/src/ /home/bitcoin/.bitcoin/
RUN git clone https://github.com/bitcoin/bitcoin.git /home/bitcoin/src/bitcoin
RUN ( cd /home/bitcoin/src/bitcoin && ./autogen.sh && ./configure --with-gui=no --disable-wallet --prefix="/usr/local/bitcoin" && make all install )

RUN find /home/bitcoin -print0 | xargs -0 chown bitcoin:bitcoin

COPY supervisor.d /etc/supervisor/conf.d

EXPOSE 8332

USER root

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
