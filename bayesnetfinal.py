"""BayesNet.py

Author: Trevor Buteau

A program that reads in a text file (like those included in the repo) and does ALL of the following:
1. Constructs a Boolean variable Bayesian network from the information in the 
text file;
2. prints out the joint distribution using the network;
3. calculates how many multiplications and additions/subtractions  were needed to calculate 
the joint distribution and prints this number as well as the number of nodes 
in the network;
4. calculates how much space this network saves (compactness) over the 
full joint distribution."""

import itertools
num_adds = 0;

#A function for parsing the complete probability table for a node in the Bayes
#Net, where parents is a list of parents and probs is a list of
#probabilities of parent node states.
def prob_Table(parents, probs):
    num_parents = len(parents)
    num_children = len(parents[1:num_parents])

    #Progress down recursively.
    if num_children-1 > 0:
        full_list = {parents[0] : prob_Table(parents[2:num_parents],probs), \
                     parents[1] : prob_Table(parents[2:num_parents],probs)}
        return full_list
    else:
        full_list = {parents[0] : float(probs.pop(0)), parents[1] : float(probs.pop(0))}
        return full_list
    
#Creates a Bayes Net based on the expected structure of a text file that has
#already been imported as a nested list.
def bayes_build(source):
    bayes_net = {}
    for i in range(0,len(source)):
        if source[i][0] == "END":
            print "Bayesfile read."
            break
        parent_count = 0            #Number of parents this node has

        for j in range(1,len(source[i])):
            if source[i][j][0] != "0":
                parent_count += 1
                
        new_name = source[i][0]
        new_parents = source[i][1:parent_count+1]
        new_probs = source[i][parent_count+1:len(source[i])]
        print "Reading node %s" %new_name

        cpt = []
        
        if new_parents == ['NONE']:
            parent_count = 0
            bayes_net[source[i][0]] = {'parentcount' : parent_count, \
                                        'priorprob' : float(new_probs[0])}
        else: 
            table_parents = new_parents[:]
            table_probs = new_probs
            for i in range(0,len(table_parents)):
                notParents = "n"+table_parents[2*i]
                table_parents.insert((2*i)+1,notParents)
            cpt = prob_Table(table_parents,table_probs)
            bayes_net[new_name] = {'parentcount' : parent_count, \
                                       'parents' : new_parents, \
                                       'probabilities' : cpt}

    print bayes_net
    return bayes_net

#Counts number of probabilities in the Bayes Net.
def count_bprobs(bayes_net):
    total_count = 0;
    for i,j in bayes_net.iteritems():
        if 'prob' in j:
            total_count += 1
    for i,j in bayes_net.iteritems():
        if 'probabilities' in j:
            total_count += 2**j['parentcount']

                
    return total_count

#Prints all possible combinations of boolean variable states in a net:
def bool_combos(nodes):
    t_list, f_list, combined_list = [],[],[]

    t_list = nodes
    f_list = nodes[:]

    for i in range(0,len(nodes)):      #f_list has the "n" complements to the t_list
        f_list[i] = "n" + (nodes[i])

    binary_list = list(itertools.product(["True","False"], repeat=len(nodes)))
    combined_list = []

    for i in range(0,len(binary_list)):
        new_list_item = []
        
        for j in range(0,len(binary_list[i])):
            if binary_list[i][j] == "True":
                new_list_item.append(t_list[j])
            elif binary_list[i][j] == "False":
                new_list_item.append(f_list[j])
        combined_list.append(new_list_item)
    return combined_list

#A function for flattening a node, making probabilities easier to access.
def flatten(mydict):
  new_dict = {}
  for key,value in mydict.items():
    if type(value) == dict:
      _dict = {':'.join([key, _key]):_value for _key, _value in flatten(value).items()}
      new_dict.update(_dict)
    else:
      new_dict[key]=value
  return new_dict

#Extracts/calculates a specific probability value from the Bayes Net
def get_probability(nodes,bayes_net):
    output_nodes = nodes[:] #Save these for output at the end.
    bool_nodes = nodes[:]   #nodes with correct true/false values
    sub_probs = []
    for i in range (0,len(nodes)):
        if nodes[i].startswith("n"):
            nodes[i] = nodes[i][1:]    #Removes 'n' for proper indexing in dictionary
        
        if 'priorprob'  in bayes_net[nodes[i]]:    #No parents, easy index case
            #print bayes_net[nodes[i]]
            if bool_nodes[i].startswith("n"):
                invert_prior = 1 - bayes_net[nodes[i]]['priorprob']
                global num_adds
                num_adds += 1
                sub_probs.append(invert_prior)
            else:
                sub_probs.append(bayes_net[nodes[i]]['priorprob'])
            
        else:                       #1 or more parents, more complicated...
            bool_parents = []
            temp_list_index = 0
            for j in range(0,bayes_net[nodes[i]]['parentcount']):
                if bayes_net[nodes[i]]['parents'][j] in bool_nodes:
                    bool_parents.append(bayes_net[nodes[i]]['parents'][j])
                else:
                    temp_list = bayes_net[nodes[i]]['parents'][:]
                    bool_parents.append("n" + temp_list[temp_list_index])
                temp_list_index += 1
           
            flat_node = flatten(bayes_net[nodes[i]])
            concat = 'probabilities'
            for k in range(0,len(bool_parents)):      #Constructing the final index value
                concat = concat + ":" + bool_parents[k]
            sub_probs.append(flat_node[concat])

    combined_prob = 1
    for x in range(0,len(sub_probs)):
        combined_prob = combined_prob * sub_probs[x]
    output_line = "%s" %(output_nodes) + ", " + "%s" %(combined_prob) 
    print output_line
 
    return combined_prob

#For counting the number of nodes in a Bayes Net with no priors.
def no_priors(bayes_net):
    num_no_priors = 0
    for i in bayes_net.iteritems():
        search  =  i[1]
        if 'priorprob' in search:
            num_no_priors += 1
    return num_no_priors

#For printing the full joint distribution
def full_joint_dist(bayes_net):
    for i in range (0,len(table)):
        get_probability(table[i],new_net)

        



#Main output for the file.

#Creates a nested list object with each line from the source file as
#its own list within the list.

filename = "bayesnets4.txt"

with open(filename,"r") as source_file:
     source = [line.split() for line in source_file]

#Build the net
new_net = bayes_build(source)
new_nodes = new_net.keys()
print new_nodes

#For printing analytics of the net
num_nodes = len(new_net.keys())
joint_dist_size = 2**num_nodes
bnet_probs = float(count_bprobs(new_net))
compactness = bnet_probs/joint_dist_size
num_mults = num_nodes*joint_dist_size
num_adds = 0;


#All possible boolean variable permutations of the nodes in the Bayes Net
table = bool_combos(new_nodes)

#Calculate and print full joint distribution
full_joint_dist(new_net)


print "----------------------------------------------------------------------"
print "File Name                                         : %s" %(filename)
print "Num of lines in joint distribution                : %s" %(joint_dist_size)
print "Num of CPT lines                                  : %s" %(bnet_probs)
print "Compactness of the Bayes Net                      : %s" %(compactness)
print "Num of Nodes in Bayes Net                         : %s" %(num_nodes)
print "Num of Multiplications in Full Joint Dist         : %s" %(num_mults)
print "Num of Additions/Subtractions                     : %s" %(num_adds)
print "----------------------------------------------------------------------"
