#!/usr/bin/env python
import sys
import os
import networkx as nx
import matplotlib.pyplot as plt
import time

import jointrw

def generate_krapivsky_networks(dirname,
                                n_nodes = 1000,
                                p = 0.2, 
                                lamb = 3.5, 
                                mu = 1.8,
                                r = 0.2,
                                fname_base = "krapiv"):
    "Generate a set of Krapivsky networks from quicknet."
    run_string = "./quicknet/quicknet/krapivskyrecip -n %d -p %f -l %f -m %f -r %f -e %s/%s.csv"
    this_run_string = run_string % (n_nodes, p, lamb, mu, r, dirname, fname_base)
    print(this_run_string)
    os.system(this_run_string)
    return "%s/%s.csv" % (dirname, fname_base)

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 6:
        print "Usage: krapivsky.py n_nodes p lambda mu r prop_steps"
        sys.exit(1)
    n_nodes = int(args[0])
    p = float(args[1])
    l = float(args[2])
    m = float(args[3])
    r = float(args[4])
    prop_steps = float(args[5])

    steps = int(prop_steps * n_nodes)

    results_path = "results/krapivsky_%s_%s_%s_%s_%s_%s_%s" % (n_nodes, p, l, m, r, prop_steps, time.time())
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    try:
        netpath = generate_krapivsky_networks(results_path,
                                              n_nodes = n_nodes,
                                              p = p,
                                              lamb = l,
                                              mu = m,
                                              r = r,
                                              fname_base = 'krapiv')
        f = open(netpath,'r')
        digraph = nx.DiGraph()
        nx.parse_edgelist(f,
                          comments="#",
                          delimiter=",",
                          nodetype = int,
                          create_using=digraph)
        f.close()
        
        jointrw.main(digraph,
                     steps,
                     also_recip = True,
                     plot_path=results_path,
                     title= ("\nn=%s, p=%s, l=%s, m=%s, r=%s" % (n_nodes, p, l, m, r) +
                             ", runs=%s, walkers=%s, steps=%s" % (1, 1, steps)))
        plt.show()
    except IndexError:
        import shutil
        print "died because graph not reciprocally connected!"
        shutil.rmtree(results_path)

    
    
