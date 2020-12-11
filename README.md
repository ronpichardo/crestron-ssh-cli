## Overview

CLI tool for sending common commands to Crestron Devices.

## Installation
Installation
```shell
$ git clone https://github.com/ronpichardo/crestron-ssh-cli.git
$ cd crestron-ssh-cli
$ python3 -m venv myvenv
$ source myvenv/bin/activate
$ pip install -r requirements.txt
```
Usage:
```shell
$ python3 main.py [OPTIONS] <filename>.csv flag=<all|update>
```
OPTIONS:
```shell
-v, --version - get version of devices provided into the csv file
-ch, --check-ports - gets the status of ports, returns if the port is on/off for webserver, ftpserver, ctpconsole, telnet
-cl, --close-ports - close ports if they are on/enabled for ftpserver, ctpconsole, telnet
```

FLAG:
all - a flag set for the close-ports option, to include the shutdown of the webserver

[Not yet implemented] update - an update to the version option, to update hardware if it is out of date