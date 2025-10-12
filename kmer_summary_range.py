import os
from collections import Counter
import csv
import sys

def extract_kmers(fastq_file, k):
    kmer_counts = Counter()
    total_reads = 0

    with open(fastq_file, 'r') as f:
        while True:
            header = f.readline()
            if not header:
                break
            seq = f.readline().strip()
            f.readline()  # +
            f.readline()  # quality

            kmer = seq[:k]
            if len(kmer) == k:
                kmer_counts[kmer] += 1
                total_reads += 1

    return kmer_counts, total_reads

def save_to_tsv(kmer_counts, total_reads, output_file):
    with open(output_file, 'w', newline='') as out:
        writer = csv.writer(out, delimiter='\t')
        writer.writerow(['k-mer', 'Count', 'Percentage'])
        for kmer, count in kmer_counts.most_common():
            percent = (count / total_reads) * 100
            writer.writerow([kmer, count, f"{percent:.2f}"])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python kmer_summary_range.py input.fastq")
        sys.exit(1)

    fastq_path = sys.argv[1]
    base_name = os.path.splitext(os.path.basename(fastq_path))[0]
    output_dir = "kmer_results"

    os.makedirs(output_dir, exist_ok=True)

    for k in range(4, 9):  # k = 4 to 8
        print(f"Processing k = {k}")
        counts, total = extract_kmers(fastq_path, k)
        output_filename = f"{base_name}_k{k}_summary.tsv"
        output_path = os.path.join(output_dir, output_filename)
        save_to_tsv(counts, total, output_path)
        print(f"Saved: {output_path}")
