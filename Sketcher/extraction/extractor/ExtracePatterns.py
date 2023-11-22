def FindInLine(line, keyword):
    items = line.split(" ")
    for item in items:
        if item.find(keyword) != -1:
            return item


def FindTSInLine(line):
    items = line.split(" ")
    for item in items:
        if item.find(":") != -1 and item.find(".") != -1:
            return item


def CalDist(last_file_path, file_id, a):
    lasts = last_file_path.split(":")
    now = file_id.split(":")
    if lasts[-1].find('/') != -1:
        lasts.append(-1)
    elif now[-1].find('/') != -1:
        now.append(-1)
    if len(lasts) != len(now):
        if len(lasts) > len(now):
            i = 0
            while i < len(lasts) - len(now):
                now.append("0")
        elif len(lasts) < len(now):
            i = 0
            while i < len(now) - len(lasts):
                lasts.append("0")
    i = 0
    dif = []
    while i < len(lasts):
        if lasts[i] != now[i]:
            dif.append(1)
        i += 1
    index = 0
    cnt = len(dif)
    weight = 0
    while index < cnt:
        weight += pow(a, index)
        index += 1
    return weight


def ExtractPattern(fname, patterns):
    f = open(fname, "r")
    fo = open(patterns, "a")
    # collect pattern every 1000 traces
    thres = 1000
    # fo.write('PatID,Wts,Wsi,Wcnt,Wdist,Rts,Rsi,Rcnt,Rdist,Mts,Msi,Mcnt,Mdist\n')
    # a is the factor for distance
    a = 1.5
    cnt = 0
    last_file_path = ""
    last_ts_W = -1
    last_ts_R = -1
    last_ts_M = -1
    cur_ts = -1
    '''
                W       R       M
        time
        size
        count
        dist
    
    '''
    tmpPattern = [
        [0, 0, 0, 0],  # for write
        [0, 0, 0, 0],  # for read
        [0, 0, 0, 0]  # for meta
    ]
    lines = f.readlines()
    line_len = len(lines)
    total_line = 0
    PatID = 0
    for line in lines:
        cnt += 1
        total_line += 1
        if cnt > thres or total_line == line_len - 1:
            last_ts_M = -1
            last_ts_R = -1
            last_ts_W = -1
            print(tmpPattern)
            fo.write(str(PatID) + ",")
            PatID += 1
            for item in tmpPattern:
                for x in item:
                    fo.write(str(x) + ",")
            fo.write("\n")
            tmpPattern = [
                [0.0, 0, 0, 0],  # for write
                [0.0, 0, 0, 0],  # for read
                [0.0, 0, 0, 0]  # for meta
            ]
            cnt = 0
        else:
            ts = FindTSInLine(line)
            if ts != None:
                ts = ts[0:-1]
                cur_ts = float(ts)
            # collect features
            # kworker/u32:9-48936   [005] .... 14224.832198:
            # nfs4_write: error=0 (OK) fileid=00:38:635372
            # fhandle=0x71ed44c6 offset=41943040 count=1048576
            # res=1048576 stateid=1:0x6540decd layoutstateid=0:0x00000000
            if line.find("nfs4_write") != -1:
                # for write
                file_id = FindInLine(line, "fileid")
                if file_id == "":
                    print("break")
                file_id = file_id[7:]
                # 1. for distance
                if last_file_path == "":
                    last_file_path = file_id
                elif last_file_path != file_id:
                    tmpPattern[0][3] += CalDist(last_file_path, file_id, a)
                    last_file_path = file_id
                # 2. for cnts
                tmpPattern[0][2] += 1
                # 3. for size
                tmp_cnt = FindInLine(line, "count")
                tmp_cnt = int(tmp_cnt[6:])
                tmpPattern[0][1] += tmp_cnt
                # 4. for ts
                if last_ts_W == -1:
                    last_ts_W = cur_ts
                else:
                    tmpPattern[0][0] = float(cur_ts) - last_ts_W
            elif line.find("nfs4_read") != -1 and line.find("nfs4_readdir") == -1:
                # for read
                file_id = FindInLine(line, "fileid")
                file_id = file_id[7:]
                # 1. for distance
                if last_file_path == "":
                    last_file_path = file_id
                elif last_file_path != file_id:
                    tmpPattern[1][3] += CalDist(last_file_path, file_id, a)
                    last_file_path = file_id
                # 2. for cnts
                tmpPattern[1][2] += 1
                # 3. for size
                tmp_cnt = FindInLine(line, "count")
                tmp_cnt = int(tmp_cnt[6:])
                tmpPattern[1][1] += tmp_cnt
                # 4. for ts
                if last_ts_R == -1:
                    last_ts_R = cur_ts
                else:
                    tmpPattern[1][0] = float(cur_ts) - last_ts_R
            else:
                # for meta
                # file id
                if line.find("mkdir") != -1 or line.find("name=") != -1:
                    file_id = FindInLine(line, "name=")
                    file_id = file_id.strip("\n")
                    file_id = file_id[5:]
                elif line.find("fileid") != -1:
                    file_id = FindInLine(line, "fileid")
                    file_id = file_id[7:]
                else:
                    file_id = last_file_path
                if file_id == "":
                    print("break2")
                # 1. for distance
                if last_file_path == "":
                    last_file_path = file_id
                elif last_file_path != file_id:
                    tmpPattern[2][3] += CalDist(last_file_path, file_id, a)
                    last_file_path = file_id
                # 2. for cnts
                tmpPattern[2][2] += 1
                # 3. for ts
                if last_ts_M == -1:
                    last_ts_M = cur_ts
                else:
                    tmpPattern[2][0] = float(cur_ts) - last_ts_M
    fo.write(str(PatID) + ",")
    PatID += 1
    for item in tmpPattern:
        for x in item:
            fo.write(str(x) + ",")
    fo.write("\n")
    f.close()
    fo.close()
    return 0


def RemoveNoise(fname, fout):
    f = open(fname, "r")
    fo = open(fout, "a")
    for line in f.readlines():
        if line.find("nfs4_") != -1 and line.find("sequence") == -1 and line.find("nfs4_map") == -1 and line.find(
                "stateid_") == -1 and line.find("xdr_status") == -1:
            fo.write(line)
    f.close()
    fo.close()
    return 0


def DataClean():
    oriFile_1 = "/home/hkc-nfs/NFS_proj/modeling/seq2seq/seq2seq/Traces/Raw/net.log"
    oriFile_2 = "/home/hkc-nfs/NFS_proj/modeling/seq2seq/seq2seq/Traces/Raw/oltp.log"
    oriFile_3 = "/home/hkc-nfs/NFS_proj/modeling/seq2seq/seq2seq/Traces/Raw/video.log"
    #oriFile_4 = "/home/hkc-nfs/NFS_proj/modeling/seq2seq/seq2seq/Traces/Raw/web.log"
    # oriFile_2 = "C:\\Users\\shang\\Desktop\\seq2seq\\seq2seq\\Traces\\Raw\\fileserver.log"
    # oriFile_3 = "C:\\Users\\shang\\Desktop\\seq2seq\\seq2seq\\Traces\\Raw\\webserver.log"
    # oriFile_4 = "C:\\Users\\shang\\Desktop\\seq2seq\\seq2seq\\Traces\\Raw\\vamail.log"

    noNosieFile = "/home/hkc-nfs/NFS_proj/modeling/seq2seq/seq2seq/Traces/WithoutNoise/all.csv.log"
    patternsFile = "/home/hkc-nfs/NFS_proj/modeling/seq2seq/seq2seq/Traces/Patterns/all.csv.pat"
    RemoveNoise(oriFile_1, noNosieFile)
    RemoveNoise(oriFile_2, noNosieFile)
    RemoveNoise(oriFile_3, noNosieFile)
    #RemoveNoise(oriFile_4, noNosieFile)
    ExtractPattern(noNosieFile, patternsFile)


def MapPat2Words(pats, Words):
    f = open(pats, "r")
    fo = open(Words, "w")
    datas = []
    lines = f.readlines()
    i = 0
    while i < 12:
        datas.append([])
        i += 1

    for line in lines:
        tmp_line = line.split(",")[1:-1]
        i = 0
        while i < 12:
            datas[i].append(float(tmp_line[i]))
            i += 1
    i = 0
    while i < 12:
        datas[i].sort()
        i += 1
    ranges = []
    i = 0
    while i < 12:
        ranges.append(datas[i][-1] - datas[i][0])
        i += 1
    print(ranges)

    for line in lines:
        tmp_line = line.split(",")[1:-1]
        i = 0
        prefix = ['W', 'R', 'M']
        ops = ['T', 'S', 'C', 'D']
        while i < 12:
            if ranges[i] == 0:
                ranges[i] = 1
            # fo.write(prefix[i // 4] + ops[i % 4] + str(round(float(tmp_line[i]) / ranges[i], 3)) + " ")
            fo.write(ops[i % 4] +str(round(float(tmp_line[i]) / ranges[i], 4)) + " ")
            i += 1
        fo.write("\t")

        i = 0
        while i < 12:
            if ranges[i] == 0:
                ranges[i] = 1
            # fo.write(prefix[i // 4] + ops[i % 4] + str(round(float(tmp_line[i]) / ranges[i], 3)) + " ")
            fo.write(ops[i % 4] +str(round(float(tmp_line[i]) / ranges[i], 4)) + " ")
            i += 1
        fo.write("\n")

    f.close()
    fo.close()
    return 0


'''
    
        lines.append(tmp_line)
        # fo.write('PatID 0,Wts1,Wsi2,Wcnt3,Wdist4,Rts5,Rsi6,Rcnt7,Rdist8,Mts9,Msi10,Mcnt11,Mdist12\n')
        tmp_ts_max = max(float(tmp_line[1]), float(tmp_line[5]), float(tmp_line[9]))
        tmp_ts_min = min(float(tmp_line[1]), float(tmp_line[5]), float(tmp_line[9]))
        if tmp_ts_max > ts_MAX:
            ts_MAX = tmp_ts_max
        if tmp_ts_min < ts_MIN:
            ts_MIN = tmp_ts_min

        tmp_size_max = max(float(tmp_line[2]), float(tmp_line[6]), float(tmp_line[10]))
        tmp_size_min = min(float(tmp_line[2]), float(tmp_line[6]), float(tmp_line[10]))
        if tmp_size_max > size_MAX:
            size_MAX = tmp_size_max
        if tmp_size_min < size_MIN:
            size_MIN = tmp_size_min

        tmp_cnt_max = max(float(tmp_line[3]), float(tmp_line[7]), float(tmp_line[11]))
        tmp_cnt_min = min(float(tmp_line[3]), float(tmp_line[7]), float(tmp_line[11]))
        if tmp_cnt_max > cnt_MAX:
            cnt_MAX = tmp_cnt_max
        if tmp_cnt_min < cnt_MIN:
            cnt_MIN = tmp_cnt_min

        tmp_dist_max = max(float(tmp_line[4]), float(tmp_line[8]), float(tmp_line[12]))
        tmp_dist_min = min(float(tmp_line[4]), float(tmp_line[8]), float(tmp_line[12]))
        if tmp_dist_max > dist_MAX:
            dist_MAX = tmp_dist_max
        if tmp_dist_min < dist_MIN:
            dist_MIN = tmp_dist_min

    ts_range = ts_MAX - ts_MIN
    size_range = size_MAX - size_MIN
    cnt_range = cnt_MAX - cnt_MIN
    dist_range = dist_MAX - dist_MIN
    # fo.write("ts_range " + str(ts_range) + "\t" + "size_range " + str(size_range) + "\t" + "cnt_range " + str(cnt_range) + "\t" + "dist_range " + str(dist_range) + "\n")
    for line in lines:
        fo.write("T" + str(round(float(line[1]) / ts_range, 3)) + " ")
        fo.write("S" + str(round(float(line[2]) / size_range, 3)) + " ")
        fo.write("C" + str(round(float(line[3]) / cnt_range, 3)) + " ")
        fo.write("D" + str(round(float(line[4]) / dist_range, 3)) + " ")
        fo.write("T" + str(round(float(line[5]) / ts_range, 3)) + " ")
        fo.write("S" + str(round(float(line[6]) / size_range, 3)) + " ")
        fo.write("C" + str(round(float(line[7]) / cnt_range, 3)) + " ")
        fo.write("D" + str(round(float(line[8]) / dist_range, 3)) + " ")
        fo.write("T" + str(round(float(line[9]) / ts_range, 3)) + " ")
        fo.write("S" + str(round(float(line[10]) / size_range, 3)) + " ")
        fo.write("C" + str(round(float(line[11]) / cnt_range, 3)) + " ")
        fo.write("D" + str(round(float(line[12]) / dist_range, 3)) + "\t")
        fo.write("T" + str(round(float(line[1]) / ts_range, 3)) + " ")
        fo.write("S" + str(round(float(line[2]) / size_range, 3)) + " ")
        fo.write("C" + str(round(float(line[3]) / cnt_range, 3)) + " ")
        fo.write("D" + str(round(float(line[4]) / dist_range, 3)) + " ")
        fo.write("T" + str(round(float(line[5]) / ts_range, 3)) + " ")
        fo.write("S" + str(round(float(line[6]) / size_range, 3)) + " ")
        fo.write("C" + str(round(float(line[7]) / cnt_range, 3)) + " ")
        fo.write("D" + str(round(float(line[8]) / dist_range, 3)) + " ")
        fo.write("T" + str(round(float(line[9]) / ts_range, 3)) + " ")
        fo.write("S" + str(round(float(line[10]) / size_range, 3)) + " ")
        fo.write("C" + str(round(float(line[11]) / cnt_range, 3)) + " ")
        fo.write("D" + str(round(float(line[12]) / dist_range, 3)) + "\n")
    f.close()
    fo.close()
'''


def RunConvert():
    oriPat = "/home/hkc-nfs/NFS_proj/modeling/seq2seq/seq2seq/Traces/Patterns/all.csv.pat"
    NormalizedPat = "/home/hkc-nfs/NFS_proj/modeling/seq2seq/seq2seq/NormalizedPat/allTRAIN.csv"
    MapPat2Words(oriPat, NormalizedPat)
    return 0


if __name__ == "__main__":
    print('start')
    DataClean()
    print('end')
    print('start')
    RunConvert()
    print('end')
