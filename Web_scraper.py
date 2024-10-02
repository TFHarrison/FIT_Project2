import requests, zipfile
from time import sleep
from random import random

with open("Weather station codes.txt", 'r') as f:
	data=[list(filter(None, i.split(' '))) for i in f.read().strip().split('\n')]

data=[[i[0], ' '.join(i[1:len(i)-9])]+i[len(i)-9:len(i)-7]+[' '.join(i[len(i)-7:len(i)-5]), ' '.join(i[len(i)-5:len(i)-3])]+i[len(i)-3:] for i in data]

url=lambda x: f"http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=139&p_display_type=dataFile&p_startYear=&p_c=&p_stn_num={x}"

#Need to put your own cookies in for it to work
#if they detect you web scraping just change your cookies and it will be fine
cookies={"_easyab_seed":"",
         "_ga":"",
         "_ga_Y4Z1NSQVJ5":"",
         "ak_bmsc":"",
         "JSESSIONID":""}

for i in data:
    webpage = requests.get(url(i[0]), cookies=cookies, headers={'User-Agent': 'Mozilla/5.0'})
    loc=webpage.text.find("All years of data")-41
    url2=''
    while True:
        ch=webpage.text[loc]
        if ch=='"':
            break
        url2=webpage.text[loc]+url2
        loc-=1

    sleep(0.5*random())

    zipdata = requests.get('http://www.bom.gov.au'+url2.replace('amp;', ''), cookies=cookies, headers={'User-Agent': 'Mozilla/5.0'})
    if not ("Your request cannot be completed" in zipdata.text):
        print(i[0], True)
        with open(f'Data/{i[0]}.zip', 'wb') as f:
            f.write(zipdata.content)
    else:
        print(i[0],False)

    sleep(0.5*random())

#Seperate the download and the compile given the download is likely to trip errors
fname=lambda x: f'{x}/IDCJAC0001_{x}_Data1.csv'

with open('Main_data.csv', 'w') as Main:
    Main.write('Lat,long,Year,Month,Rain\n')
    for i in data:
        with zipfile.ZipFile(f'Data/{i[0]}.zip', 'r') as zipper:
            zipper.extractall(i[0])
            
        with open(fname(i[0]), 'r') as f:
            Main.write('\n'.join([','.join(i[2:4]+x.split(',')[2:-1]) for x in f.read().strip('\n').split('\n')[1:]])+'\n')
        
        print(i[0])
            
