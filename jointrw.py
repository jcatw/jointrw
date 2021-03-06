#!/usr/bin/env python

import networkx as nx
import os, os.path
import numpy as np
import random
import matplotlib.pyplot as plt

def label_directed_graph(digraph):
    for node in nx.nodes_iter(digraph):
        digraph.node[node]['in-degree'] = digraph.in_degree(node)
        digraph.node[node]['out-degree'] = digraph.out_degree(node)

def label_undirected_graph(graph):
    for node in nx.nodes_iter(graph):
        graph.node[node]['degree'] = graph.degree(node)
    graph.graph['labeled'] = True

def estimate_joint_dist(graph, nsteps):
    assert(not nx.is_directed(graph))
    assert('labeled' in graph.graph and graph.graph['labeled'])

    n = nsteps  #total num seen
    n_iod = {}  #total seen with indeg i, outdeg o, deg d

    # random initial node; don't include in estimator
    node = random.choice(graph.nodes())
    
    # rw
    for i in xrange(nsteps):
        node = random.choice(list(nx.all_neighbors(graph, node)))
        iod_tuple = (graph.node[node]['in-degree'],
                     graph.node[node]['out-degree'],
                     graph.node[node]['degree'])
        n_iod[iod_tuple] = n_iod.get(iod_tuple,0) + 1

    # degree distribution parameters
    max_indeg  = max([graph.node[k]['in-degree'] for k in graph.node.keys()])
    max_outdeg = max([graph.node[k]['out-degree'] for k in graph.node.keys()])
    deg_par = np.zeros((max_indeg + 1, max_outdeg + 1))

    for (indeg, outdeg, deg) in n_iod.keys():
        val = n_iod[(indeg, outdeg, deg)]
        deg_par[indeg, outdeg] += float(val) / float(n * deg)
        #deg_par[indeg, outdeg] += float(val) / float(deg)

    # normalize
    deg_par /= deg_par.sum()

    np.savetxt("deg_par.csv", deg_par, delimiter=",")

    return deg_par

def pdf_to_ccdf(pdf):
    ccdf = np.zeros(len(pdf))
    ccdf[0] = 1.0
    for i in xrange(1,len(pdf)):
        ccdf[i] = ccdf[i-1] - pdf[i-1]
    return ccdf

def plot_marginals(deg_par, graph, title="", plot_path="results/default"):
    max_indeg  = max([graph.node[k]['in-degree'] for k in graph.node.keys()])
    max_outdeg = max([graph.node[k]['out-degree'] for k in graph.node.keys()])

    fig = plt.figure()

    # marginal in-degree
    x_indeg = np.arange(max_indeg+1)
    est_indeg = deg_par.sum(1)
    true_indeg = np.zeros(max_indeg+1)
    for node in graph.node.keys():
        true_indeg[graph.node[node]['in-degree']] += 1. / graph.order()
    plt.subplot(1, 2, 1)
    plt.plot( np.log10(x_indeg+1), np.log10(pdf_to_ccdf(true_indeg)), 'k-',
              np.log10(x_indeg+1), np.log10(pdf_to_ccdf(est_indeg)) , 'kx--')
    
    plt.xlabel('log(1 + in-degree)')
    plt.ylabel('log(ccdf)')

    # marginal out-degree
    x_outdeg = np.arange(max_outdeg + 1)
    est_outdeg = deg_par.sum(0)
    true_outdeg = np.zeros(max_outdeg+1)
    for node in graph.node.keys():
        true_outdeg[graph.node[node]['out-degree']] += 1. / graph.order()
    plt.subplot(1, 2, 2)
    plt.plot( np.log10(x_outdeg+1), np.log10(pdf_to_ccdf(true_outdeg)), 'k-',
              np.log10(x_outdeg+1), np.log10(pdf_to_ccdf(est_outdeg)) , 'kx--')
    plt.xlabel('log(1 + out-degree)')

    if title == "":
        plt.suptitle("Marginal Distributions")
    else:
        plt.suptitle("Marginal Distributions: %s" % (title),)

    if not os.path.exists(plot_path):
        os.makedirs(plot_path)
    plt.savefig('%s/marginal_%s.pdf' % (plot_path,title.replace(' ','').replace('\n',',')))

    return fig

def main(digraph, nsteps, also_recip=False, plot_path='results/default', title=""):
    orig_title = title
    # construct the directed graph
    label_directed_graph(digraph)

    if also_recip:
        things = [False, True]
    else:
        things = [False]
    
    for recip in things:
        title = orig_title
        graph = digraph.to_undirected(reciprocal = recip)
        label_undirected_graph(graph)

        # estimate the degree distribution
        deg_par = estimate_joint_dist(graph, nsteps)
        
        # plot the marginals
        if recip:
            title = "Reciprocated" + title
        else:
            title = "Flattened" + title
        plot_marginals(deg_par, graph, title, plot_path)
    print "Results directory: %s" % (plot_path,)

# test        
if __name__ == '__main__':
    main(nx.gnp_random_graph(100, 0.3, directed = True), 100, also_recip=True)
    plt.show()
