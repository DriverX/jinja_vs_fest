import os
import time
from engine import TmplEngineJinja, TmplEngineFest, pyv8
from data import *

test_loops = 1
render_loops = 10**6

def get_mem():
    a = os.popen('ps -p %d -o %s | tail -1' % (os.getpid(),"vsize,rss,pcpu")).read()
    a = a.split()
    return (int(a[0]), int(a[1]))

log_s = "vm-%i, pm-%i"

def begin_mem(name=""):
    print "BEGIN %s: %s" % (name, (log_s % get_mem()))

def end_mem(name=""):
    print "END %s: %s" % (name, (log_s % get_mem()))

#@profile
def engine_jinja():
    return TmplEngineJinja("tmpl/jinja")

#@profile
def template_jinja(engine, name):
    return engine.get_template(name)

#@profile
def render_jinja(tmpl, data):
    return tmpl.render(**data)


#@profile
def engine_fest():
    return TmplEngineFest("tmpl/fest")

#@profile
def template_fest(engine, name):
    return engine.get_template(name)

#@profile
def render_fest(tmpl, data):
    return tmpl.render(**data)

#@profile
def main():
    """
    begin_mem("jinja")
    
    begin_mem("engine")
    engine = engine_jinja()
    end_mem("engine")

    begin_mem("gentmpl")
    template_jinja(engine, "answer_results.tmpl")
    template_jinja(engine, "os.tmpl")
    end_mem("gentmpl")

    begin_mem("render")
    for i in xrange(render_loops):
        template = template_jinja(engine, "answer_results.tmpl")
        html = render_jinja(template, answer_results[0])
        template = template_jinja(engine, "os.tmpl")
        html = render_jinja(template, sg_results[0])
    end_mem("render")

    end_mem("jinja")
    """
    begin_mem("fest")
    
    begin_mem("engine")
    engine = engine_fest()
    end_mem("engine")

    begin_mem("gentmpl")
    template = template_fest(engine, "answer_results.xml")
    template = template_fest(engine, "os.xml")
    end_mem("gentmpl")

    begin_mem("render")
    for i in xrange(render_loops):
        template = template_fest(engine, "answer_results.xml")
        for data in answer_results:
            html = render_fest(template, data)
        template = template_fest(engine, "os.xml")
        for data in sg_results:
            html = render_fest(template, data)
        # html = render_fest(template, sg_results[0])
        if i % 1000 == 0:
            print get_mem()
    end_mem("render")
    
    #print pyv8.JSEngine.collect()
    #del engine
    #del template
    #del html
    end_mem("fest")


if __name__ == "__main__":
    main()

