import csv

# Input and output file path
input_file = "csod.csv"
output_file = "output.csv"

with open(input_file, "r",newline="") as infile:
 with open(output_file, "w",newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        if len(row) >= 3:  
            row[1],row[2] = row[2],row[1]  
        writer.writerow(row)

print(f"Modified CSV saved as {output_file}")
