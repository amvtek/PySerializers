# -*- coding: utf-8 -*-
"""
    run_benchmark
    ~~~~~~~~~~~~~

    Command line runner for Protobuf/Thrift benchmark

    :copyright: (c) 2014 by sc AmvTek srl
    :email: devel@amvtek.com
"""

import sys, argparse
from timeit import timeit


from benchmarks import build_benchmark

class ProcessCrash(RuntimeError):
    pass

def parse_command_line():
    "read and parse command line"

    def size(v):
        v = int(v)
        if v <= 0:
            raise ValueError("can not be <= 0")
        return v

    parser = argparse.ArgumentParser(
        description="Compare performance of Thrift & Protobuf serialization"
        )

    parser.add_argument(
            "-m","--messages", metavar="MSG", nargs='*',
            help="list message class to benchmark (default all %(default)s)",
            default=['NumStuff','StringStuff','ComboStuff','ComboBunch'],
            choices=['NumStuff','StringStuff','ComboStuff','ComboBunch'],
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

def list_available_frameworks(verbose=True):
    "return list of available frameworks"

    from utils import is_protobuf_available, is_thrift_available

    need_ext = lambda impl:impl.startswith('pyext')
    
    frameworks = [
            ('protobuf','py',is_protobuf_available),
            ('thrift','py',is_thrift_available),
            ('protobuf','pyext',is_protobuf_available),
            ('thrift','pyext',is_thrift_available),
            ]
    rv = []
    for frm,impl,found in frameworks :
        rv.append((frm,impl,found(need_ext(impl))))

    return rv

def get_benchargs(clargs, ctx):
    "return dictionary containing benchmark parameters"

    rv = dict(clargs.__dict__)
    
    for arg in ['messages', 'nrun', 'outpath']:
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
    return timed/(1.0*nrun*benchmark.ns)


if __name__ == '__main__':

    # parse command line
    args = parse_command_line()
    
    # prepare reporting
    import reports
    BR = reports.BenchResult
    report = reports.Report()

    # check what frameworks are available on local machine
    frameworks = proc_run(list_available_frameworks)

    print report.add_header(args)

    # run each benchmark
    nrun = args.nrun
    results = []
    for message in args.messages:

        for target in ['serialize', 'deserialize']:

            res = []
            
            for framework, implementation,installed in frameworks:

                r = BR(message, target, framework, implementation)

                if installed:

                    try:

                        benchargs = get_benchargs(args, locals())
                        
                        r.opTime = proc_run(run_benchmark, args=(benchargs,nrun))
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
