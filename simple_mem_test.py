import sys
from os import path
import json
import PyV8 as v8
from memory_test import get_mem
from engine import FestHelpers
from data import answer_results

def main():
    #ctx = v8.JSContext(FestHelpers())
    ctx = v8.JSContext()
    for i in xrange(10**6):
        with ctx:
            res = ctx.eval("%i" % i)
        if i % 1000 == 0:
            print get_mem()
    return
    """
    while True:
        i = sys.stdin.readline()
        if i:
            try:
                with ctx:
                    for m in xrange(100):
                        print ctx.eval(i)
                    print get_mem()
            except Exception, e:
                print e
    return
    for i in xrange(10**6):
        with ctx:
            res = ctx.eval("foo = null;")
        if i % 1000 == 0:
            print get_mem()
    return
    """

    with open(path.abspath("fest/lib/compile.js"), "rb") as f:
        compilejs = f.read()
    with ctx:
        ctx.eval(compilejs)
   
    with ctx:
        tmplstr = ctx.eval("compile('%s')" % path.join("tmpl/fest", "answer_results.xml")).decode("utf-8")
        ctx.eval("""
        var __tmpl = function(json) {
                return (%s)(JSON.parse(json));
            };
        """ % (tmplstr))

    for i in xrange(10**6):
        with ctx:
            func = ctx.eval("__tmpl")
            result = func(json.dumps(answer_results[0]))
        if i % 1000 == 0:
            print get_mem()
    

if __name__ == "__main__":
    main()


