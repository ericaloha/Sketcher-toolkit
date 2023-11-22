import os

import libnfs


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from parser import ParseNFS_Trace


def print_hi(name):
    os.system("trace-cmd clear")
    os.system("echo 1 > /tracing/tracing_on")
    #os.system("echo function > /tracing/current_tracer")
    os.system("echo 0 > /tracing/events/enable")
    os.system("echo 1 > /tracing/events/nfs4/enable")
    #os.system("echo 0 > /tracing/events/nfs/enable")
    os.system("echo 'START of TEST: hkc' > /tracing/trace_marker")
    nfs = libnfs.NFS("nfs://137.189.89.102/home/hkc/newNFS_/")
    os.system("echo 'hkc test' > /tracing/trace_marker")
    a = nfs.open('/foo-test', mode='w+')
    os.system("echo 'hkc test' > /tracing/trace_marker")
    a.write("Test string")
    os.system("echo 'hkc test' > /tracing/trace_marker")
    a.close()
    os.system("echo 'hkc test' > /tracing/trace_marker")
    print(nfs.stat("/"))
    os.system("echo 'hkc test' > /tracing/trace_marker")
    nfs.mkdir("/hkc/1233")
    os.system("echo 'hkc test' > /tracing/trace_marker")
    print(nfs.listdir("/hkc"))
    os.system("echo 'hkc test' > /tracing/trace_marker")
    os.system("echo 'END of TEST: hkc ' > /tracing/trace_marker")
    os.system("echo 0 > /tracing/events/nfs4/enable")
    os.system("echo 0 > /tracing/tracing_on")
    #os.system("/tracing/trace >> /home/hkc-nfs/test.log")


# Press the green button in the gutter to run the script.



if __name__ == '__main__':
    print_hi('PyCharm')
    trace="/home/hkc-nfs/NFS_proj/ftrace/trace-origin/video/myvdo.log"
    #ParseNFS_Trace(trace)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
