#!/usr/bin/env python
import os, os.path
import gzip
import networkx as nx
import urllib

import jointrw

data_path = 'data/wiki-Talk.txt.gz'

if __name__ == '__main__':
    if not os.path.exists(data_path):
        print "pulling data..."
        d = os.path.dirname(data_path)
        if not os.path.exists(d):
            os.makedirs(d)
        urllib.urlretrieve('http://snap.stanford.edu/data/wiki-Talk.txt.gz',data_path)
    print 'reading data...'
    f = gzip.open(data_path,'r')
    digraph = nx.DiGraph()
    nx.parse_edgelist(f,
                      comments="#",
                      delimiter="\t",
                      nodetype = int,
                      create_using=digraph)
    f.close()
    print 'random walk...'
    jointrw.main(digraph, digraph.order() // 100, also_recip=False)
    
