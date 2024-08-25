class Node:
    """
    Node class for the flow network
    """
    def __init__(self):
        self.demand = 0
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)


class RN_Node:
    """
    Node class for the residual network
    Additional attributes:
        visited: A boolean attribute to store if the node has been visited
        corresponding_node: The corresponding node in the flow network
        edge_taken: The edge taken to reach the node
    """
    def __init__(self, node):
        self.visited = False
        self.edges = []
        self.corresponding_node = node
        self.edge_taken = None

    def add_edge(self, edge):
        self.edges.append(edge)


class ShiftNode(Node):
    """
    Shift node class for the flow network
    """
    def __init__(self, company, day, shift, req):
        super().__init__()
        self.company = company
        self.day = day
        self.shift = shift
        self.req = req


class OfficerNode(Node):
    """
    Officer node class for the flow network
    """
    def __init__(self, officer, preferences):
        super().__init__()
        self.officer = officer
        self.preferences = preferences


class AllocationNode(Node):
    """
    Allocation node class for the flow network
    """
    def __init__(self, officer, day):
        super().__init__()
        self.officer = officer
        self.day = day