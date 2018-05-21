# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.


def extend_path(path, nodes):
    #nodes.sort()
    #print 'extending', path, 'with', nodes
    paths = []
    for node in nodes:
        if node not in path:
            new_path = path[:]
            new_path.append(node)
            paths.insert(0, new_path)
    return paths

def path_is_solution(path, start, goal):
    return path[0] == start and path[-1] == goal

def bfs(graph, start, goal):
    agenda = [[start]]
    while(len(agenda)>0):
        #print 'agenda:', agenda
        path = agenda.pop(0)
        if path_is_solution(path, start, goal):
            return path
        else:
            extended_paths = extend_path(path, graph.get_connected_nodes(path[-1]))
            for p in extended_paths:
                agenda.append(p)
    return []

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    agenda = [[start]]
    while(len(agenda)>0):
        #Sprint 'agenda:', agenda
        path = agenda.pop(0)
        if path_is_solution(path, start, goal):
            return path
        else:
            extended_paths = extend_path(path, graph.get_connected_nodes(path[-1]))
            for p in extended_paths:
                agenda.insert(0, p)
    return []


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    agenda = [[start]]
    while(len(agenda)>0):
        path = agenda.pop(0)
        if path_is_solution(path, start, goal):
            return path
        extended_paths = extend_path(path, graph.get_connected_nodes(path[-1]))
        extended_paths = sorted(extended_paths, key=lambda n: (graph.get_heuristic(n[-1], goal), n[-1]), reverse=True)
        for p in extended_paths:
            agenda.insert(0, p)
    return []

def best_paths_in_agenda(graph, goal, agenda, count):
    new_agenda = sorted(agenda, key=lambda n: (graph.get_heuristic(n[-1], goal), n[-1]))
    return new_agenda[0:count]

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    #print 'beam_search', graph, start, goal, beam_width
    agenda = [[start]]
    while(len(agenda)>0):
        #print 'agenda:', agenda
        for path in agenda:
            if path_is_solution(path, start, goal):
                return path
        best_in_agenda = best_paths_in_agenda(graph, goal, agenda, beam_width)
        agenda = []
        for path in best_in_agenda:
            agenda += extend_path(path, graph.get_connected_nodes(path[-1]))
    return []

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    length = len(node_names)
    total_length = 0
    if length > 1:
        for i in range(length-1):
            edge = graph.get_edge(node_names[i], node_names[i+1])
            total_length = total_length + edge.length
    return total_length

def pop_shortest_path_from_agenda(graph, agenda, goal):
    path = min(agenda, key=lambda n: (path_length(graph, n), n[-1]))
    agenda.remove(path)
    return path

def pop_potentially_shortest_path_from_agenda(graph, agenda, goal):
    path = min(agenda, key=lambda n: (path_length(graph, n) + graph.get_heuristic(n[-1], goal), n[-1]))
    agenda.remove(path)
    return path

def branch_and_bound(graph, start, goal):
    agenda = [[start]]
    extended_list = []
    while(len(agenda)>0):
        path = pop_shortest_path_from_agenda(graph, agenda, goal)
        if path_is_solution(path, start, goal):
            return path
        elif True or path[-1] not in extended_list:
            extended_list.append(path[-1])
            agenda += extend_path(path, graph.get_connected_nodes(path[-1]))
    return []

def a_star(graph, start, goal):
    agenda = [[start]]
    extended_list = []
    while(len(agenda)>0):
        path = pop_potentially_shortest_path_from_agenda(graph, agenda, goal)
        if path_is_solution(path, start, goal):
            return path
        elif path[-1] not in extended_list:
            extended_list.append(path[-1])
            agenda += extend_path(path, graph.get_connected_nodes(path[-1]))
    return []


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible_node(graph, node, goal):
    path = branch_and_bound(graph, node, goal)
    heuristic = graph.get_heuristic(node, goal)
    if (len(path) > 0 and heuristic > 0):
        return heuristic <= path_length(graph, path)
    else:
        return True

def is_admissible(graph, goal):
    for node in graph.nodes:
        if not is_admissible_node(graph, node, goal):
            return False
    return True

def is_consistent(graph, goal):
    for edge in graph.edges:
        n1 = edge.node1
        n2 = edge.node2
        h1 = graph.get_heuristic(n1, goal)
        h2 = graph.get_heuristic(n2, goal)
        if abs(h1 - h2) > edge.length:
            #print 'graph', graph, 'is not consitent becuase ', edge, "is not consistent", h1, h2
            return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '5'
WHAT_I_FOUND_INTERESTING = 'Everything'
WHAT_I_FOUND_BORING = 'Nothing'
