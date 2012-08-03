# -*- coding: utf-8 -*-
import os
from os import path
from pprint import pprint
import PyV8 as pyv8
import jinja2
try:
    import simplejson as json
except ImportError:
    import json
import hashlib

print pyv8.JSEngine.version

class JSLocker(pyv8.JSLocker):
    pass


class FestError(pyv8.JSError):
    pass


class FestHelpers(pyv8.JSClass):
    def __init__(self, read_root=None, *args, **kwargs):
        self._read_root = path.abspath(read_path) if read_root is not None else os.getcwd()
        super(FestHelpers, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        if name in ("__dirname", "__fest_error", "__read_file"):
            mapname = "_%s%s" % (self.__class__.__name__, name)
            # print name, mapname, hasattr(self, mapname)
            attr = getattr(self, mapname, None)
        else:
            attr = super(FestHelpers, self).__getattr__(name)
        if attr is not None:
            return attr
        raise AttributeError(name)
    
    __dirname = path.abspath("fest/lib")

    def __fest_error(self, message):
        raise FestError(message)

    def __read_file(self, file, encoding="utf-8"):
        # print file
        filepath = path.join(self._read_root, file)
        f = open(filepath, "rb")
        content = f.read()
        f.close()
        return content


class BaseTmplEngine(object):
    Tmpl = None

    def __init__(self, searchdir, use_cache=True):
        self._searchdir = path.abspath(searchdir)
        self._cache = {}
        self._use_cache = bool(use_cache)

        self.setup()

    def setup(self):
        pass

    def get_template(self, tmplname):
        tmpl = None
        cache = self._cache
        if self._use_cache and tmplname in cache:
            tmpl = cache[tmplname]
        else:
            tmpl = self.Tmpl(self, tmplname)
            if self._use_cache:
                cache[tmplname] = tmpl
        return tmpl


class BaseTmpl(object):
    def __init__(self, engine, name):
        self._engine = engine
        self._name = name
        self._template = self.gen_template()
    
    def gen_template(self):
        return None

    def render(self, **kwargs):
        return u""


class TmplJinja(BaseTmpl):
    def gen_template(self):
        return self._engine._jinja.get_template(self._name)

    def render(self, **kwargs):
        return self._template.render(**kwargs)


class TmplEngineJinja(BaseTmplEngine):
    Tmpl = TmplJinja

    def setup(self):
        loader = jinja2.FileSystemLoader(self._searchdir)
        cache_size = 50 if self._use_cache else 0
        self._jinja = jinja2.Environment(loader=loader, cache_size=cache_size, auto_reload=False)


class TmplFest(BaseTmpl):
    @property
    def context(self):
        if not hasattr(self, "_context"):
            self._context = pyv8.JSContext()
        return self._context
    
    def gen_template(self):
        ret = None
        with JSLocker():
            with self._engine._jsctx as ctx:
                evaljs = "compile('%s')" % path.join(self._engine._searchdir,
                                                     self._name)
                content = ctx.eval(evaljs)
                content = content.decode("utf-8")

                if content:
                    jscons = """(function(json, error_log) {
                        return (%s)(JSON.parse(json));
                    })""" % (content)
        with self.context:
            ret = self.context.eval(jscons)
        return ret

    def render(self, **kwargs):
        result = u""
        
        with JSLocker():
            with self.context as ctx:
                func = self._template
                result = func(json.dumps(kwargs))
        return result
    

class TmplEngineFest(BaseTmplEngine):
    Tmpl = TmplFest

    def setup(self):
        self._jsctx = pyv8.JSContext(FestHelpers())
        with open(path.abspath("fest/lib/compile.js"), "rb") as f:
            compilejs = f.read()
        if compilejs:
            with self._jsctx as ctx:
                ctx.eval(compilejs)



