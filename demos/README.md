# Setting up SCP Handler

So, for bitcoin, unfortunately, we need to get the .bitcoin/.cookie file. This is difficult if it's on another box though.

So, first, we have to create a ssh key. Run this on the machine that you intend to run bitcoin_example.py from.

1. `cd ${HOME}/.ssh`
2. `ssh-keygen -f bitcoin_scpcookiehandler -C "Bitcoin SCP Cookie Handler"`
3. edit `${HOME}/.ssh/config` to contain the lines

        Host bitcoin_scpcookiehandler
            IdentityFile ~/.ssh/bitcoin_scpcookiehandler
            IdentitiesOnly yes
            Hostname {dockerhostname}
            User {dockerhostnameuser}
 4. There should be a file `${HOME}/.ssh/bitcoin_scpcookiehandler.pub`.
 5. cat this file, and copy it to the clipboard.

On whatever machine that's running the bitcoin docker:

1. Add this line to `${HOME}/.ssh/authorized_keys`

        command="/usr/bin/env python3 ${HOME}/src/cryptocurrency-docker/demos/bitcoin_scpcookiehandler.py" {pasted public key}

That _should_ be it..
