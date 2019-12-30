# bloomfilter

"""Bloom filters are space-efficient probabilistic data structures used to test whether an element is a part of a set."""
"""Bloom filters are primarily used in bioinformatics to test the existence of a k-mer in a sequence or set of sequences. """
https://en.wikipedia.org/wiki/Bloom_filters_in_bioinformatics
# how to run?
There is a CLI interface that can be accessed by typing in the following command in your favorite terminal:

""" bloomFilter --ref reference.fasta --query query.fasta --kmer $kmerLength --bloomsize $size """

Reference and query should be fasta files, whereas kmerLength is the length of the sequences to be generated.
Bloomsize is the size of the bit array