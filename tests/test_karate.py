# coding=utf-8
'''
Run the graph embedding methods on Karate graph and evaluate them on
graph reconstruction and visualization. Please copy the
gem/data/karate.edgelist to the working directory
'''
import os

import matplotlib.pyplot as plt
from time import time

from gem.utils import graph_util, plot_util
from gem.evaluation import visualize_embedding as viz
from gem.evaluation import evaluate_graph_reconstruction as gr

from gem.embedding.gf import GraphFactorization
from gem.embedding.hope import HOPE
from gem.embedding.lap import LaplacianEigenmaps
from gem.embedding.lle import LocallyLinearEmbedding
from gem.embedding.node2vec import node2vec
from gem.embedding.sdne import SDNE
import numpy as np

edge_path = "/home/cary/Documents/Data/CloneData/edge"
embedding_path = "/home/cary/Documents/Data/CloneData/embedding"

edge_dirs = os.listdir(edge_path)
for edge_dir in edge_dirs:
    embedding_dir = os.path.join(embedding_path, edge_dir)

    if not os.path.exists(embedding_dir):
        os.mkdir(embedding_dir)

    edge_dir = os.path.join(edge_path, edge_dir)
    edge_files = os.listdir(edge_dir)
    for edge_file in edge_files:
        # File that contains the edges. Format: source target
        # Optionally, you can add weights as third column: source target weight
        # edge_f = 'data/karate.edgelist'
        embedding_file = os.path.join(embedding_dir, edge_file)

        if not os.path.exists(embedding_file):
            os.mkdir(embedding_file)

        edge_file_dir = os.path.join(edge_dir, edge_file)
        for tmp in os.listdir(edge_file_dir):

            edge_f = os.path.join(edge_file_dir, tmp)

            # if edge_f.__contains__("71/2403/8963027.edgelist") or \
            #         edge_f.__contains__("71/2281/8951281.edgelist") or \
            #         edge_f.__contains__("71/2281/8951162.edgelist"):
            #     continue

            # Specify whether the edges are directed
            isDirected = True

            # Load graph
            G = graph_util.loadGraphFromEdgeListTxt(edge_f, directed=isDirected)
            G = G.to_directed()

            models = [HOPE(d=4, beta=0.01)]
            # Load the models you want to run
            # models.append(GraphFactorization(d=2, max_iter=50000, eta=1 * 10 ** -4, regu=1.0))
            # models.append(LaplacianEigenmaps(d=2))
            # models.append(LocallyLinearEmbedding(d=2))
            # models.append(node2vec(d=2, max_iter=1, walk_len=80, num_walks=10, con_size=10, ret_p=1, inout_p=1))
            # models.append(SDNE(d=2, beta=5, alpha=1e-5, nu1=1e-6, nu2=1e-6, K=3, n_units=[50, 15, ], rho=0.3, n_iter=50, xeta=0.01,
            #                    n_batch=100,
            #                    modelfile=['enc_model.json', 'dec_model.json'],
            #                    weightfile=['enc_weights.hdf5', 'dec_weights.hdf5']))

            # For each model, learn the embedding and evaluate on graph reconstruction and visualization

            for embedding in models:
                # print ('Num nodes: %d, num edges: %d' % (G.number_of_nodes(), G.number_of_edges()))
                t1 = time()
                # Learn embedding - accepts a networkx graph or file with edge list
                Y, t = embedding.learn_embedding(graph=G, edge_f=None, is_weighted=True, no_python=True)
                Y_mean = Y.mean(axis=0)

                print edge_f

                f = open(os.path.join(embedding_file, tmp[0: tmp.index(".")] + ".embedding"), 'w')
                f.write(Y_mean.__str__() + "\n")
                f.write(t.__str__() + "\n")
                f.close()

                # print (embedding._method_name + ':\n\tTraining time: %f' % (time() - t1))
                # Evaluate on graph reconstruction
                # MAP, prec_curv, err, err_baseline = gr.evaluateStaticGraphReconstruction(G, embedding, Y, None)
                # ---------------------------------------------------------------------------------
                # print(("\tMAP: {} \t preccision curve: {}\n\n\n\n" + '-' * 100).format(MAP, prec_curv[:5]))
                # ---------------------------------------------------------------------------------
                # Visualize
                # viz.plot_embedding2D(embedding.get_embedding(), di_graph=G, node_colors=None)
                # plt.show()
                # plt.clf()
