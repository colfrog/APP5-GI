from shorty import shorty

class dijkstra(shorty):
    def analyze(self):
        if self.start is None or self.graph is None:
            return False

        # Initialise priority queue
        low = None
        high = None

        # Start by exploring the starting node
        self.low = self.shortest_path(self.start)
        self.high = self.longest_path(self.start)
        return True

    def shortest_path(self, node):
        lesser_than = lambda x, y: x < y
        return self.best_path(node, lesser_than)

    def longest_path(self, node):
        bigger_than = lambda x, y: x > y
        return self.best_path(node, bigger_than)

    def best_path(self, node, compare, explored = []):
        if node in explored:
            return None

        paths = []
        best = None
        for (con_node, con_weight) in self.graph[node].items():
            if con_node in explored:
                continue
            if self.end is not None and con_node == self.end:
                return ([(con_node, con_weight)], con_weight)

            best = self.best_path(con_node, compare, explored + [node])
            if best is not None:
                paths.append(([(con_node, con_weight)] + best[0], con_weight + best[1]))

        best = None
        for path in paths:
            if best is None or compare(path[1], best[1]):
                best = path

        return (best)
