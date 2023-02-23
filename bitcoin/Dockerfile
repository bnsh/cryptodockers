FROM ubuntu:22.04

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
		curl \
	&& echo "bitcoin ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-bitcoin \
	&& /bin/true

RUN mkdir -p /home/bitcoin/src/ /home/bitcoin/.bitcoin/
RUN git clone https://github.com/bitcoin/bitcoin.git /home/bitcoin/src/bitcoin
RUN ( cd /home/bitcoin/src/bitcoin && ./autogen.sh && ./configure --with-gui=no --disable-wallet --prefix="/usr/local/bitcoin" && make all install )

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > /tmp/rust.sh && chmod 755 /tmp/rust.sh && export RUSTUP_HOME=/opt/rust CARGO_HOME=/opt/rust && echo "export RUSTUP_HOME=${RUSTUP_HOME} CARGO_HOME=${CARGO_HOME}" && bash /tmp/rust.sh -y --no-modify-path

# RUN git clone https://github.com/casey/ord.git /home/bitcoin/src/ord
# RUN ( cd /home/bitcoin/src/ord && ./autogen.sh && ./configure --prefix="/usr/local/ord" && make all install )

RUN find /home/bitcoin -print0 | xargs -0 chown bitcoin:bitcoin

COPY supervisor.d /etc/supervisor/conf.d

EXPOSE 8332

USER root

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
