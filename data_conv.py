#Code to convert main data into usable subsections
#5/10/2024

#open Main data
with open('Main_data.csv', 'r') as f:
    data=[i.split(',') for i in f.read().split('\n')[1:]]
    #data=[[float(i[0]), float(i[1]), int(i[2]), int(i[3]), float(i[4])] for i in data]

#dictionaries to sort the data
years={}
stations={}

for lin in data:
    
    #seperating out data
    loc=','.join(lin[:2])
    year=lin[2]
    month=lin[3]
    rain=float(lin[4])

    #seperating out data for stations
    if loc in stations:
        if year in stations[loc]:
            stations[loc][year][0]+=rain
            stations[loc][year][1]+=1
        else:stations[loc][year]=[rain,1]
    else:stations[loc]={year:[rain,1]}

    #Seperating out per year
    if year in years:
        if month in years[year]:
            years[year][month][0]+=rain
            years[year][month][1]+=1
        else:years[year][month]=[rain, 1]
    else:years[year]={month:[rain,1]}

#Cleaning the statiion data to give 1 value per station
for station in stations:
    sdat=stations[station]
    ydat=[sdat[year][0]/sdat[year][1] for year in sdat]
    stations[station]=sum(ydat)/len(ydat)

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
        
    years_f[year]=yavg[0]/yavg[1]
    
avg=avg[0]/avg[1]

for month in months_f:
    months_f[month]=months_f[month][0]/months_f[month][1]

#Writing to all the files
with open('Webpg/Clean/Station_avg.csv', 'w') as f:
    f.write('Lat,long,Rain\n')
    for station in stations:
        f.write(station+','+str(stations[station])+'\n')

with open('Webpg/Clean/Monthly_avg.csv', 'w') as f:
    f.write('Month,Rain\n')
    for month in months_f:
        f.write(month+','+str(months_f[month])+'\n')

with open('Webpg/Clean/Yearly_avg.csv', 'w') as f:
    f.write('Year,Rain\n')
    for year in sorted(years_f):
        f.write(year+','+str(years_f[year])+'\n')

with open('Webpg/Clean/Station_dev.csv', 'w') as f:
    f.write('Lat,long,Rain\n')
    for station in stations:
        f.write(station+','+str(stations[station]-avg)+'\n')

with open('Webpg/Clean/Monthly_dev.csv', 'w') as f:
    f.write('Month,Rain\n')
    for month in months_f:
        f.write(month+','+str(months_f[month]-avg)+'\n')

with open('Webpg/Clean/Yearly_dev.csv', 'w') as f:
    f.write('Year,Rain\n')
    for year in sorted(years_f):
        f.write(year+','+str(years_f[year]-avg)+'\n')
