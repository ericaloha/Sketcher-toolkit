import random

from treelib import Tree, Node


def initTree():
    tree = Tree()
    return tree


def AddNodes(tree, parentID, nodeID):
    tree.create_node(identifier=nodeID, parent=parentID)
    return tree


def CreateTree(nodescnt):
    tree = initTree()
    nodeID = 1
    all_parents = []
    tree.create_node(identifier=0)
    all_parents.append(0)
    i = 0
    while i < nodescnt:
        seed = random.randint(1, nodescnt)
        par_index = seed % len(all_parents)
        parentID = all_parents[par_index]
        AddNodes(tree, parentID, nodeID)
        all_parents.append(nodeID)
        nodeID += 1
        i += 1
    # tree.show()
    return tree


def EncodeTree(tree):
    par_exist = {}
    encoded = []
    for node_id in tree.expand_tree():
        if tree.nodes[node_id].is_leaf():
            id = node_id
            D = tree.level(id)
            par = tree.parent(id)
            R = 0
            while True:
                R = tree.level(par.identifier)
                if par.identifier not in par_exist.keys():
                    par_exist[par.identifier] = 1
                else:
                    break
                par = tree.parent(par.identifier)
                if par is None:
                    R = 0
                    break
            # print(str(id) + " ==> <R:" + str(R) + " , D:" + str(D) + "> ")
            encoded.append([R, D])

    return encoded


def DecodeNodes(tree, R, D, cur_id):
    start_level = D
    define_level = R
    node_exist = []
    tree.create_node(identifier=0)
    node_exist.append(0)


def DecodeTree(encoded):
    tree = Tree()
    id = 0
    node_exist = []
    tree.create_node(identifier=0)
    node_exist.append(0)
    id += 1
    last_D = 0
    for item in encoded:
        R = item[0]
        D = item[1]
        if last_D > R:
            dif = last_D - R
            while dif > 0:
                node_exist.pop()
                dif -= 1
        while R < D:
            par_id = node_exist[R]
            tree.create_node(identifier=id, parent=par_id)
            node_exist.append(id)
            id += 1
            R += 1
        last_D = D

    return tree


def DefineLocations(tree):
    nameDict = []
    layers = tree.depth()
    i = 0
    while i <= layers:
        nameDict.append([])
        i += 1
    for node_id in tree.expand_tree():
        level = tree.level(node_id)
        offset = len(nameDict[level])
        nameDict[level].append(node_id)
    return nameDict


def CheckTreeLen(strencoded, tree_code):
    codes_now = len(strencoded.split(" "))
    left = tree_code - codes_now
    i = 0
    while i < left:
        strencoded = strencoded + " f"
        i += 1
    return strencoded


def GenerateTreeMapping(Trees):
    nodecnt = 15
    tree = CreateTree(nodecnt)
    # tree.show()
    encoded = EncodeTree(tree)
    strencoded = ""
    for item in encoded:
        strencoded += "L" + str(item[0]) + "_" + str(item[1]) + " "
    strencoded = strencoded.rstrip(" ")
    tree_code = 15
    strencoded = CheckTreeLen(strencoded, tree_code)
    # print(encoded)
    # print(strencoded)
    tree = DecodeTree(encoded)
    # tree.show()
    name_dict = DefineLocations(tree)
    level = 0
    ios_ = ""
    locas = []
    for item in name_dict:
        # print("level: "+str(level)+" -->"+str(item))
        off = 0
        for it in item:
            # ios_+=str(level)+"_"+str(off)+" "
            locas.append("D_" + str(level) + "_" + str(off))
            off += 1
        level += 1
    pats = 0
    while pats < 1000:
        i = 0
        # size = 50
        size = random.randint(10, 20)
        ios_ += "start "
        while i < size:
            # random.gauss(len(locas)/2, 2)
            index = int(random.randint(0, len(locas) - 1))
            #index = int(random.uniform(0,len(locas)-1))
            if index > len(locas)-1:
                index = len(locas)-1
            ios_ += locas[index] + "_S" + str(int(random.uniform(20, 40))) + " "
            i += 1
        ios_ = ios_.rstrip(" ")
        ios_ += " end\n"
        pats += 1
    # print(ios_)
    # sequence = ios_ + "\t" + strencoded
    Ftree = open(Trees, "a")
    Ftree.write(strencoded + "\n")
    Ftree.close()
    #sequence = strencoded + "\t" + ios_
    sequence = ios_
    print(sequence)
    return sequence


if __name__ == "__main__":
    nameDir = 'C:\\Users\\huang\\Desktop\\Generative\\LSTM_RNN_Single_Pat\\input\\mapping\\'
    index = 3
    Trees = 'C:\\Users\\huang\\Desktop\\Generative\\LSTM_RNN_Single_Pat\\input\\mapping\\TreesRandom.txt'
    while index <= 3:
        fo = open(nameDir + str(index) + ".txt", "w")
        fo.write(GenerateTreeMapping(Trees) + "\n")
        fo.close()
        index += 1
    print(-1)
