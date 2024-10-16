#Code to convert main data into usable subsections
#5/10/2024

#open Main data
with open('Main_data.csv', 'r') as f:
    data=[i.split(',') for i in f.read().split('\n')[1:]]
    #data=[[float(i[0]), float(i[1]), int(i[2]), int(i[3]), float(i[4])] for i in data]

#dictionaries to sort the data
years={}
stations={}

for lin in data[:-1]:
    
    #seperating out data
    loc=','.join(lin[:3])
    year=lin[3]
    month=lin[4]
    rain=float(lin[5])

    #seperating out data for stations
    if loc in stations:
        if year in stations[loc]:
            stations[loc][year][0][0]+=rain
            stations[loc][year][0][1]+=1
            if rain>stations[loc][year][1]:
                stations[loc][year][1]=rain
            elif rain<stations[loc][year][1]:
                stations[loc][year][1]=rain
        else:stations[loc][year]=[[rain,1],rain,rain]
    else:stations[loc]={year:[[rain,1],rain,rain]}

    #Seperating out per year
    if year in years:
        if month in years[year]:
            years[year][month][0]+=rain
            years[year][month][1]+=1
        else:years[year][month]=[rain, 1]
    else:years[year]={month:[rain,1]}
    
#Cleaning the statiion data to give 1 value per station
with open('Clean/Station_data.csv', 'w') as f:
    f.write('Name,Lat,Long,Year,Mean,Max,Min\n')
    for station in stations:
        sdat=stations[station]
        for year in sdat:
            f.write(f'{station},{year},{round(sdat[year][0][0]/sdat[year][0][1],2)},{sdat[year][1]},{sdat[year][2]}\n')
        ydat=[sdat[year][0][0]/sdat[year][0][1] for year in sdat]
        stations[station]=[round(sum(ydat)/len(ydat),2), sdat[max(sdat, key=lambda x: sdat[x][1])][1],sdat[min(sdat, key=lambda x: sdat[x][2])][2]]
        
#default final lists
months_f={'01':[0,0], '02':[0,0], '03':[0,0], '04':[0,0], '05':[0,0], '06':[0,0],
          '07':[0,0], '08':[0,0], '09':[0,0], '10':[0,0], '11':[0,0], '12':[0,0]}
years_f={}
avg=[0,0]

#Cleaning the year and months data
for year in years:
    yavg=[0,0]
    for month in years[year]:
        mdat=years[year][month]
        mavg=mdat[0]/mdat[1]
        
        months_f[month][0]+=mavg
        months_f[month][1]+=1
        
        yavg[0]+=mavg
        yavg[1]+=1

        avg[0]+=mavg
        avg[1]+=1
        
    years_f[year]=round(yavg[0]/yavg[1],2)
    
avg=round(avg[0]/avg[1],2)

for month in months_f:
    months_f[month]=months_f[month][0]/months_f[month][1]

#Writing to all the files
with open('Clean/Station_avg.csv', 'w') as f:
    f.write('Name,Lat,Long,Mean,Max,Min\n')
    for station in stations:
        f.write(station+','+','.join([str(i) for i in stations[station]])+'\n')

with open('Clean/Monthly_avg.csv', 'w') as f:
    f.write('Month,Rain\n')
    for month in months_f:
        f.write(month+','+str(months_f[month])+'\n')

with open('Clean/Yearly_avg.csv', 'w') as f:
    f.write('Year,Rain\n')
    for year in sorted(years_f):
        f.write(year+','+str(years_f[year])+'\n')

with open('Clean/Station_dev.csv', 'w') as f:
    f.write('Name,Lat,Long,Rain\n')
    for station in stations:
        f.write(station+','+str(stations[station][0]-avg)+'\n')

with open('Clean/Yearly_dev.csv', 'w') as f:
    f.write('Year,Rain\n')
    for year in sorted(years_f):
        f.write(year+','+str(years_f[year]-avg)+'\n')

