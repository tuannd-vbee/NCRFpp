with open('data/training_nsw.yml', 'r') as f_in:
    lines = f_in.readlines()

f_out = open('data/training_loc.txt', 'w')
for line in lines:
    if 'range' in line or 'fraction' in line:
        continue
    f_out.write(line)

f_in.close()