with open('Tides.txt', 'r') as r:
    with open('Tides.csv', 'w') as w:
        data=[list(filter(None, i.split(' '))) for i in r.read().strip().split('\n')]
        w.write('\n'.join([','.join(i) for i in data]))

m={'1':[0,0], '2':[0,0], '3':[0,0], '4':[0,0], '5':[0,0], '6':[0,0], '7':[0,0], '8':[0,0], '9':[0,0], '10':[0,0], '11':[0,0], '12':[0,0]}
for i in data[1:]:
    m[i[0]][0]+=float(i[6])
    m[i[0]][1]+=1

with open("Tidal.csv", 'w') as f:
    f.write('Mth,Mean\n')
    for i in m:f.write(f'{i},{m[i][0]/m[i][1]}\n')
