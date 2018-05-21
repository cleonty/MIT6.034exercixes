from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

def find_matching_rules(rules, hypothesis):
    matching_rules = []
    for rule in rules:
        consequent = rule.consequent()
        for c in consequent:
            bindings = match(c, hypothesis)
            if bindings != None:
                matching_rules.append(rule)
    return matching_rules

def backchain_to_goal_tree(rules, hypothesis):
#    print 'START backchain_to_goal_tree', hypothesis
    goal_tree = OR()
    matching_rules = find_matching_rules(rules, hypothesis)
    #print "matching rules", matching_rules
    if len(matching_rules) > 0:
        goal_tree.append(hypothesis)
        for rule in matching_rules:
            consequent = rule.consequent()
            antecedent = rule.antecedent()
            
            for c in consequent:
                bindings = match(c, hypothesis)
                if bindings != None:
                    #print "consequent:", c
                    #print "antecedent:", antecedent
                    #print "bindings:", bindings
                    if isinstance(antecedent, (OR, AND)):
                        for i in xrange(len(antecedent)):
                            new_hypothesis = populate(antecedent[i], bindings)
                            #print "new hypothesis", new_hypothesis
                            antecedent[i] = backchain_to_goal_tree(rules, new_hypothesis)
                        goal_tree.append(antecedent)
                    else:
                        new_hypothesis = populate(antecedent, bindings)
                        goal_tree.append(backchain_to_goal_tree(rules, new_hypothesis))
        goal_tree = simplify(goal_tree)
    else:
        goal_tree = hypothesis
    return goal_tree

# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
