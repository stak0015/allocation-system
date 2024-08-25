class Edge:
    """
    Edge class for the flow network
    """
    def __init__(self, start, end, lower_bound, upper_bound):
        self.start = start
        self.end = end
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.flow = 0

    def residual_capacity(self):
        """
        Returns the residual capacity of the edge
        """
        return self.upper_bound - self.flow
    

class RN_Edge:
    """
    Edge class for the residual network
    Additional attributes:
        corresponding_edge: The corresponding edge in the flow network
        type: 0 for forward edge, 1 for backward edge
        compliment_edge: The compliment edge in the residual network (forward/backward edge pair)
    """
    def __init__(self, start, end, value, type, edge):
        self.start = start
        self.end = end
        self.value = value
        self.type = type # 0 for forward edge, 1 for backward edge
        self.corresponding_edge = edge
        self.compliment_edge = None
    
    def set_compliment(self, edge):
        self.compliment_edge = edge

    def update(self, value):
        """
        Updates the flow value of the edge and the corresponding edge in the flow network during path augmentation
        """
        if self.type == 0:
            self.corresponding_edge.flow += value
            self.value = self.corresponding_edge.residual_capacity()
        else:
            self.corresponding_edge.flow -= value
            self.value = self.corresponding_edge.flow