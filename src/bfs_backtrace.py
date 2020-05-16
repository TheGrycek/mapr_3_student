#!/usr/bin/env python
import rospy as rp
from grid_map import GridMap


class BFS(GridMap):
    def __init__(self):
        super(BFS, self).__init__()
        self.prev = [[(0, 0) for i in range(self.map.info.height)] for j in range(self.map.info.width)]

    def search(self):
       bord = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        vis = []
        queue = [self.start]

        while (len(queue) > 0):
            vis_b = False

            while (vis_b == False):

                if(queue[0] not in vis):
                    vis_b = True
                    c_node = queue[0]
                else:
                    queue.pop(0)

            vis.append(c_node)
            r = c_node[0]
            c = c_node[1]
            self.map.data[c + r * self.map.info.width] = 50  # ustawienie węzła jako odwiedzony
            if (c_node == self.end):
                break

            for b in bord:
                if self.map.data[c + b[0] + (r + b[1]) * self.map.info.width] < 50:
                    queue.append((r + b[1], c + b[0]))
                    self.prev[r + b[1]][c + b[0]] = c_node

            queue.pop(0)
            self.publish_visited()

        start_r = False
        path = []
        c_node = self.end
        path.append(c_node)

        while (start_r == False):
            r = c_node[0]
            c = c_node[1]
            c_node = self.prev[r][c]
            path.append(c_node)
            if (c_node == self.start):
                start_r = True

        self.publish_path(path)
        self.publish_visited()


if __name__ == '__main__':
    bfs = BFS()
    bfs.search()
