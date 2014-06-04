#!/usr/bin/env python
import sys
import networkx as nx
import matplotlib.pyplot as plt
import time
import os

import jointrw

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 3:
        print "Usage: er.py n_nodes p prop_steps"
        sys.exit(1)
    n_nodes = int(args[0])
    p = float(args[1])
    prop_steps = float(args[2])

    steps = int(n_nodes * prop_steps)

    results_path = "results/er_%s_%s_%s_%s" % (n_nodes, p, prop_steps, time.time())
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    try:
        digraph = nx.fast_gnp_random_graph(n_nodes, p, directed = True)
        nx.write_edgelist(digraph,
                          "%s/er.csv" % (results_path,),
                          delimiter = ",")
        jointrw.main(digraph,   #graph
                     steps,  #number of steps
                     also_recip=True,
                     plot_path=results_path,
                     title=("\nn=%s, p=%s" % (n_nodes, p) +
                            ", runs=%s, walkers=%s, steps=%s" % (1, 1, steps)))
        plt.show()
    except IndexError:
        import shutil
        print "died because graph not reciprocally connected!"
        shutil.rmtree(results_path)
