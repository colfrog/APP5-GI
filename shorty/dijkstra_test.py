#!/usr/bin/python3

from dijkstra import dijkstra

graph = {
    0: { 1: 1, 2: 3 },
    1: { 0: 1, 2: 1 },
    2: { 0: 3, 1: 1, 3: 1 },
    3: { 2: 1 }
}

d = dijkstra()
d.graph = graph
d.start = 0
d.end = 3

def test(name, given, expected):
    print(name, "given:", given)
    print(name, "expected:", expected)
    assert(given == expected)

test("Analyze", d.analyze(), True)
test("Low", d.low, ([(1, 1), (2, 1), (3, 1)], 3))
test("High", d.high, ([(2, 3), (3, 1)], 4))
