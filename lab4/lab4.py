from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False

    # Add your forward checking logic here.
    var = state.get_current_variable()
    value = None
    if var is not None: # we are not in the root state
        if var.is_assigned():
            value = var.get_assigned_value()
            #print 'var', var, 'is assigned to value', value   
            constraints = state.get_constraints_by_name(var.get_name())
            for c in constraints:
                #print 'Considering constraint', c
                other_var_name = c.get_variable_i_name()
                if other_var_name == var.get_name():
                    other_var_name = c.get_variable_j_name()
                other_var = state.get_variable_by_name(other_var_name)
                #print 'other var', other_var
                for y in other_var.get_domain():
                    if not c.check(state, value, y):
                        #print 'constraint', c, 'failed for', value, y, 'remove it from domain'
                        other_var.reduce_domain(y)
                    if other_var.domain_size() == 0:
                        #print 'Domain is empty, return false'
                        return False
            #print 'Evrything was ok, return True'
            return True
        else:
            #print 'var', var, 'is not assigned to any value, return false'
            return True
    else:
        #print 'We  are at root state, return True'
        return True
 # Here value is the value of the variable current being assigned. 
    

# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=True):
    verbose = True
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        if verbose:
            print 'forward_checking returned false, return false'
        return False
    vars = [var for var in state.get_all_variables() if var.domain_size() == 1]
    queue = vars
    visited = []
    while len(queue) > 0:
        var = queue.pop(0)
        visited.append(var)
        var_name = var.get_name()
        value = var.get_domain()[0]
        constraints = state.get_constraints_by_name(var_name)
        for c in constraints:
            other_var_name = c.get_variable_i_name()
            if other_var_name == var.get_name():
                    other_var_name = c.get_variable_j_name()
            other_var = state.get_variable_by_name(other_var_name)
            for y in other_var.get_domain():
                if not c.check(state, value, y):
                    #print 'constraint', c, 'failed for', value, y, 'remove it from domain'
                    other_var.reduce_domain(y)
                if other_var.domain_size() == 0:
                    #print 'Domain is empty, return false'
                    return False
        new_vars = [var for var in state.get_all_variables() if var.domain_size() == 1 and var not in queue and var not in visited]
        queue.extend(new_vars)
    # Add your propagate singleton logic here.
    return True

## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')

#print 'senate people', senate_people[1]
#print 'senate vote', vote_info(senate_votes[1])


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    assert isinstance(list1, list)
    assert isinstance(list2, list)

    dist = 0

    # 'zip' is a Python builtin, documented at
    # <http://www.python.org/doc/lib/built-in-funcs.html>
    sum = 0
    for item1, item2 in zip(list1, list2):
        delta = item1 - item2
        sum += delta*delta
    dist = math.sqrt(sum)
    return dist

edit_distance = euclidean_distance

#Once you have implemented euclidean_distance, you can check the results:
#print evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2, verbose=1)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(euclidean_distance, 5)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
#print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    n_yes = len(yes)
    n_no = len(no)
    n_total = n_yes + n_no
    yes_party = yes
    no_party = no
    groups = set(yes_party+no_party)
    disorder = 0.0
    d = 0.0
    for group in groups:
        count = float(yes_party.count(group))
        if count > 0:
            d = d - count / n_yes * math.log(count / n_yes, 2)
    disorder = disorder + float(n_yes) / n_total * d
    d = 0.0
    for group in groups:
        count = float(no_party.count(group))
        if count > 0:
            d = d - count / n_no * math.log(count / n_no, 2)
    disorder = disorder + float(n_no) / n_total * d
    return disorder

#print CongressIDTree(senate_people, senate_votes, information_disorder)
#print evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2, verbose=1)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print
        
    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)

                                   
## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 45
rep_classified = limited_house_classifier(house_people, house_votes, N_1)

## Find a value of n that classifies at least 90 senators correctly.
N_2 = 135
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 30
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)


## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "1"
WHAT_I_FOUND_INTERESTING = "a"
WHAT_I_FOUND_BORING = "b"


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn

    
