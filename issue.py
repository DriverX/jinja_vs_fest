import os
import PyV8
def get_mem():
    a = os.popen('ps -p %d -o %s | tail -1' % (os.getpid(),"vsize,rss,pcpu")).read()
    a = a.split()
    return (int(a[0]), int(a[1]))

def main():
    ctx = PyV8.JSContext()
    for i in xrange(10**6):
        with ctx:
            res = ctx.eval("%i" % i)
        if i % 1000 == 0:
            print get_mem()

if __name__ == "__main__":
    main()

