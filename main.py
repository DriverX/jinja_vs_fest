# -*- coding: utf-8 -*-
import os
from os import path
from pprint import pprint
import json
import timeit
import memory_profiler
from engine import TmplEngineJinja, TmplEngineFest


    

jinja = None
fest = None
data = None

def main():
    global jinja
    global fest
    global data
    
    loops = 100

    # jinja = TmplEngineJinja("tmpl/jinja", use_cache=use_cache)
    # jinja_tmpl = jinja.get_template("test.tmpl")
    # jinja_tmpl.render(data=data)

    # fest = TmplEngineFest("tmpl/fest", use_cache=use_cache)
    # fest_tmpl = fest.get_template("test.xml")
    # fest_tmpl.render(**data)



    for use_cache in (False, True):
        jinja = TmplEngineJinja("tmpl/jinja", use_cache=use_cache)
        fest = TmplEngineFest("tmpl/fest", use_cache=use_cache)
       

        tmplname = "answer_results.tmpl"
        s_build = """
        tmpl = engine.get_template("%s")
        """
        sres_build = "tmpl: %s, gen: %.2f usec/pass"
        setup_build = "from __main__ import jinja as engine"
        stmt = s_build % tmplname
        t = timeit.Timer(stmt, setup_build)
        print sres_build % (tmplname, 10**6 * t.timeit(number=1))


        s = """
        tmpl = engine.get_template("%s")
        tmpl.render(**data)
        """
        sres = "tmpl: %s, cache: %i, %.2f usec/pass"

        stmt = s % tmplname
        setup = "from __main__ import jinja as engine, data"
        from data import answer_results
        for result in answer_results:
            data = result
            t = timeit.Timer(stmt, setup)
            print sres % (tmplname, use_cache, 10**6 * t.timeit(number=loops)/loops)

        tmplname = "answer_results.xml"
        setup_build = "from __main__ import fest as engine"
        stmt = s_build % tmplname
        t = timeit.Timer(stmt, setup_build)
        print sres_build % (tmplname, 10**6 * t.timeit(number=1))

        stmt = s % tmplname
        setup = "from __main__ import fest as engine, data"
        for result in answer_results:
            data = result
            t = timeit.Timer(stmt, setup)
            print sres % (tmplname, use_cache, 10**6 * t.timeit(number=loops)/loops)


if __name__ == "__main__":
    main()


