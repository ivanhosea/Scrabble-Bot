with open('dictionary_v2.txt', mode='r') as file_input:
    with open('dictionary_v2_filtered.txt', mode='w') as file_output:
        for line in file_input:
            # Only add to the new file if every letter in the word is lowercase
            if line.rstrip().islower():
                file_output.write(line)