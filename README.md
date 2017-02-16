# ProxyManager

## How to start it
To start the code, just run ProxyManager.py on a python 3 shell.

## Requirements
The project requires the following python packages:
- pymongo
- pycurl

It also requires:
- python 3
- mongo database at localhost and with default port (I'll make this configurable at some point)

## How it works
The project consists of two components:
- Thread that constantly checks the ProxyFiles folder for new proxies and adds them to the database.
- Thread that picks the least recently updated proxies from the database so that working threads update them.

# TODO
- Add a config option for database settings (host, port, username, password and db name).
- Add a config option for number of threads working on updating the database.
- Add a config option to disable thread that reads new files.
- Add a config option for verbose messages.
- Make thread that reads new files accept different formats (currently it only accepts host:port).
- Create a new optional thread that parses defined pages with lists of proxies.
- Remove code that is not being used.
