with open('record.txt', 'r') as f:
    lines = f.readlines()
print lines

print ('Parsing file names...')

updatedLines = []
for line in lines:
    line = line.replace('.jpg', '')
    updatedLines.append(line)

print('')


#write back to disk
with open('record.txt', 'w') as f:
    f.writelines(updatedLines)
