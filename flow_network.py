from circular_queue import CircularQueue
from edges import *
from nodes import *

class FlowNetwork:
    def __init__(self, preferences, officers_per_org, min_shifts, max_shifts):
        """
        Creates the flow network for the given inputs

        Written by: Shunnosuke Takei

        Precondition: None
        Postcondition: Creates the flow network for the given inputs

        Input:
            preferences: A 2D array where each subarray contains the preferences of an officer
            officers_per_org: A 2D array where each subarray contains the number of officers required for each shift in a company
            min_shifts: The minimum number of shifts an officer can work
            max_shifts: The maximum number of shifts an officer can work
        Return:
            None

        Time complexity:
            Best case analysis: O(N * M) where N is the number of officers and M is the number of companies
            Worst case analysis: O(N * M) where N is the number of officers and M is the number of companies
        Space complexity:
            Input space analysis: O(N + M) where N is the number of officers and M is the number of companies
            Aux space analysis: O(N * M) where N is the number of officers and M is the number of companies
        """
        self.source = Node()
        self.ff_source = Node()
        self.sink = Node()
        self.shift_nodes = []
        self.officer_nodes = []
        self.allocation_nodes = []
        self.size = 0

        # Security officer nodes are stored in a 1D array
        # O(N) where N is the number of officers
        for i in range(len(preferences)):
            node = OfficerNode(i, preferences[i])
            self.officer_nodes.append(node)
            self.size += 1
        
        # Shift nodes are stored in a 3D array [i][j][k] where i is the company, j is the day, and k is the shift
        # O(M) where M is the number of companies
        for i in range(len(officers_per_org)):
            self.shift_nodes.append([])
            for day in range(30):
                self.shift_nodes[i].append([ShiftNode(i, day, 0, officers_per_org[i][0]), ShiftNode(i, day, 1, officers_per_org[i][1]), ShiftNode(i, day, 2, officers_per_org[i][2])])
                self.size += 3

        # Allocation nodes are stored in a 2D array [i][j] where i is the officer and j is the day
        # This allocation node helps determine which shift the officer is allocated to for the day
        # The allocation node is connected to the officer node and the shift node via edges
        # O(N * M) where N is the number of officers and M is the number of companies
        for officer in self.officer_nodes:
            self.allocation_nodes.append([])
            for day in range(30):
                node = AllocationNode(officer.officer, day)
                self.allocation_nodes[officer.officer].append(node)
                self.size += 1
                officer.add_edge(Edge(officer, node, 0, 1))
                for company_shifts in self.shift_nodes:
                    for i in range(len(officer.preferences)):
                        if officer.preferences[i] == 1:
                            node.add_edge(Edge(node, company_shifts[day][i], 0, 1))

        # Connect the shift nodes to the sink node
        # O(M) where M is the number of companies
        total_req = 0
        for company in self.shift_nodes:
            for day in company:
                for shift in day:
                    shift.add_edge(Edge(shift, self.sink, 0, shift.req))
                    total_req += shift.req

        # Decrement the demand of the source node by the total number of shifts required
        self.source.demand -= total_req

        # Connect the source node to the officer nodes
        # O(N) where N is the number of officers
        for officer in self.officer_nodes:
            self.source.add_edge(Edge(self.source, officer, 0, max_shifts - min_shifts))
            officer.demand -= min_shifts
            self.source.demand -= min_shifts
            self.ff_source.add_edge(Edge(self.ff_source, officer, 0, abs(officer.demand)))
        
        # Connect the source node to the new source node which will be used in Ford Fulkerson
        self.ff_source.add_edge(Edge(self.ff_source, self.source, 0, abs(self.source.demand)))


    def residual_network(self):
        """
        Creates the residual network for the flow network

        Precondition: None
        Postcondition: Creates the residual network for the flow network

        Time complexity:
            Best case analysis: O(V + E) where V is the number of vertices and E is the number of edges in the network
            Worst case analysis: O(V + E) where V is the number of vertices and E is the number of edges in the network
        Space complexity:
            Input space analysis: O(1)
            Aux space analysis: O(V + E) where V is the number of vertices and E is the number of edges in the network
        """
        self.rn_ff_source = RN_Node(self.ff_source)
        self.rn_source = RN_Node(self.source)
        self.rn_sink = RN_Node(self.sink)
        self.rn_officer_nodes = []
        self.rn_shift_nodes = []
        self.rn_allocation_nodes = []

        # Copy the nodes from the flow network to the residual network
        for officer in self.officer_nodes:
            node = RN_Node(officer)
            self.rn_officer_nodes.append(node)

        for allocation in self.allocation_nodes:
            self.rn_allocation_nodes.append([])
            for day in allocation:
                node = RN_Node(day)
                self.rn_allocation_nodes[-1].append(node)
        
        for company in self.shift_nodes:
            self.rn_shift_nodes.append([])
            for day in company:
                shifts = []
                for shift in day:
                    node = RN_Node(shift)
                    shifts.append(node)
                self.rn_shift_nodes[-1].append(shifts)

        # Create forward and backward edges for each edge in the flow network
        for edge in self.ff_source.edges:
            end_node = edge.end
            if end_node != self.source:
                forward_edge = RN_Edge(self.rn_ff_source, self.rn_officer_nodes[end_node.officer], edge.residual_capacity(), 0, edge)
                backward_edge = RN_Edge(self.rn_officer_nodes[end_node.officer], self.rn_ff_source, edge.flow, 1, edge)
                forward_edge.set_compliment(backward_edge)
                backward_edge.set_compliment(forward_edge)
                self.rn_ff_source.add_edge(forward_edge)
                self.rn_officer_nodes[end_node.officer].add_edge(backward_edge)

            else:
                forward_edge = RN_Edge(self.rn_ff_source, self.rn_source, edge.residual_capacity(), 0, edge)
                backward_edge = RN_Edge(self.rn_source, self.rn_ff_source, edge.flow, 1, edge)
                forward_edge.set_compliment(backward_edge)
                backward_edge.set_compliment(forward_edge)
                self.rn_ff_source.add_edge(forward_edge)
                self.rn_source.add_edge(backward_edge)
        
        for edge in self.source.edges:
            end_node = edge.end
            forward_edge = RN_Edge(self.rn_source, self.rn_officer_nodes[end_node.officer], edge.residual_capacity(), 0, edge)
            backward_edge = RN_Edge(self.rn_officer_nodes[end_node.officer], self.rn_source, edge.flow, 1, edge)
            forward_edge.set_compliment(backward_edge)
            backward_edge.set_compliment(forward_edge)
            self.rn_source.add_edge(forward_edge)
            self.rn_officer_nodes[end_node.officer].add_edge(backward_edge)
        
        for officer in self.officer_nodes:
            for edge in officer.edges:
                end_node = edge.end
                forward_edge = RN_Edge(self.rn_officer_nodes[officer.officer], self.rn_allocation_nodes[officer.officer][end_node.day], edge.residual_capacity(), 0, edge)
                backward_edge = RN_Edge(self.rn_allocation_nodes[officer.officer][end_node.day], self.rn_officer_nodes[officer.officer], edge.flow, 1, edge)
                forward_edge.set_compliment(backward_edge)
                backward_edge.set_compliment(forward_edge)
                self.rn_officer_nodes[officer.officer].add_edge(forward_edge)
                self.rn_allocation_nodes[officer.officer][end_node.day].add_edge(backward_edge)
   
        for allocation in self.allocation_nodes:
            for day in allocation:
                for edge in day.edges:
                    end_node = edge.end
                    forward_edge = RN_Edge(self.rn_allocation_nodes[edge.start.officer][end_node.day], self.rn_shift_nodes[end_node.company][end_node.day][end_node.shift], edge.residual_capacity(), 0, edge)
                    backward_edge = RN_Edge(self.rn_shift_nodes[end_node.company][end_node.day][end_node.shift], self.rn_allocation_nodes[edge.start.officer][end_node.day], edge.flow, 1, edge)
                    forward_edge.set_compliment(backward_edge)
                    backward_edge.set_compliment(forward_edge)
                    self.rn_allocation_nodes[edge.start.officer][end_node.day].add_edge(forward_edge)
                    self.rn_shift_nodes[end_node.company][end_node.day][end_node.shift].add_edge(backward_edge)

        for company in self.shift_nodes:
            for day in company:
                for shift in day:
                    for edge in shift.edges:
                        forward_edge = RN_Edge(self.rn_shift_nodes[shift.company][shift.day][shift.shift], self.rn_sink, edge.residual_capacity(), 0, edge)
                        backward_edge = RN_Edge(self.rn_sink, self.rn_shift_nodes[shift.company][shift.day][shift.shift], edge.flow, 1, edge)
                        forward_edge.set_compliment(backward_edge)
                        backward_edge.set_compliment(forward_edge)
                        self.rn_shift_nodes[shift.company][shift.day][shift.shift].add_edge(forward_edge)
                        self.rn_sink.add_edge(backward_edge)
    

    def FordFulkerson(self):
        """
        Runs the Ford Fulkerson algorithm on the flow network

        Precondition: None
        Postcondition: Finds the maximum flow from the source node to the sink node in the network

        Time complexity:
            Best case analysis: O(F * E + (V + E)) where F is the maximum flow of the network, V is the number of vertices and E is the number of edges in the network
            Worst case analysis: O(F * E + (V + E)) where F is the maximum flow of the network, V is the number of vertices and E is the number of edges in the network
        Space complexity:
            Input space analysis: O(1)
            Aux space analysis: O(V + E) where V is the number of vertices and E is the number of edges in the network
        """
        # Create the residual network for the flow network
        # O(V + E)
        self.residual_network()

        # Run the Ford Fulkerson algorithm
        # 
        while True:
            # Find an augmenting path in the residual network 
            # If no path to the sink node is found, break the loop
            if not self.PathAugmentation(self.rn_ff_source, self.rn_sink):
                break

            current_node = self.rn_sink
            min_flow = float('inf')
            
            # Find the minimum flow in the augmenting path and update the flow values in both networks
            while current_node != self.rn_ff_source:
                edge = current_node.edge_taken
                min_flow = min(min_flow, edge.value)
                current_node = edge.start
            current_node = self.rn_sink
            while current_node != self.rn_ff_source:
                edge = current_node.edge_taken
                # If the edge is a forward edge increment the flow value, else decrement
                if edge.type == 0:
                    edge.update(min_flow)
                    edge.compliment_edge.value += min_flow
                else:
                    edge.update(min_flow)
                    edge.compliment_edge.update(min_flow)
                current_node = edge.start
            self.reset_visited()


    def PathAugmentation(self, node, sink):
        """
        Finds an augmenting path in the residual network using BFS

        Precondition: None
        Postcondition: Finds the shortest path (or lack thereof) from the start node to end node in the network 

        Input:
            node: The start node of the path
            sink: The end node of the path
        Return:
            True if an augmenting path is found, False otherwise

        Time complexity: 
            Best case analysis: O(V + E) where V is the number of vertices and E is the number of edges in the network
            Worst case analysis: O(V + E) where V is the number of vertices and E is the number of edges in the network
        Space complexity: 
            Input space analysis: O(1)
            Aux space analysis: O(1)
        """
        queue = CircularQueue(self.size)
        node.visited = True
        queue.append(node)
        while queue.length > 0:
            current_node = queue.serve()
            if current_node == sink:
                queue.clear()
                return True
            for edge in current_node.edges:
                if not edge.end.visited:
                    if edge.value > 0:
                        edge.end.visited = True
                        # Update the node to store the edge taken to reach the node
                        edge.end.edge_taken = edge
                        queue.append(edge.end)
        queue.clear()
        return False
    

    def reset_visited(self):
        """
        Resets the visited attribute of all nodes in the residual network

        Time complexity: 
            Best case analysis: O(V) where V is the number of vertices in the network
            Worst case analysis: O(V) where V is the number of vertices in the network 
        Space complexity: 
            Input space analysis: O(1)
            Aux space analysis: O(1)
        """
        self.rn_ff_source.visited = False
        self.rn_source.visited = False
        self.rn_sink.visited = False
        for node in self.rn_officer_nodes:
            node.visited = False
        for allocation in self.rn_allocation_nodes:
            for node in allocation:
                node.visited = False
        for company in self.rn_shift_nodes:
            for day in company:
                for shift in day:
                    shift.visited = False
                        