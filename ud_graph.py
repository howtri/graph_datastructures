# Course: CS261 - Data Structures
# Author: Tristan Howell
# Assignment: Assignment 6: Graph Data Structures
# Description: Implement an undirected graph data structure

import heapq
from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Accepts a str v to add as a new vertex in the graph

        No returns
        """
        if v in self.adj_list:
            return
        self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Accepts two strs representing vertices and links with an edge in each vertex's list

        No returns
        """
        if u == v:
            return

        self.add_vertex(u)
        self.add_vertex(v)
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Accepts two strs representing vertices and removes the edge link in each vertex's list

        No returns
        """
        if v not in self.adj_list or u not in self.adj_list:
            return

        if v not in self.adj_list[u] or u not in self.adj_list[v]:
            return

        self.adj_list[v].remove(u)
        self.adj_list[u].remove(v)

    def remove_vertex(self, v: str) -> None:
        """
        Accepts a str representing a vertex and removes it and all edges linking to it

        No returns
        """
        if v not in self.adj_list:
            return

        while self.adj_list[v]:
            self.remove_edge(v, self.adj_list[v][0])

        self.adj_list.pop(v)

    def get_vertices(self) -> []:
        """
        Accepts no parameters

        Returns list of vertices in the graph (any order)
        """
        return [vertex for vertex in self.adj_list]

    def get_edges(self) -> []:
        """
        Accepts no parameters

        Return list of edges in the graph (any order)
        """
        edge_pairs = []
        processed = []
        for vertex in self.adj_list:
            for edge in self.adj_list[vertex]:
                if edge not in processed:
                    edge_pairs.append((vertex, edge))
            processed.append(vertex)
        return edge_pairs

    def is_valid_path(self, path: []) -> bool:
        """
        Accepts a list path of vertices

        Return true if provided path is valid, False otherwise
        """
        # empty or path of one vertex is valid
        if not path:
            return True

        if len(path) == 1 and path[0] not in self.adj_list:
            return False

        for position in range(len(path) - 1):
            if path[position + 1] not in self.adj_list[path[position]]:
                return False
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Accepts a start and optional end vertex to perform a dfs on

        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """

        visited = []
        if v_start == v_end:
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
                for neighbor in self.adj_list[cur]:
                    if neighbor not in visited:
                        next_level.append(neighbor)
                next_level.sort()
                # move "lowest" lexicographically sorted values to the top of the stack
                stack += next_level[::-1]
        return visited


    def bfs(self, v_start, v_end=None) -> []:
        """
        Accepts a start and optional end vertex to perform a bfs on

        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        visited = []
        if v_start == v_end:
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
                for neighbor in self.adj_list[cur]:
                    if neighbor not in visited:
                        next_level.append(neighbor)
                next_level.sort()
                # move "lowest" lexicographically sorted values to the top of the stack
                stack = next_level[::-1] + stack
        return visited

    def count_connected_components(self):
        """
        Accepts no parameters

        Return number of connected components in the graph
        """
        components = 0
        vertices = self.get_vertices()
        visited = []
        while len(visited) != len(vertices):
            components += 1
            # we just need to visit all the edges within this component in whatever order
            stack = []

            for i in vertices:
                if i not in visited:
                    # the first value not already seen to find any unattached components
                    start = i
                    break

            stack.append(start)
            while len(stack):
                cur = stack.pop()
                if cur not in visited:
                    visited.append(cur)
                    for neighbor in self.adj_list[cur]:
                        if neighbor not in visited:
                            stack.append(neighbor)
        return components

    def has_cycle(self):
        """
        Accepts no parameters and checks for any loops within the graph

        Returns True if a loop is present, otherwise False
        """
        visited = []
        stack = []

        for vertex in self.adj_list:
            stack.append(vertex)

            while len(stack):
                cur = stack.pop()
                if cur not in visited:
                    visited.append(cur)

                    next_level = []
                    for neighbor in self.adj_list[cur]:
                        next_level.append(neighbor)
                    next_level.sort()
                    # move "lowest" lexicographically sorted values to the top of the stack
                    stack += next_level[::-1]

                if cur in stack:
                    return True

            visited = []
            stack = []

        return False


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
