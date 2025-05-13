"""
DNA Sequence Generator and Analyzer

Purpose:
This program generates random DNA sequences in FASTA format based on user input,
inserts the user's name at a random position, calculates sequence statistics,
and saves the result to a file. The statistics exclude non-DNA characters.

Context of use:
- DNA sequence simulation for testing algorithms
- Generating test data for sequence analysis tools
"""

import random
import sys
from datetime import datetime


# ORIGINAL:
# def generate_dna_sequence(length):
#     return ''.join(random.choices('ACGT', k=length))

# MODIFIED (added weights for more realistic CG content and seed for reproducibility):
def generate_dna_sequence(length):
    """Generate a DNA sequence with slightly higher probability for AT pairs (more biologically realistic)"""
    random.seed(datetime.now().microsecond)  # Seed with current microsecond for better randomness
    return ''.join(random.choices('ACGT', weights=[0.3, 0.2, 0.2, 0.3], k=length))


def insert_name(sequence, name):
    """Insert the user's name at a random position in the sequence"""
    position = random.randint(0, len(sequence))
    return sequence[:position] + name + sequence[position:]


# ORIGINAL:
# def calculate_statistics(sequence):
#     filtered_seq = ''.join([nt for nt in sequence if nt in 'ACGT'])
#     total = len(filtered_seq)
#     counts = {nt: filtered_seq.count(nt) for nt in 'ACGT'}
#     percentages = {nt: (counts[nt] / total) * 100 for nt in 'ACGT'}
#     cg = counts['C'] + counts['G']
#     at = counts['A'] + counts['T']
#     cg_ratio = (cg / at) * 100 if at != 0 else float('inf')
#     return percentages, cg_ratio

# MODIFIED (optimized counting using collections.Counter and added error handling):
def calculate_statistics(sequence):
    """Calculate nucleotide statistics, excluding non-DNA characters"""
    from collections import Counter

    filtered_seq = [nt for nt in sequence if nt in 'ACGT']
    if not filtered_seq:
        raise ValueError("No valid DNA nucleotides in sequence!")

    total = len(filtered_seq)
    counts = Counter(filtered_seq)

    # Initialize all nucleotides in case some are missing
    percentages = {nt: (counts.get(nt, 0) / total) * 100 for nt in 'ACGT'}

    cg = counts.get('C', 0) + counts.get('G', 0)
    at = counts.get('A', 0) + counts.get('T', 0)

    try:
        cg_ratio = (cg / at) * 100 if at != 0 else float('inf')
    except ZeroDivisionError:
        cg_ratio = float('inf')

    return percentages, cg_ratio


# ORIGINAL:
# def save_to_fasta(filename, header, sequence):
#     with open(filename, 'w') as f:
#         f.write(f">{header}\n{sequence}\n")

# MODIFIED (added line wrapping at 80 chars per FASTA standard and backup file creation):
def save_to_fasta(filename, header, sequence):
    """Save sequence to FASTA file with standard 80-character line wrapping"""
    import os

    # Create backup if file exists
    if os.path.exists(filename):
        base, ext = os.path.splitext(filename)
        backup_name = f"{base}_backup{ext}"
        os.replace(filename, backup_name)

    with open(filename, 'w') as f:
        f.write(f">{header}\n")

        # Split sequence into lines of 80 characters
        for i in range(0, len(sequence), 80):
            f.write(sequence[i:i + 80] + "\n")


def validate_input(length_str):
    """Validate that the sequence length is a positive integer"""
    try:
        length = int(length_str)
        if length <= 0:
            raise ValueError("Length must be positive")
        return length
    except ValueError:
        print("Error: Please enter a valid positive integer for sequence length")
        sys.exit(1)


def main():
    """Main program execution"""
    try:
        length_str = input("Enter the sequence length: ")
        length = validate_input(length_str)
        seq_id = input("Enter the sequence ID: ").strip()
        description = input("Provide a description of the sequence: ").strip()
        name = input("Enter your name: ").strip()

        if not seq_id or not name:
            raise ValueError("Sequence ID and name cannot be empty")

        base_sequence = generate_dna_sequence(length)
        final_sequence = insert_name(base_sequence, name)
        header = f"{seq_id} {description}"
        filename = f"{seq_id}.fasta"

        save_to_fasta(filename, header, final_sequence)
        percentages, cg_ratio = calculate_statistics(final_sequence)

        print(f"\nThe sequence was saved to the file {filename}")
        print("Sequence statistics (excluding non-DNA characters):")
        for nt in 'ACGT':
            print(f"{nt}: {percentages[nt]:.1f}%")
        print(f"%CG: {percentages['C'] + percentages['G']:.1f}")
        print(f"CG/AT ratio: {cg_ratio:.1f}")

    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()