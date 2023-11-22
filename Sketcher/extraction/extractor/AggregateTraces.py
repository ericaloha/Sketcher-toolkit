import os

def FindTime(items):
    for item in items:
        if item.find(".")!=-1 and item.find(":")!=-1:
            return item
    return 0
def Aggregate(dir, out):
    # /home/hkc-nfs/NFS_proj/ftrace/trace-origin/new/websrv/30min/web
    files = os.listdir(dir)
    newfiles = []
    for file in files:
        index = file.split(".")[-1]
        if len(index) == 1:
            new_index = '0' + index
            new_file = file.replace(index, new_index)
            newfiles.append(new_file)
        else:
            newfiles.append(file)
        newfiles.sort()
    Output = open(out, "a")
    cur_time = ''
    for file in newfiles:
        #index=file.split(".")[-1]
        #if index[0]=="0":
        #   file=file.replace("0","")
        # print(file)
        if cur_time == '':
            ptr = open(dir + '/' + file, "r")
            for line in ptr.readlines():
                # [002] .... 88879.475495: nfs4_delegreturn_exit: error=0 (OK) dev=00:39 fhandle=0x7a1e648d stateid=1:0x1980e098
                if line.find("[") != -1 and line.find("nfs4") != -1 and line.find("....") != -1:
                    Output.write(line)
                    cur_time= FindTime(line.split(" "))[:-1]
            ptr.close()
        else:
            ptr = open(dir + '/' + file, "r")
            for line in ptr.readlines():
                if line.find("[") != -1 and line.find("nfs4") != -1 and line.find("....") != -1:
                    time=FindTime(line.split(" "))[:-1]
                    if float(time) >float(cur_time):
                        cur_time=time
                        Output.write(line)
                    else:
                        continue
            ptr.close()
        print(file)
    Output.close()
    print('end')



Aggregate("/home/hkc-nfs/NFS_proj/ftrace/trace-origin/new/net/30min/netsrv",
          "/home/hkc-nfs/NFS_proj/ftrace/trace-origin/new/net/30min/netsrv/net.log")
