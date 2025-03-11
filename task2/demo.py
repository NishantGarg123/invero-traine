import csv
output = {}
keys=[]
flag=0
# Input and output file path
input_file = "csod.csv"

with open(input_file, "r",) as infile:
 
    reader = csv.reader(infile)
    
    for row in reader:
      if(flag==0):
         flag=1
         for i in range(len(row)):
            keys.append(row[i])
            output[row[i]]=[]
         print(keys)
         print(output)
      else:
         for i in range(len(row)):
            output[keys[i]].append(row[i])
    print(output)
      

        
    
        


