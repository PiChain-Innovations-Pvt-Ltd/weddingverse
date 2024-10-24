def split_file(input_file, lines_per_file=375):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()  # Read all lines in the file

    # Calculate the number of output files needed
    total_lines = len(lines)
    num_files = (total_lines // lines_per_file) + (1 if total_lines % lines_per_file > 0 else 0)

    # Write each split file
    for i in range(num_files):
        with open(f'weddingbazaar/decorators/txt_loc_list/split_file_{i + 1}.txt', 'w', encoding='utf-8') as output_file:
            # Calculate start and end indices for each chunk
            start_index = i * lines_per_file
            end_index = start_index + lines_per_file
            output_file.writelines(lines[start_index:end_index])  # Write the chunk to the file

    print(f'Successfully split into {num_files} files.')

# Usage
input_file_path = 'weddingbazaar/decorators/txt_loc_list/allDecors.txt'  # Replace with your file path
split_file(input_file_path)
