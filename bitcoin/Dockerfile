FROM ubuntu:22.04

LABEL maintainer="Binesh Bannerjee <binesh_binesh@hotmail.com>"

ENV TZ=US/Eastern RUSTUP_HOME=/opt/rust CARGO_HOME=/opt/rust
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN \
	groupadd -r bitcoin \
	&& useradd -m -r -s /bin/bash -g bitcoin bitcoin \
	&& apt-get update -y \
	&& apt-get install -y \
		autoconf \
		automake \
		autotools-dev \
		bsdmainutils \
		build-essential \
		curl \
		git \
		libboost-dev \
		libboost-filesystem-dev \
		libboost-system-dev \
		libboost-test-dev \
		libevent-dev \
		libminiupnpc-dev \
		libnatpmp-dev \
		libqrencode-dev \
		libqt5core5a \
		libqt5dbus5 \
		libqt5gui5 \
		libsqlite3-dev \
		libssl-dev \
		libtool \
		libzmq3-dev \
		pkg-config \
		python3 \
		python3-dev \
		qttools5-dev \
		qttools5-dev-tools \
		qtwayland5 \
		rsync \
		sudo \
		supervisor \
		supervisor-doc \
		systemtap-sdt-dev \
		vim \
	&& echo "bitcoin ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-bitcoin \
	&& /bin/true

RUN mkdir -p /home/bitcoin/src/ /home/bitcoin/.bitcoin/
RUN git clone https://github.com/bitcoin/bitcoin.git /home/bitcoin/src/bitcoin
RUN ( cd /home/bitcoin/src/bitcoin && ./autogen.sh && ./configure --prefix="/usr/local/bitcoin" && make all install )

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > /tmp/rust.sh && chmod 755 /tmp/rust.sh && export PATH="${RUSTUP_HOME}/bin:${PATH}" && bash /tmp/rust.sh -y --no-modify-path && . /opt/rust/env && rustup default stable

RUN git clone https://github.com/casey/ord.git /home/bitcoin/src/ord
RUN ( . /opt/rust/env &&  cd /home/bitcoin/src/ord && cargo build --release )
RUN cp -pv /home/bitcoin/src/ord/target/release/ord /usr/local/bin/ord

RUN find /home/bitcoin -print0 | xargs -0 chown bitcoin:bitcoin

COPY supervisor.d /etc/supervisor/conf.d

EXPOSE 8332

USER root

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
