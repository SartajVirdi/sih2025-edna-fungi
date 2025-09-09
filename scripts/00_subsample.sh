#!/usr/bin/env bash
set -e
# Create demo sub-sample of reads (5k reads) from a larger FASTQ or convert provided FASTA.
INPUT_FASTQ="$1"   # e.g., data/raw_reads.fastq
OUT_FASTQ="data/demo_reads.fastq"
OUT_FASTA="data/demo_reads.fasta"
N=5000

if [ -z "$INPUT_FASTQ" ]; then
  echo "Usage: $0 path/to/input.fastq"
  exit 1
fi

# Use seqtk to subsample
seqtk sample -s42 "$INPUT_FASTQ" $N > "$OUT_FASTQ"
# convert to fasta
seqtk seq -a "$OUT_FASTQ" > "$OUT_FASTA"

echo "Wrote $OUT_FASTQ and $OUT_FASTA"
