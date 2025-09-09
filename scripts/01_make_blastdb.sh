#!/usr/bin/env bash
set -e
REF="data/dump.fasta"
OUTDB="db/ITS_Fungi_DB"

mkdir -p db
makeblastdb -in "$REF" -dbtype nucl -parse_seqids -title ITS_RefSeq_Fungi -out "$OUTDB"

echo "BLAST db created at $OUTDB.*"
