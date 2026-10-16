def oneline_fasta(input_fasta: str, output_path: str) -> str:
    '''
    Converts a multiline FASTA file into a oneline format by merging split sequence lines

    Arguments:
    input_fasta: str, path to the input multiline FASTA file
    output_path: str, path to save the output oneline FASTA file

    Returns str (the output path of the generated single-line FASTA file)
    '''
    with open(input_fasta, 'r') as infile, open(output_path, 'w') as outfile:
        seq = [] # empty list for oneline output

        for line in infile:
            line = line.strip()

            # check for start symbol >
            if line.startswith('>'):
                # check if seq is not empty
                if seq:
                    outfile.write("".join(seq) + "\n")
                    seq = []
                outfile.write(line + "\n")
            else:
                # adding lines to seq list
                seq.append(line)

        if seq:
            # writing last oneline output in the output file
            outfile.write("".join(seq) + "\n")

        return output_path

def parse_blast(input_file: str, output_path: str) -> str:
    """
    Extracts the best hit descriptions from a BLAST report, cleans them and sorts alphabetically

    Arguments:
    input_file: str, path to the input BLAST text file
    output_path: str, path to save the sorted list of best hit descriptions

    Returns str (the output path of the generated text file)
    """
    aligns = []
    search_protein = False

    with open(input_file, 'r') as infile:
        for line in infile:
            line = line.strip()

            if "Sequences producing significant alignments:" in line:
                search_protein = True
                continue

            if search_protein:
                if line == "" or "Description" in line or "Scientific" in line:
                    continue

                if "[" in line:
                    descr = line.split("[")[0].strip()
                elif "..." in line:
                    descr = line.split("...")[0]
                else:
                    descr = line

                aligns.append(descr)
                search_protein = False

    aligns.sort()
    
    with open(output_path, "w") as outfile:
         for descr in aligns:
             outfile.write(descr + "\n")

    return output_path
            