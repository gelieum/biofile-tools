def fastq_process(input_fastq, output_path, gc_bounds, length_bounds, quality_threshold):
  """
  Coordinates line-by-line reading and writing, format validation and multi-criteria filtering of a FASTQ file

  Arguments:
  input_fastq: str, path to the input FASTQ file
  output_path: str, path to save the filtered FASTQ file
  output_path: str, name of the output FASTQ file (optional, defaults to the input file name) 
  gc_bounds: tuple / int, lower and upper limits for GC percentage / only upper limit for GC percentage
  length_bounds: tuple / int, lower and upper limits for read length / only upper limit for read length
  quality_threshold: int / float, minimum average Phred quality score per read
  
  Returns str (path to the filtered file) or None if validation fails
  Prints an error message if the file extension is invalid
  """
  # FASTQ extension check
  if not input_fastq.endswith((".fastq", ".fq")):
    print("Error: File must be .fastq")
    return

  # first read flag
  is_first_read = True

  # line by line reading and writing FASTQ file
  with open(input_fastq, mode = "r") as infile, open(output_path, mode = "w") as outfile:
    while True:
        # end file check
      line1 = infile.readline()
      if not line1:
        break
        
      if is_first_read:
        # check for @ symbol in first line
        if not line1.startswith("@"):
          print("Error: File is not FASTQ format")
          return
        is_first_read = False
        
      line2 = infile.readline()
      line3 = infile.readline()
      line4 = infile.readline()

      # remove \n symbols in the end of the lines
      seq = line2.rstrip('\n')
      quality = line4.rstrip('\n')

      # call filter functions and aggregate results
      if (check_length(seq, length_bounds) and 
      check_gc(seq, gc_bounds) and 
      quality_check(quality, quality_threshold)):
         
         # write line by line in output file
         outfile.write(line1)
         outfile.write(line2)
         outfile.write(line3)
         outfile.write(line4)
   
    return output_path
  

def check_length(seq: str, length_bounds=(0,2**32)) -> bool:
  '''
  Checks if the read length falls within the specified boundaries

  Arguments:
  seq: str, the sequence (read) to evaluate
  length_bounds: tuple / int, lower and upper length limits (optional, default is (0, 2**32))
                   or a single integer acting as the upper limit while the lower limit defaults to 0
  
  Returns bool (True in case the sequence length satisfies the boundaries, False otherwise)
  '''
  if isinstance(length_bounds, tuple):
    min_len = length_bounds[0]
    max_len = length_bounds[1]
  else:
    min_len = 0
    max_len = length_bounds
    
  return min_len <= len(seq) <= max_len


def check_gc(seq: str, gc_bounds= (20,80)) -> bool:
  '''
  Calculates the GC percentage of a sequence and checks if it falls within the specified boundaries

  Arguments:
  seq: str, the sequence (read) to evaluate
  gc_bounds: tuple / int, lower and upper limits for GC-content percentage (optional, default is (20, 80))
               or a single number acting as the upper limit while the lower limit defaults to 0
  Returns bool (True if the calculated GC percentage satisfies the boundaries, False otherwise)
  '''
  gc_count = ((seq.upper().count('G') + seq.upper().count('C'))/len(seq))*100
  
  if isinstance(gc_bounds, tuple):
    min_gc = gc_bounds[0]
    max_gc = gc_bounds[1]
  else:
    min_gc = 0
    max_gc = gc_bounds
    
  return min_gc <= gc_count <= max_gc  
  

def quality_check(quality: str, quality_threshold: int = 0) -> bool:
  '''
  Evaluates if the average Phred quality score of a read meets the minimum threshold
  
  Arguments:
  quality: str, the quality score string from a FASTQ record (ASCII characters)
  quality_threshold: int, the minimum average Phred score (optional, default is 0)
  
  Returns bool (True if the calculated mean quality score is greater than or equal to the threshold, False otherwise)
  '''
  total_q = 0
  for i in quality:
    total_q += ord(i) - 33
  mean_q = total_q/len(quality)
    
  return mean_q >= quality_threshold
