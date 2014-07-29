# -*- coding: utf-8 -*-
"""
    reports
    ~~~~~~~

    reporting utilities for thrift/protobuf benchmarking...

    :copyright: (c) 2014 by sc AmvTek srl
    :email: devel@amvtek.com
"""

import platform
from datetime import datetime

from benchmarks import __version__
from tabulate import tabulate # see PyPI : tabulate module

BENCHMARK_LOAD_PARAMS = {
        'NumStuff':[('L1','l1')],
        'StringStuff':[('L1','l1'),('BS','bs')],
        'ComboStuff':[('L1','l1'),('BS','bs')],
        'ComboBunch':[('L1','l1'),('BS','bs'),('L2','l2')],
}

class BenchResult(object):

    SUCCESS = "success"

    CRASHED = "crashed"

    status = None

    opTime = None
    
    rank = None

    def __init__(self, message, target, framework, implementation, version=""):

        self.message = message
        self.target = target
        self.framework_name = framework
        self.implementation = implementation
        self.version = version

    def get_framework(self):
        "return library name"

        framework = self.framework_name
        if self.implementation:
            framework = "%s/%s" % (framework, self.implementation)
        if self.version:
            framework = "%s %s" % (framework, self.version)

        return framework
    framework = property(get_framework)

    def as_result_row(self, condensed=True):

        if condensed:

            headAttrs = ['framework']
        else:

            headAttrs = ['message','target','framework']

        rv = []
        for attr in headAttrs:
            rv.append(getattr(self,attr))

        if self.status == self.SUCCESS:

            rv.extend(['OK',fmt_timing_result(self.opTime),"%.2f"%self.rank])

        elif self.status == self.CRASHED:

            rv.extend(['CRASHED','CRASHED','CRASHED'])

        else:

            rv.extend(['NA','-','-'])

        return rv

def fmt_timing_result(value):
    "return string encoding value using optimal time unit"

    value = float(value)
    if value < 0:
        raise ValueError("value can not be < 0")

    # select best unit of time
    for factor, uom in [ (1,'sec'),(1e-3,'ms'),(1e-6,'us'),(1e-9,'ns')]:
        if value >= factor:
            break

    # convert value to best unit of time
    value /= factor

    return "%.2f %s" % (value,uom)

def underline(words, ulc='-', top=False):

    if isinstance(words,(list,tuple)):
        words = " ".join(words)
    words = words.strip()
    line = ulc*len(words)
    if top:
        return "%(line)s\n%(words)s\n%(line)s" % locals()
    return "%(words)s\n%(line)s" % locals()

def get_max_length(strlist):
    "return length of longer string in strlist"

    return max([len(s) for s in strlist])

def fmt_param_list(params):

    fmt = "* %{}s : %s".format(get_max_length([k for k,v in params]))
    buf = []
    for k,v in params:
        line = fmt % (k,v)
        buf.append(line)
    return "\n".join(buf)

def tabulate_results(reslist, condensed=True):

    if condensed:

        headers = ['framework', 'status', 'op_time', 'rank']

    else:

        headers = ['message', 'target', 'framework', 'status', 'op_time', 'rank']

    # extract results
    res = [r.as_result_row(condensed) for r in reslist]

    return tabulate(res, headers, tablefmt='grid')

class Report(object):

    def __init__(self):

        self.buf = []

    def add_header(self,clargs):
        
        # Add report title
        buf = []
        buf.append(underline("Python Serialization Benchmark","#",True))
        buf.append("")

        # check platform
        plat = platform.platform()
        py = "%s/%s" %(platform.python_implementation(),platform.python_version())
        version = "%i.%i.%i" % __version__

        buf.append(fmt_param_list([
            ('Platform',plat),
            ('Python',py),
            ('Benchmark version',version),
            ('Run at',datetime.utcnow()),
            ('Randomization seed', clargs.seed),
            ('Benchmarks sample size', clargs.ns),
            ('Benchmark repeat', clargs.nrun)
            ]))
        buf.append("")

        header = "\n".join(buf)
        self.buf.append(header)

        return header

    def add_result_section(self, message, target, clargs, reslist):

        buf = []

        # add section title
        buf.append(underline((message,target),"="))
        buf.append("")

        # report value of load parameters
        # those parameters if changed will meaningfully change results
        mlp = BENCHMARK_LOAD_PARAMS.get(message)
        if mlp:
            
            params = []
            for name, aname in mlp:
                params.append((name,getattr(clargs,aname)))

            buf.append(fmt_param_list(params))
            buf.append("")

        # tabulate reslist
        buf.append(tabulate_results(reslist))
        buf.append("")

        section = "\n".join(buf)
        self.buf.append(section)

        return section

    def getvalue(self):
        "return full report"

        return "\n".join(self.buf)
