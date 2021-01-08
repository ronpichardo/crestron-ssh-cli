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
-a, --adhoc - run a command passed in as an argument
```

FLAG:
all - a flag set for the close-ports option, to include the shutdown of the webserver

Output example when running, including an IP that created an exception
<img width="703" alt="SShOutput" src="https://user-images.githubusercontent.com/63974878/104048673-a0934780-51b1-11eb-93aa-862724c03f2b.png">

```shell
(myvenv) ➜  crestron-ssh-cli git:(main) ✗ python main.py -v devices.csv 
CP3 Cntrl Eng [v1.501.2867.24563 (Nov 07 2016)
CP3 Cntrl Eng [v1.601.3935.27221 (Oct 11 2019)
Unable to connect to 100.112.200.31
CP3 Cntrl Eng [v1.601.3935.27221 (Oct 11 2019)
CP3 Cntrl Eng [v1.601.3935.27221 (Oct 11 2019)
CP3 Cntrl Eng [v1.601.3935.27221 (Oct 11 2019)
CP3 Cntrl Eng [v1.501.2867.24563 (Nov 07 2016)
```
[Not yet implemented] update - an update to the version option, to update hardware if it is out of date