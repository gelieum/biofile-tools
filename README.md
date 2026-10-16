# Bioinformatics Files Toolkit (Biofile-Tools)

**Biofile-Tools** is a toolkit providing core utilities for sequencing data filtration and biological file manipulation. Developed entirely using the Python standard library.

Author:
* Angelina Popova

## Project Structure

| Directory/File | Description |
| :--- | :--- |
| `main.py` | Contains core utility functions for processing BLAST, FASTA, and FASTQ data|
| `helpers/fastq.py` | Help functions for FASTQ files processing|
| `helpers/bio_files.py` |Help functions for BLAST and FASTA files processing|

---

## Core Features & Functionality

The toolkit provides three main workflows, fully documented with Python docstrings:

### 1. FASTQ Filtration (`filter_fastq`)
Implements an optimized, memory-efficient line-by-line streaming pipeline to filter high-throughput sequencing reads based on multiple quality and composition metrics

#### Arguments:
* `input_fastq` (str): Path to the input `.fastq` file.
* `output_fastq` (str): Name of the output file. Screened reads are automatically saved into a `filtered/` directory.
* `gc_bounds` (tuple / int / float): GC-content percentage limits. Default is `(0, 100)`. If a single number is passed, it acts as the upper limit (lower limit defaults to 0).
* `length_bounds` (tuple / int): Read length limits. Default is `(0, 2**32)`. Follows the same single-number upper limit logic as `gc_bounds`.
* `quality_threshold` (int / float): Minimum acceptable average Phred33 quality score per read. Default is `0`.

---

### 2. Biological File Manipulation

#### Multiline to Oneline FASTA Conversion (`convert_multiline_fasta_to_oneline`)
Converts standard multiline FASTA files into a oneline sequence format by merging fragmented sequence lines under each `>` header.
* **Arguments:** `input_fasta` (str), `output_fasta` (str, optional).
* **Result:** If `output_fasta` is omitted, it defaults to the input file name. Results are saved in a newly created `oneline/` subdirectory.

#### BLAST Output Parsing (`parse_blast_output`)
Parses raw flat text BLAST reports (`.txt`) to extract the top-scoring biological functional description for each query, eliminating organism tags and technical details.
* **Arguments:** `input_file` (str), `output_file` (str).
* **Result:** Selects the very first hit from the `Description` column under the `Sequences producing significant alignments:` section for each query. Saves the final cleaned protein list sorted alphabetically in a single column within the `output_blast/` directory.

---

## Technical Highlights

* **Memory Efficiency ("On-the-fly" processing):** The FASTQ pipeline processes streams dynamically via `.readline()`. It never stores more than one read in RAM at a time.
* **Dependencies:** Developed using pure standard Python libraries, requiring no external heavy bioinformatics packages. You only need **os library** imported.

---