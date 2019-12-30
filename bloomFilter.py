from typing import List
from bfilter import BloomFilter
from hashes import FNV, DJB2, Jenkins
import argparse


class Fasta:
    """
    Simple class to store fasta-formatted sequences
    """

    def __init__(self, header, seq):
        self.header = header
        self.seq = seq

    def __str__(self):
        return self.seq


def read_fasta(filename: str) -> List[Fasta]:
    """
    Reads a FASTA file
    """
    with open(filename, "r") as file:

        sequences = []
        header = ''
        seq = ''

        line = file.readline()
        while line:
            line = line.strip()

            # if a new sequences found
            if line.startswith('>'):

                # add the previous sequence if present
                if seq != '':
                    sequences.append(Fasta(header, seq))

                # start a new sequence
                header = line[1:]
                seq = ''
            else:
                # sequence can be on multiple lines
                seq += line

            line = file.readline()

        # add the last sequence
        if seq != '':
            sequences.append(Fasta(header, seq))

        return sequences


def generate_sequences(fasta: Fasta, length: int) -> List[str]:
    """
    Generates all possible k-mers from a given sequence
    """
    seq = fasta.seq.lower()

    # TODO optimize
    return [seq[i: j] for i in range(len(seq)) for j in range(i + 1, len(seq) + 1) if len(seq[i: j]) is length]


def init_parser():
    """
    Initializes argument parser
    """
    parser = argparse.ArgumentParser(description='Bloom Filter')
    parser.add_argument('--ref', dest='ref', required=True,
                        help='Path to reference FASTA')
    parser.add_argument('--query', dest='query',
                        required=True, help='Path to query FASTA')
    parser.add_argument('--kmer', dest='kmer',
                        required=True, help='k-mer length')
    parser.add_argument('--bloomsize', dest='bloomsize',
                        required=True, help='Bloom Filter length')

    args = parser.parse_args()

    return args


def run():
    """
    Runs CLI commands
    """
    args = init_parser()
    # initialize fasta
    ref = read_fasta(args.ref)[0]
    query = read_fasta(args.query)[0]
    # get arguments regarding size
    kmer_size = int(args.kmer)
    bloomsize = int(args.bloomsize)
    # generate sequences
    ref_sequences = generate_sequences(ref, kmer_size)
    query_sequences = generate_sequences(query, kmer_size)
    # initialize hash functions
    fnv = FNV()
    djb2 = DJB2()
    jenkins = Jenkins()
    # initialize filter
    bloom = BloomFilter(bloomsize, fnv, djb2, jenkins)
    # reference
    ref_count = len(ref_sequences)
    bloom.add_from_list(ref_sequences)
    # query
    query_count = len(query_sequences)
    bloom.check_from_list(query_sequences)
    # found
    found = bloom.found
    # output
    print('Number of (not necessarily distinct) k-mers indexed in reference: {}'.format(ref_count))
    print('Number of (not necessarily distinct) k-mers scanned in query: {}'.format(query_count))
    print('Number of (not necessarily distinct) k-mers from query found in the reference: {}'.format(found))
    # debug
    # print('Bloom: {}'.format(bloom.bit_array))
if __name__ == '__main__':
    run()
