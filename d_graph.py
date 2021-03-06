# Course: CS261 - Data Structures
# Author: Tristan Howell
# Assignment: Assignment 6: Graph Data Structures
# Description: Implement a directed graph data structure

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Create new nested list in the matrix and extend all previous lists as not being an edge of the newest vertex

        Returns the number of vertices in the graph
        """
        # add the newest list
        self.adj_matrix.append([0 for i in range(len(self.adj_matrix))])
        # add a new column to each list including the newest
        for list in self.adj_matrix:
            list.append(0)

        self.v_count += 1
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Accepts two ints representing vertices and adds a weight representing an edge between them

        No returns
        """
        if weight < 0 or src == dst:
            return

        if src >= self.v_count or dst >= self.v_count:
            return

        # src is the list and dst is the index in that list
        self.adj_matrix[src][dst] = weight


    def remove_edge(self, src: int, dst: int) -> None:
        """
        Accepts two ints representing vertices and removes the weight representing an edge between them

        No returns
        """
        if src < 0 or dst < 0:
            return

        if src >= self.v_count or dst >= self.v_count:
            return

        self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        No parameters

        Returns all vertices in the graph
        """
        return list(range(self.v_count))

    def get_edges(self) -> []:
        """
        No parameters

        Returns all edges of the graph represented as the src, dst, and weight
        """
        edges = []
        for outer in range(self.v_count):
            for inner in range(self.v_count):
                if self.adj_matrix[outer][inner]:
                    edges.append((outer, inner, self.adj_matrix[outer][inner]))
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Accepts a path list

        Returns True for a valid path, otherwise False
        """
        if not path:
            return True

        if len(path) == 1 and path[0] not in range(self.v_count):
            return False

        for position in range(len(path)):
            current = self.adj_matrix[path[position]]
            edges = [i for i in range(len(current)) if current[i]]
            # check the next position in the path is a vertex and is connected to the current
            if position + 1 == len(path):
                break
            if path[position + 1] not in range(self.v_count) or path[position + 1] not in edges:
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Accepts a start and optional end vertex to perform a dfs on

        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        visited = []
        if v_start not in range(self.v_count):
            return visited
        # "stack" operations for a list will be pop and append
        # using a list to find the next *smallest vertex to follow
        stack = []
        stack.append(v_start)

        while len(stack):
            cur = stack.pop()
            if cur not in visited:
                visited.append(cur)
                if cur == v_end:
                    # the path when we found the end
                    return visited
                next_level = []
                for neighbor_pos in range(len(self.adj_matrix[cur])):
                    if self.adj_matrix[cur][neighbor_pos] and neighbor_pos not in visited:
                        next_level.append(neighbor_pos)
                next_level.sort()
                # move "lowest" lexicographically sorted values to the top of the stack
                stack += next_level[::-1]
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Accepts a start and optional end vertex to perform a dfs on

        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        visited = []
        if v_start not in range(self.v_count):
            return visited
        # "stack" operations for a list will be pop and insert[0]
        # using a list to find the next *smallest vertex to follow
        stack = []
        stack.append(v_start)

        while len(stack):
            cur = stack.pop()
            if cur not in visited:
                visited.append(cur)
                if cur == v_end:
                    # the path when we found the end
                    return visited
                next_level = []
                for neighbor_pos in range(len(self.adj_matrix[cur])):
                    if self.adj_matrix[cur][neighbor_pos] and neighbor_pos not in visited:
                        next_level.append(neighbor_pos)
                next_level.sort()
                # move "lowest" lexicographically sorted values to the top of the stack
                stack = next_level[::-1] + stack
        return visited

    def has_cycle(self):
        """
        Accepts no parameters and checks for any loops within the graph

        Returns True if a loop is present, otherwise False
        """
        visited = []
        stack = []

        for vertex_pos in range(self.v_count):
            stack.append(vertex_pos)

            while len(stack):
                cur = stack.pop()
                if cur not in visited:
                    visited.append(cur)

                    next_level = []
                    for neighbor_pos in range(len(self.adj_matrix[cur])):
                        if self.adj_matrix[cur][neighbor_pos]:
                            next_level.append(neighbor_pos)
                    next_level.sort()
                    # move "lowest" lexicographically sorted values to the top of the stack
                    stack += next_level[::-1]

                if cur in stack:
                    return True

            visited = []
            stack = []

        return False

    def dijkstra(self, src: int) -> []:
        """
        Accepts an int as the start vertex and uses dijkstras algorithm to determine distances to all nodes, inf if not
        possible

        Returns a list of "distances" (sum of weights)
        """
        visited = {}
        pr_heap = []
        heapq.heappush(pr_heap, (0, src))
        while pr_heap:
            cur = heapq.heappop(pr_heap)
            cur_vert = cur[1]
            cur_dis = cur[0]
            if cur_vert not in visited:
                visited[cur_vert] = cur_dis
                # all neighbors
                for neighbor_pos in range(len(self.adj_matrix[cur_vert])):
                    if self.adj_matrix[cur_vert][neighbor_pos]:
                        # current distance and next to determine overall shortest
                        heapq.heappush(pr_heap, (self.adj_matrix[cur_vert][neighbor_pos] + cur_dis, neighbor_pos))

        # any indexes to the range of v_count not in visited are unreachable, place into index order in list
        distances = []
        for ind in range(self.v_count):
            if ind in visited:
                distances.append(visited[ind])
            else:
                distances.append(float('inf'))

        return distances




if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
