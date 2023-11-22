import pandas as pd
from matplotlib import pyplot


def ShowInput():
    dataset = pd.read_csv('pats/videoserver.csv', index_col=0, header=0)
    values = dataset.values
    # specify columns to plot

    groups = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    i = 1
    # plot each column
    pyplot.figure()
    for group in groups:
        pyplot.subplot(len(groups), 1, i)
        pyplot.plot(values[:, group])
        pyplot.title(dataset.columns[group + 1], x=1, y=0.2, loc='right')
        i += 1
    pyplot.tight_layout()
    pyplot.show()
    return 0


def trimoutPut():
    fori = open("C:\\Users\\shang\\Desktop\\INPUT_NEW.csv", "r")
    ftested = open("C:\\Users\\shang\\Desktop\\tested.txt", "r")
    lines = []
    for line in fori.readlines():
        tmpline = ''
        line = line.split("\t")[0]
        items = line.split(" ")
        for item in items:
            cnt = item[1:]
            tmpline += str(cnt) + ","
        lines.append(tmpline)

    fori_new = open("C:\\Users\\shang\\Desktop\\INPUT_NEW_Ori.csv", "w")

    fori_new.write("Wts,Wsize,Wcnt,Wdist,Rts,Rsize,Rcnt,Rdist,Mts,Msize,Mcnt,Mdist\n")
    for item in lines:
        fori_new.write(item + "\n")

    fori_new.write("\stoped \n")

    flag = 0
    for line in ftested.readlines():
        line = line.strip("\n")
        items = line.split(" ")[1:-1]
        for item in items:
            item = item[1:]
            fori_new.write(item + ",")
        if flag == 0:
            fori_new.write("\t")
            flag = 1
        else:
            fori_new.write("\n")
            flag = 0

    fori.close()
    fori_new.close()
    ftested.close()
    return 0


def MergeIntoOneRow(fin,fout):
    f=open(fin,"r")
    fo=open(fout,"w")
    flag=0
    for line in f.readlines():
        tmpline=line.strip("\n")
        fo.write(tmpline)
        if flag == 0:
            fo.write(",")
            flag=1
        else:
            fo.write("\n")
            flag=0
    f.close()
    fo.close()
    return 0



if __name__ == "__main__":
    #trimoutPut()
    MergeIntoOneRow("C:\\Users\\shang\\Desktop\\tested111.txt","C:\\Users\\shang\\Desktop\\tested12.txt")
