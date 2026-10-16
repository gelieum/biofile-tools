import os

def filter_fastq(input_fastq: str, output_fastq: str = None, gc_bounds=(0,100), length_bounds=(0,2**32), quality_threshold: int =0):
  '''
  Filters FASTQ file reads by length, GC-content, and sequencing quality

  Arguments:
  input_fastq: str, path to the input FASTQ file
  output_path: str, name of the output FASTQ file (optional, defaults to the input file name) 
  gc_bounds: tuple / int, lower and upper limits for GC percentage / only upper limit for GC percentage
  length_bounds: tuple / int, lower and upper limits for read length / only upper limit for read length
  quality_threshold: int / float, minimum average Phred quality score per read

  Returns None.
  Creates "filtered" subdirectory in the parent folder of the input file and saves the result there
  Prints completion message and output file directory if succeeds
  '''
  parent_dir = os.path.dirname(input_fastq) # get input file directory
  output_dir = os.path.join(parent_dir, "filtered") # create "filtered" folder for filtered fastq files
  os.makedirs(output_dir, exist_ok=True) # create nothing if "filtered" folder already exists

  # in case of no output file name - input file name is taken  
  if output_fastq is None:
      output_fastq = os.path.basename(input_fastq)
 
  output_path = os.path.join(output_dir, output_fastq) # create an output_path argument for help function 

  # import help function from fastq.py module in helpers  
  from helpers.fastq import fastq_process 

  # call help function and pass arguments    
  result = fastq_process(input_fastq, output_path, gc_bounds, length_bounds, quality_threshold)

  # completion message and output file directory if successful  
  if result:
      print("----- FASTQ filtering has been successfully completed -----")
      print(f"----- Filtered FASTQ file directory: {output_path} -----")  

def convert_multiline_fasta_to_oneline(input_fasta: str, output_fasta: str = None):
    '''
    Converts a multiline FASTA file into a oneline FASTA format

    Arguments:
    input_fasta: str, path to the input multiline FASTA file
    output_fasta: str, name of the output FASTA file (optional, defaults to the input file name)

    Returns None
    Creates a "oneline" subdirectory in the parent folder of the input file and saves the result there
    Prints completion message and output file directory if succeeds
    '''
    parent_dir = os.path.dirname(input_fasta)
    output_dir = os.path.join(parent_dir, "oneline")
    os.makedirs(output_dir, exist_ok=True)
    
    if output_fasta is None:
      output_fasta = os.path.basename(input_fasta)

    output_path = os.path.join(output_dir, output_fasta)

    # import help function from bio_files.py module in helpers 
    from helpers.bio_files import oneline_fasta

    # call help function and pass arguments 
    result = oneline_fasta(input_fasta, output_path)

    # completion message and output file directory if successful 
    if result:
        print("----- Multiline FASTA has been successfully converted to oneline FASTA -----")
        print(f"----- Oneline FASTA directory: {output_path} -----")

def parse_blast_output(input_file: str, output_file: str = None):
    '''
    Parses a BLAST output file to extract the best alignment hit descriptions.

    Arguments:
    input_file: str, path to the input BLAST text file
    output_file: str, name of the output file (optional, defaults to the input file name)

    Returns None
    Creates an "output_blast" subdirectory in the parent folder of the input file and saves the sorted results there
    Prints completion message and output file directory if succeeds
    '''
    parent_dir = os.path.dirname(input_file)
    output_dir = os.path.join(parent_dir, "output_blast")
    os.makedirs(output_dir, exist_ok=True)
    
    if output_file is None:
      output_file = os.path.basename(input_file)

    output_path = os.path.join(output_dir, output_file)

    # import help function from bio_files.py module in helpers 
    from helpers.bio_files import parse_blast
    
    # call help function and pass arguments 
    result = parse_blast(input_file, output_path)

    # completion message and output file directory if successful 
    if result:
        print("----- BLAST has been successfully parsed -----")
        print(f"----- BLAST best hits directory: {output_path} -----")