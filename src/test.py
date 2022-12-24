zips = {}
with open('zipCodes.csv', 'r') as f:
    for line in f:
        vals = line.split(',')
        zips[vals[0]] = vals[1]