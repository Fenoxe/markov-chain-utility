import random
import matplotlib.pyplot as plt
import sys

class Node:

    def __init__(self, _p_list=[], _outputs=[], _nodes=[]):
        self.p_list = []
        self.outputs = []
        self.nodes = []

    def add_node(self, node, p, o):
        self.p_list.append(p)
        self.nodes.append(node)
        self.outputs.append(o)

    def __next_index(self):
        r = random.uniform(0, 1)
        for i, p in enumerate(self.p_list):
            if r < p:
                return i
            r -= p
        return -1

    def next_node(self):
        i = self.__next_index()
        out = self.outputs[i]
        node = self.nodes[i]
        return node, out


class MarkovChain:

    def __init__(self, _nodes=[], _start=None, _end=None, _PRINT_OUTPUT=True):
        self.nodes = _nodes
        self.start = _start
        self.end = _end
        self.PRINT_OUTPUT = _PRINT_OUTPUT
        self.last_outputs = []
    
    def set_print_output(self, b):
        assert isinstance(b, bool) 
        self.PRINT_OUTPUT = b

    def add_node(self, node, is_start=False, is_end=False):
        self.nodes.append(node)
        if is_start:
            self.start = node
        if is_end:
            self.end = node
    
    def run(self, max_iters=None):
        assert self.end != None or max_iters != None
        curr_node = self.start
        self.last_outputs = []

        if self.end == None:
            keep_going = lambda: i < max_iters
        elif max_iters == None:
            keep_going = lambda: curr_node != self.end
        else:
            keep_going = lambda: (i < max_iters) and (curr_node != self.end)

        i = 0

        while keep_going():
            curr_node, out = curr_node.next_node()
            if self.PRINT_OUTPUT:
                print(out)
            self.last_outputs.append(out)
            i += 1

    def show_states_graph(self):
        plt.plot(self.last_outputs)
        plt.xlabel('iter num')
        plt.ylabel('state')
        plt.show()


# test case
P = 0.5
M = 100

if len(sys.argv) > 1:
    P = float(sys.argv[1])

if len(sys.argv) > 2:
    M = int(sys.argv[2])

print('running with P={} M={}'.format(P, M))

A = Node()
B = Node()

A.add_node(B, P, 1)
B.add_node(A, P, 0)
A.add_node(A, 1-P, 0)
B.add_node(B, 1-P, 1)

mc = MarkovChain(_nodes=[A,B], _start=A, _PRINT_OUTPUT=False)

mc.run(M)
mc.show_states_graph()

# s = Node()
# blue = Node()
# red = Node()
# e = Node()

# s.add_node(blue, 0.75, 's->b')
# s.add_node(red, 0.25, 's->r')

# blue.add_node(blue, 0.75, 'b->b')
# blue.add_node(e, 0.25, 'b->e')

# red.add_node(e, 0.75, 'r->e')
# red.add_node(red, 0.25, 'r->r')

# mc = MarkovChain(_nodes=[s, blue, red, e], _start=s, _end=e, _PRINT_OUTPUT=False)

# iters = {}

# N = 10000

# for i in range(N):
#     mc.run()
#     l = len(mc.last_outputs)
#     if l not in iters:
#         iters[l] = 0
#     iters[l] += 1
#     if i % 50 == 0:
#         print(i)

# for i, val in sorted(iters.items()):
#     print("P[X={}] = {}".format(i, val/N))
