#################
PbThriftBenchmark
#################

Benchmark Protocol buffer vs Thrift using **Python** 

See some `initial results`_ ...

Installation :
==============

If you are familiar with Python, things shall be pretty straightforward :

* Create a virtualenv **yourenv** targetting Python **2.7**. 
* Install dependencies listed in project `requirements.txt`_.
* Clone this project on your local machine.

Note that the `protocol buffer package`_ that can be installed from PyPI, does not
currently contains the source of the CPP extension package necessary to achieve
good performance.

Running the benchmark :
=======================

* starts your command line shell
* activate newly created environment
* goes into project folder

For help :
    python run_benchmark.py -h

To run with defaults options...:
    python run_benchmark.py

.. _initial results: results.rst

.. _protocol buffer package: https://pypi.python.org/pypi/protobuf/2.5.0

.. _requirements.txt: requirements.txt

