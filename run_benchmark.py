# -*- coding: utf-8 -*-
"""
    run_benchmark
    ~~~~~~~~~~~~~

    Command line runner for Python serializers benchmark

    :copyright: (c) 2014 by sc AmvTek srl
    :email: devel@amvtek.com
"""

import sys, argparse
from timeit import timeit


from benchmarks import build_benchmark
import utils

FRAMEWORKS = [
    ('json', utils.is_json_available),
    ('sjson', utils.is_sjson_available),
    ('ujson', utils.is_ujson_available),
    ('msgpack', utils.is_msgpack_available),
    ('protobuf/py', utils.is_protobuf_available),
    ('thrift/py', utils.is_thrift_available),
    ('protobuf/pyext', utils.is_protobuf_available),
    ('thrift/pyext', utils.is_thrift_available),
    ('pycapnp', utils.is_pycapnp_available),
]

class ProcessCrash(RuntimeError):
    pass

def parse_command_line():
    "read and parse command line"

    supported = [t[0] for t in FRAMEWORKS]
    
    def size(v):
        v = int(v)
        if v <= 0:
            raise ValueError("can not be <= 0")
        return v

    parser = argparse.ArgumentParser(
        description="Compare Python performance of Serialization frameworks"
        )

    parser.add_argument(
            "-m","--messages", metavar="MSG", nargs='*',
            help="list message class to benchmark (default all %(default)s)",
            default=['NumStuff','StringStuff','ComboStuff','ComboBunch'],
            choices=['NumStuff','StringStuff','ComboStuff','ComboBunch'],
            )

    parser.add_argument(
            "-f","--frameworks",metavar="FRMW", nargs='*',
            help="list framework to benchmark (default all %(default)s)",
            default=supported,
            choices=supported,
            )

    parser.add_argument(
            "-s","--string_size",metavar="BS",dest="bs",
            help="size of string fields (default: %(default)i)",
            type=size, default=64,
            )

    parser.add_argument(
            "-l","--list_size",metavar="L1",dest="l1",
            help="size of list fields in *Stuff msg (default: %(default)i)",
            type=size, default=4,
            )

    parser.add_argument(
            "-b","--bunch_list_size",metavar="L2",dest="l2",
            help="size of list fields in ComboBunch msg (default: %(default)i)",
            type=size, default=32,
            )

    parser.add_argument(
            "-n", "--sample_size", metavar="NS", dest="ns",
            help="benchmark sample size (default: %(default)i)",
            type=size, default=128,
            )
    
    parser.add_argument(
            "-r", "--timeit_repeat", metavar="TR", dest="nrun",
            help="timeit repetition number (default: %(default)i)",
            type=size, default=128,
            )
    
    parser.add_argument(
            "-o", "--out", metavar="OUT", dest="outpath",
            help="file path where to save report (default: %(default)s)",
            default=None,
            )

    parser.add_argument(
            "--seed", metavar="SEED", dest="seed",
            help="randomization seed (default: %(default)s)",
            default="seed_thrift_vs_proto",
            )

    return parser.parse_args()

# protocol buffers python library relies on environnement variables
# to select pure python or c extension implementation
# once one implementation has been imported it is pretty difficult to import
# another...
# sandboxing each benchmark in its own process was the only way we found to
# reliably control which implementation is used... :(
def proc_run(func, args=None, kwargs=None):
    "run func in a subprocess and return its result"

    args = args or ()
    kwargs = kwargs or {}

    def target_func(pout,args,kwargs):

        rv = func(*args,**kwargs)
        pout.send(rv)

    from multiprocessing import Process, Pipe
    
    pin, pout = Pipe()
    
    proc = Process(target=target_func, args=(pout, args, kwargs))
    proc.start()
    proc.join()

    # check result
    if proc.exitcode == 0:
        # run was successfull
        return pin.recv()
    else:
        raise ProcessCrash()

def list_available_frameworks(frameworks):
    "return list of available frameworks"

    check_frameworks = dict(FRAMEWORKS)
    need_ext = lambda impl:impl.startswith('pyext')
    
    rv = []
    for frm in frameworks :

        # retrieve availability detection function
        detect_func = check_frameworks.get(frm)
        
        if detect_func:

            frm, impl = ("%s/"%frm).split('/')[:2]
            rv.append((frm,impl, detect_func(need_ext(impl))))

    return rv

def get_benchargs(clargs, ctx):
    "return dictionary containing benchmark parameters"

    rv = dict(clargs.__dict__)
    
    for arg in ['messages', 'nrun', 'outpath', 'frameworks']:
        rv.pop(arg, None)

    for arg in ['message', 'target', 'framework', 'implementation']:
        rv[arg] = ctx[arg]

    return rv

def run_benchmark(benchargs, nrun):
    "run a single benchmark returning time per operation ..."
    
    # construct benchmark
    benchmark = build_benchmark(**benchargs)

    # run benchmark
    timed = timeit(stmt=benchmark.run, number=nrun)
    return timed/(1.0*nrun*benchmark.ns), benchmark.framework_version


if __name__ == '__main__':

    # parse command line
    args = parse_command_line()
    
    # prepare reporting
    import reports
    BR = reports.BenchResult
    report = reports.Report()

    # check what frameworks are available on local machine
    frameworks = proc_run(list_available_frameworks, args=(args.frameworks,))

    print report.add_header(args)

    # run each benchmark
    nrun = args.nrun
    results = []
    for message in args.messages:

        for target in ['serialize', 'deserialize']:

            res = []
            
            for framework, implementation, installed in frameworks:

                r = BR(message, target, framework, implementation)

                if installed:

                    try:

                        benchargs = get_benchargs(args, locals())
                        r.opTime, r.version = proc_run(run_benchmark, args=(benchargs,nrun))
                        r.status = BR.SUCCESS

                    except ProcessCrash:

                        r.status = BR.CRASHED

                res.append(r)

            # calculate rank of each result in group defined by message,target
            okres = [ r for r in res if r.status == BR.SUCCESS]
            if okres:
                winner = min(okres,key=lambda r:getattr(r,'opTime'))
                for r in okres:
                    r.rank = r.opTime / winner.opTime
            
            print report.add_result_section(message,target,args,res)

            # save report in a file
            if args.outpath is not None:
                with open(args.outpath,'w') as f:
                    f.write(report.getvalue())
