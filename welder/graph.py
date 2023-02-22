from collections import defaultdict

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.reverse_graph = defaultdict(list)
        self.V = 0
        self.all_nodes = []

    def addEdge(self, node1, node2):
        if node1 not in self.all_nodes:
            self.all_nodes.append(node1)
            self.V += 1

        if node2 not in self.all_nodes:
            self.all_nodes.append(node2)
            self.V += 1

        self.graph[node1].append(node2)
        if node1 not in self.reverse_graph[node2]:
            self.reverse_graph[node2].append(node1)

    class CyclicGraph(Exception): pass

    def bfs(self, node):
        visited = []
        queue = []    
        visited.append(node)
        queue.append(node)
        
        while queue:
            s = queue.pop(0)
            
            for x in self.graph[s]:
                if x not in visited:
                    visited.append(x)
                    queue.append(x)
                    
        return visited

    def topologicalSort(self):
		
        in_degree = {node: 0 for node in self.all_nodes}
		
        # init in_degree
        for i in self.graph: # O(V + E)
            for j in self.graph[i]:
                in_degree[j] += 1

        queue = [] # all vertices with indegree 0
        for i in self.all_nodes:
            if in_degree[i] == 0:
                queue.append(i)

        visited_vertices = 0
        top_order = [] # result of topological search

        while queue:

            u = queue.pop(0)
            top_order.append(u)

            for i in self.graph[u]:
                in_degree[i] -= 1
                if in_degree[i] == 0:
                    queue.append(i)

            visited_vertices += 1

        if visited_vertices != self.V:
            raise Graph.CyclicGraph('Graph cannot be cyclic')
        else :
            return top_order