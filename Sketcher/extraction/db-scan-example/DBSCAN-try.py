# -*- coding: utf-8 -*-
import math
import random
import matplotlib.pyplot as plt
import sys
from mpl_toolkits.mplot3d import Axes3D

class DBSCAN(object):
    STATUS_UNVISITED = 'unvisited'
    STATUS_VISITED = 'visited'

    STATUS_GROUP = 1
    STATUS_NOGROUP = 0

    data = dict()

    def __init__(self, e, minPts):
        """
        e 最小距离
        minPts 最少样本数量
        """
        self.e = e
        self.minPts = minPts

    def nearby(self, id):
        nearby_points = list()
        for link_id in self.scores[id]:
            if self.scores[id][link_id] <= self.e:
                nearby_points.append(link_id)

        return nearby_points

    def visit_nearby_points(self, points, group):
        for id in points:
            if self.data[id]['is_visited'] == self.STATUS_VISITED \
                    and self.data[id]['is_group'] == self.STATUS_GROUP:
                continue
            self.data[id]['is_visited'] = self.STATUS_VISITED

            if self.data[id]['is_group'] == self.STATUS_NOGROUP:
                group.append(id)
                self.data[id]['is_group'] = self.STATUS_GROUP

            nearby_points = self.nearby(id)
            if len(nearby_points) >= self.minPts:
                self.visit_nearby_points(nearby_points, group)

    def fit(self, data_set, scores):
        self.scores = scores
        groups = list()

        for index, item in enumerate(data_set):
            self.data[index] = {'id': index,
                                'is_visited': self.STATUS_UNVISITED,
                                'is_group': self.STATUS_NOGROUP
                                }

        for id in self.data:
            if self.data[id]['is_visited'] == self.STATUS_VISITED:
                continue

            self.data[id]['is_visited'] = self.STATUS_VISITED
            nearby_points = self.nearby(id)

            if len(nearby_points) >= self.minPts:
                group = list()
                group.append(id)
                self.data[id]['is_group'] = self.STATUS_GROUP
                self.visit_nearby_points(nearby_points, group)
                groups.append(group)

        for id in self.data:
            if self.data[id]['is_group'] == self.STATUS_NOGROUP:
                groups.append([id])

        return groups


def init_data_(num, min, max):
    data = []
    for i in range(num):
        data.append([random.randint(min, max), random.randint(min, max)])

    return data


def init_data(fname):
    data = []
    f = open(fname, "rb")
    str1 = b''
    for line in f.readlines():
        if b'\xef\xbb\xbf' in line:
            str1 = line.replace(b'\xef\xbb\xbf', b'')  # 用replace替换掉'\xef\xbb\xbf'
        else:
            str1 = line
        str1 = str1.strip(b'\n')
        str1 = str1.strip(b'\r').split(b',')
        objs = str1
        data.append([float(objs[0]), float(objs[1]), float(objs[2])])

    f.close()
    return data


def mat_score(data_set):
    score = dict()
    for i in range(len(data_set)):
        score[i] = dict()

    for i in range(len(data_set) - 1):
        j = i + 1
        while j < len(data_set):
            score[i][j] = math.sqrt(
                abs(data_set[i][0] - data_set[j][0]) ** 2 + abs(data_set[i][1] - data_set[j][1]) ** 2 + abs(data_set[i][2] - data_set[j][2]) ** 2)
            score[j][i] = score[i][j]
            j += 1

    return score


def show_cluster(data_set, groups):
    plt.title(u'DBSCAN')
    #mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    mark = ['^r', '+g', 'sb', 'dy', '<k', 'pm', 'or', 'ob', 'og', 'ok',]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    print(len(groups))
    if len(groups) >10:
        print("failed")
        return 0
    for index, group in enumerate(groups):
        for i in group:
            plt.plot(data_set[i][0], data_set[i][1], data_set[i][2], mark[index])
            #plt.plot(data_set[i][0], data_set[i][1], mark[index])

    plt.xlim(-0.5, 1)
    plt.ylim(-0.5, 1)
    plt.ylim(-0.5, 1)
    ax.set_xlabel('Write')
    ax.set_ylabel('Read')
    ax.set_zlabel('File Counts')
    plt.show()


if __name__ == '__main__':
    sys.setrecursionlimit(100000)  # 例如这里设置为十万
    data_set = init_data("C:\\Users\\shang\\Desktop\\trace-3.csv")

    score_mat = mat_score(data_set)

    groups = DBSCAN(0.4, 10).fit(data_set, score_mat)
    show_cluster(data_set, groups)
