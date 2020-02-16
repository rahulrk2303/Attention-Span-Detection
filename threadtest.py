import threading
import time


def doit(arg):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        print ("working on %s" % arg)
        time.sleep(1)
    print("Stopping %s as you wish." % arg)

def doit2(arg):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        print ("working on %s" % arg)
        time.sleep(1)
    print("Stopping %s as you wish." % arg)


def main():
    t = threading.Thread(target=doit, args=("task1",))
    t2 = threading.Thread(target=doit2, args=("task2",))
    t.start()
    t2.start()
    time.sleep(5)
    t.do_run = False
    t2.do_run = False
    t.join()
    t2.join()

if __name__ == "__main__":
    main()