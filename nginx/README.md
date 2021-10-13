# NGINX conf file
This nginx conf file will forward requests
1. /bitcoin to localhost:8332 and
2. /ethereum to localhost:8545
This way we can have a machine that runs the dockers for ethereum and bitcoin and an nginx on the host which we can address for all of our requests remotely.
These files should go into `/etc/nginx/snippets` and you need to add

    include snippets/bitcoin.conf;
    include snippets/ethereum.conf;

into /etc/nginx/sites-available/default _after_ the `location / {...}` section (*Not* _inside_ the `location /` brackets!!)
