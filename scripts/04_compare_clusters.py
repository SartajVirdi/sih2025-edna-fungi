#!/usr/bin/env python3
import pandas as pd
import sys

blast_file = "results/blast_hits.tsv"   # produced by 02_blast_classify.sh
cluster_file = "results/clustering_results.tsv"
out = "results/cluster_vs_blast_summary.tsv"

# parse blast: consider assigned if pident >= 90
assigned = set()
with open(blast_file) as fh:
    for line in fh:
        parts = line.strip().split("\t")
        if len(parts) < 3: continue
        qid = parts[0]; pident = float(parts[2])
        if pident >= 90.0:
            assigned.add(qid)

df = pd.read_csv(cluster_file, sep="\t")
summary = df.groupby('label').apply(lambda g: pd.Series({
    'n_reads': len(g),
    'n_assigned': sum(1 for id in g['id'] if id in assigned),
    'pct_assigned': 100.0*sum(1 for id in g['id'] if id in assigned)/len(g) if len(g)>0 else 0
}))
summary.to_csv(out, sep="\t")
print("Wrote cluster v blast summary to", out)
print(summary.sort_values('n_reads', ascending=False).head(20))
