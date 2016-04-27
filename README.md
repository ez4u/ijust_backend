# ijust
---------------------

An acm judge ...


### Installation:
After cloning, run these commands to install requirements and then create database.

	sudo apt-get install redis-server
	sudo apt-get install libcurl4-openssl-dev

	python script.py -u

### Create database:

	python script.py -crdb

### Drop database:

	python script.py -drdb

### Run server:

    python script.py -r

### Test:
Run server before test.

    python script.py --test-all
    python script.py --test-one api_1.user


### Apidoc url:

	/apidocs/index.html

