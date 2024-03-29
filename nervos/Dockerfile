FROM ubuntu:22.04

LABEL maintainer="Binesh Bannerjee <binesh_binesh@hotmail.com>"

ENV TZ=US/Eastern RUSTUP_HOME=/opt/rust CARGO_HOME=/opt/rust
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN \
	adduser --gecos nervos nervos \
	&& addgroup --system supervisord \
	&& addgroup nervos supervisord \
	&& apt-get update -y \
	&& apt-get install -y \
		autoconf \
		automake \
		autotools-dev \
		bsdmainutils \
		build-essential \
		clang \
		curl \
		gcc \
		git \
		libboost-dev \
		libboost-filesystem-dev \
		libboost-system-dev \
		libboost-test-dev \
		libc6-dev \
		libclang-dev \
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
	&& echo "nervos ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-nervos \
	&& /bin/true

RUN mkdir -p /home/nervos/src/ /home/nervos/.nervos/
RUN ( git clone https://github.com/nervosnetwork/ckb.git /home/nervos/src/nervos && cd /home/nervos/src/nervos && git checkout master )

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > /tmp/rust.sh && chmod 755 /tmp/rust.sh && export PATH="${RUSTUP_HOME}/bin:${PATH}" && bash /tmp/rust.sh -y --no-modify-path && . /opt/rust/env && rustup default stable

RUN ( . /opt/rust/env && cd /home/nervos/src/nervos && make prod )
RUN find /home/nervos/src/nervos -type f -name 'ckb' -print
RUN cp -pv /home/nervos/src/nervos/target/prod/ckb /usr/local/bin/ckb

RUN find /home/nervos -print0 | xargs -0 chown nervos:nervos

COPY supervisor.d /etc/supervisor/conf.d

EXPOSE 8332

USER root

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
