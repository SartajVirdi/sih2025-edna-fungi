#!/usr/bin/env bash
set -e
DB="db/ITS_Fungi_DB"
QUERY="data/demo_reads.fasta"   # or your reads fasta
OUT="results/blast_hits.tsv"
mkdir -p results

# Run blastn (tune evalue, threads as needed)
blastn -query "$QUERY" -db "$DB" -outfmt "6 qseqid sseqid pident length evalue bitscore stitle" -max_target_seqs 5 -evalue 1e-5 -num_threads 4 -out "$OUT"

echo "BLAST results: $OUT"
