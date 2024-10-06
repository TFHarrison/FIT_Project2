with open('Tides.txt', 'r') as r:
    with open('Tides.csv', 'w') as w:
        w.write('\n'.join([','.join(list(filter(None, i.split(' ')))) for i in r.read().strip().split('\n')]))
