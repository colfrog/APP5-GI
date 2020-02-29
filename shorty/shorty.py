class shorty:
    # Dictionary { node: Dictionary { other_node: weight } }
    graph = None

    # High and low paths for the last call to analyze
    # Tuple (list of connections, total weight)
    low = None
    high = None

    # Graph indexes
    start = None
    end = None

    # To define in children
    def analyze(self):
        return None

    def read_graph(self, graph):
        self.graph = graph

    def set_start(self, start):
        self.start = start

    def remove_start(self):
        self.start = None

    def set_end(self, end):
        self.end = end

    def remove_end(self):
        self.end = None

    def shortest(self):
        return low

    def longest(self):
        return high
