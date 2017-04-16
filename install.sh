#!/bin/bash
cp juiceit.py /usr/local/bin/juiceit
chmod +x /usr/local/bin/juiceit
cp init.d/juiceit /etc/init.d/juiceit
chmod +x /etc/init.d/juiceit
ln -s /etc/init.d/juiceit /etc/rc5.d/S99juiceit
