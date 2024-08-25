# Written by: Shunnosuke Takei
from flow_network import FlowNetwork

def allocate(preferences, officers_per_org, min_shifts, max_shifts):
    """
    Allocates shifts to officers based on their preferences and the number of officers required for each shift in each company
    
    Written by: Shunnosuke Takei

    Approach:
        My approach was to create a flow network for the given inputs, consisting of officer nodes, allocation nodes and shift nodes. Each officer will have 30 allocation nodes, one for each day, which will have edges
        connecting to the shift nodes based on the officer's preferences. The shift nodes will have edges connecting to the sink node based on the number of officers required for each shift in each company. The network
        will also have a source node with edges connecting to the officer nodes based on the minimum and maximum number of shifts an officer can work. Another source node will be created to resolve the demand of the source
        node, which will always be -(total number of shifts required). Next, a residual network is created for the flow network, which will be used to run the Ford Fulkerson algorithm. The Ford Fulkerson algorithm will find
        the maximum flow possible from the source node to the sink node in the network. If the flow is equal to the total number of shifts required, the allocation is valid and will return a list of shifts allocated to each
        officer. Otherwise, the allocation is invalid and will return None.

    Precondition: None
    Postcondition: Allocates shifts to officers based on their preferences and the number of officers required for each shift in each company
    
    Input:
        preferences: A 2D array where each subarray contains the preferences of an officer
        officers_per_org: A 2D array where each subarray contains the number of officers required for each shift in a company
        min_shifts: The minimum number of shifts an officer can work
        max_shifts: The maximum number of shifts an officer can work
    Return:
        A 4D array [i][j][k][l] where i is the officer, j is the company, k is the day, and l is the shift
        The value at [i][j][k][l] is 1 if the officer is allocated to the shift, 0 otherwise
        
    Time complexity:
        Best case analysis: O(M * N^2) where N is the number of officers and M is the number of companies
        Worst case analysis: O(M * N^2) where N is the number of officers and M is the number of companies
    Space complexity:
        Input space analysis: O(N + M) where N is the number of officers and M is the number of companies
        Aux space analysis: O(2(N * M)) = O(N * M) where N is the number of officers and M is the number of companies
    """
    fn = FlowNetwork(preferences, officers_per_org, min_shifts, max_shifts)
    fn.FordFulkerson()
    for node in fn.shift_nodes:
        for day in node:
            for shift in day:
                if shift.req != shift.edges[0].flow:
                    return None
    output = [[]]*len(preferences)
    for i in range(len(preferences)):
        output[i] = [[]]*len(officers_per_org)
        for j in range(len(officers_per_org)):
            output[i][j] = [[]]*30
            for k in range(30):
                output[i][j][k] = [0, 0, 0]
    for allocation in fn.allocation_nodes:
        for day in allocation:
            for edge in day.edges:
                if edge.flow == 1:
                    output[edge.start.officer][edge.end.company][edge.end.day][edge.end.shift] = 1
    return output


if __name__ == "__main__":
    preferences = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    officers_per_org = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    min_shifts = 0
    max_shifts = 30
    allocation = allocate(preferences, officers_per_org, min_shifts, max_shifts)
    print(allocation)