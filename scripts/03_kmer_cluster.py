#!/usr/bin/env python3
import sys
from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import PCA
import umap
import hdbscan
import matplotlib.pyplot as plt
from tqdm import tqdm

# Usage: python 03_kmer_cluster.py data/demo_reads.fasta results/
fasta_path = sys.argv[1] if len(sys.argv) > 1 else "data/demo_reads.fasta"
outdir = sys.argv[2] if len(sys.argv) > 2 else "results"
k = 6

def read_fasta(path):
    ids=[]
    seqs=[]
    with open(path, 'r', encoding='utf-8') as fh:
        id=None; seq=[]
        for line in fh:
            line=line.strip()
            if not line: continue
            if line.startswith('>'):
                if id is not None:
                    ids.append(id); seqs.append(''.join(seq))
                id = line[1:].split()[0]; seq=[]
            else:
                seq.append(line)
        if id is not None:
            ids.append(id); seqs.append(''.join(seq))
    return ids, seqs

def kmer_counts(seq, k):
    seq = seq.upper()
    counts={}
    for i in range(len(seq)-k+1):
        kmer = seq[i:i+k]
        if set(kmer) <= set('ACGTN'):
            counts[kmer] = counts.get(kmer,0)+1
    return counts

ids, seqs = read_fasta(fasta_path)
print("Read", len(ids), "sequences from", fasta_path)

kmer_dicts = []
for s in tqdm(seqs, desc="k-mer counting"):
    kmer_dicts.append(kmer_counts(s,k))

vec = DictVectorizer(sparse=False)
X = vec.fit_transform(kmer_dicts)
row_sums = X.sum(axis=1).reshape(-1,1); row_sums[row_sums==0]=1
X = X / row_sums

pca = PCA(n_components=min(50, X.shape[1]), random_state=42)
Xp = pca.fit_transform(X)

um = umap.UMAP(n_neighbors=15, min_dist=0.1, metric='euclidean', random_state=42)
Xu = um.fit_transform(Xp)

clusterer = hdbscan.HDBSCAN(min_cluster_size=10, min_samples=5)
labels = clusterer.fit_predict(Xu)

import os
os.makedirs(outdir, exist_ok=True)
df = pd.DataFrame({"id":ids, "label":labels, "umap1":Xu[:,0], "umap2":Xu[:,1]})
df.to_csv(outdir + "/clustering_results.tsv", sep="\t", index=False)

plt.figure(figsize=(7,6))
plt.scatter(df.umap1, df.umap2, c=df.label, s=8)
plt.title("UMAP + HDBSCAN clusters (k=%d)"%k)
plt.xlabel("UMAP1"); plt.ylabel("UMAP2")
plt.savefig(outdir + "/umap_clusters.png", dpi=200)
print("Wrote clustering results to", outdir)
