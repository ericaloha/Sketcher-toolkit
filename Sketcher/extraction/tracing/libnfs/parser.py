from NFS_API import NFS_IO, InitNFS_API, NFS_mkdir


def getTarget(items, tar):
    for it in items:
        if it.find(tar) != -1:
            return it
    return -1


def parsefsProfile(nfs, pos, fs_profile):
    if pos not in fs_profile.keys():
        fs_profile[pos] = 1
        NFS_mkdir(nfs, pos)
    else:
        fs_profile[pos] = fs_profile[pos] + 1
    return 0


def ParseNFS_Trace(trace):
    # nfs4_write: error=0 (OK) fileid=00:43:219895907 fhandle=0x718864a3 offset=1033650176 count=1048576 res=1048576 stateid=1:0xd90cc667 layoutstateid=0:0x00000000
    #    kworker/u32:1-86477   [006] .... 29722.842227: nfs4_sequence_done: error=0 (OK) session=0x38852311 slot_nr=13 seq_nr=2415 highest_slotid=29 target_highest_slotid=29 status_flags=0 ()
    #     kworker/u32:1-86477   [006] .... 29722.842229: nfs4_read: error=0 (OK) fileid=00:43:219895874 fhandle=0xb613c485 offset=815267840 count=262144 res=262144 stateid=1:0xeed23655 layoutstateid=0:0x00000000
    ft = open(trace, "r")
    line = ft.readline()
    # it is a tree structure
    fs_profile = {}
    files_off = {}
    write_cnt=0
    reaad_cnt=0
    write_size=0
    read_size=0
    write_1=0
    write_1_sizee=0
    nfs = InitNFS_API("nfs://137.189.89.102/home/hkc/newNFS_/")
    flag = 0
    while line:
        items = line.split(" ")
        ops = getTarget(items, "nfs4")
        if ops == -1:
            line = ft.readline()
            continue
        ops = ops.strip(" ")[:-1]
        if ops.find("nfs4_write")!=-1 or ops.find("nfs4_read")!=-1:
            pos = getTarget(items, "fileid")[7:]
            #parsefsProfile(nfs, pos, fs_profile)
            off = getTarget(items, "offset")[7:]
            cnt = getTarget(items, "count")[6:]
            seq = 0
            if ops == "nfs4_write":
                write_cnt+=1
                write_size+=int(cnt)
                if pos not in files_off.keys():
                    files_off[pos] = int(cnt)
                    seq = 1
                else:
                    if files_off[pos] == int(off):
                        seq = 1
                files_off[pos] = off + cnt
                NFS_IO(nfs, ops, pos, seq, cnt)
            else:
                write_1+=1
                write_1_sizee+=int(cnt)
                read_size+=int(cnt)
                reaad_cnt+=1
                NFS_IO(nfs, ops, pos, seq, cnt)

        line = ft.readline()

    ft.close()
    print(write_cnt)
    print(write_size/1024/1024)
    print(reaad_cnt)
    print(read_size/1024/1024)
    print(write_1)
    print(write_1_sizee/1024/1024)