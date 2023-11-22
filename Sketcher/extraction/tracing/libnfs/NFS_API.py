import random
import time

import libnfs


def getTarget(items, tar):
    for it in items:
        if it.find(tar) != -1:
            return it
    return -1


def InitNFS_API(path):
    # "nfs://137.189.89.102/home/hkc/newNFS_/"
    nfs = libnfs.NFS(path)
    return nfs


def generateIO(cnt):
    i = 0
    str1 = ""
    while i < int(cnt):
        a = random.randint(0, 9)
        str1 += str(a)
        i += 1
    return str1


def NFS_IO(nfs, ops, pos_, seq, cnt):
    pos = pos_.replace(":", "/")
    dif=0
    if ops.find("write") != -1:
        if seq == 1:
            ptr = nfs.open(pos, 'w+')
            t = time.time()
            sat = int(round(t * 1000))
            ptr.write(generateIO(cnt))
            t = time.time()
            end = int(round(t * 1000))
            dif = end - sat
            f=open("/home/hkc-nfs/writedif.log","a")
            f.write(str(dif)+" ")
            f.close()
        else:
            ptr = nfs.open(pos, 'a')
            t = time.time()
            sat = int(round(t * 1000))
            ptr.write(generateIO(cnt))
            t = time.time()
            end = int(round(t * 1000))
            dif = end - sat
            f=open("/home/hkc-nfs/writedif.log","a")
            f.write(str(dif)+" ")
            f.close()
    else:
        ptr = nfs.open(pos, "r")
        t = time.time()
        sat = int(round(t * 1000))
        ptr.read(cnt)
        t = time.time()
        end = int(round(t * 1000))
        dif=end-sat
        f = open("/home/hkc-nfs/readdif.log", "a")
        f.write(str(dif) + " ")
        f.close()
    return 1


def NFS_mkdir(nfs, pos):
    dirs = pos.split(":")[:-1]
    init_dir = "/"
    for dir in dirs:
        candidates = nfs.listdir(init_dir)
        if getTarget(candidates, dir) == -1:
            init_dir += dir
            init_dir += "/"
            nfs.makedirs(init_dir)
        else:
            init_dir += dir
            init_dir += "/"
