# openrevman

## Current coverage
[![Coverage Status](https://coveralls.io/repos/github/3like3beer/openrevman/badge.svg?branch=master)](https://coveralls.io/github/3like3beer/openrevman?branch=master)

## Install Dev Env
* Dl PyCharm https://www.jetbrains.com/pycharm/download/
* Dl mini conda https://conda.io/miniconda.html
* Dl git
* git clone repo
* Install conda env :

conda env create -f orm.yml

## TODO

activate openrevman

Then (not in script directory)
* pulp - comes with cbc solver - to be called with solve(pulp.PULP_CBC_CMD()):
pip install pulp

* glpk
sudo apt-get install glpk

* ortools
C:\Users\Maman\Miniconda3>easy_install C:\Users\Maman\Downloads\py3
_ortools-6.3.4431-py3.6-win-amd64.egg


* scipy / optimize



export via 
conda env export > orm.yml
reimport via
conda env create -f orm.yml
* microservice flask
