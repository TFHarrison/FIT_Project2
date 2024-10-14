#Code to download and compile the data from BOM for rainfall
#Need matching weather station file that you can easily get from bom
#2/10/2024

import requests, zipfile
from time import sleep
from random import random

#Open and read the weather station data to get longitude and latitude for everything
with open("Weather station codes.txt", 'r') as f:
	data=[list(filter(None, i.split(' '))) for i in f.read().strip().split('\n')]

#Finish cleaning the data to get it into the  most useable format because BOM is bad
data=[[i[0], ' '.join(i[1:len(i)-9])]+i[len(i)-9:len(i)-7]+[' '.join(i[len(i)-7:len(i)-5]), ' '.join(i[len(i)-5:len(i)-3])]+i[len(i)-3:] for i in data]

#Default URL for the data page for a given weather station number
#use this one because the zip file URL has a seperate value under the p_c option
#I couldnt find a way to predict this value so i scan the previous page that i can emulate to get the url that i can use
#It is a scuffed method but it works
url=lambda x: f"http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=139&p_display_type=dataFile&p_startYear=&p_c=&p_stn_num={x}"

#Need to put your own cookies in for it to work
#if they detect you web scraping just change your cookies and it will be fine
cookies={"_easyab_seed":"",
         "_ga":"",
         "_ga_Y4Z1NSQVJ5":"",
         "ak_bmsc":"",
         "JSESSIONID":""}

#loop through all weather stations to download data
for i in data:
    
    webpage = requests.get(url(i[0]), cookies=cookies, headers={'User-Agent': 'Mozilla/5.0'})
    
    #If this code stops working then just read through the HTML on the BOM page and see if you can update the 41 value to find the new URL
    #Finds the end of the URL
    loc=webpage.text.find("All years of data")-41
    url2=''
    
    #loop through to find the rest of the URL
    while True:
        ch=webpage.text[loc]
        if ch=='"':
            break
        url2=webpage.text[loc]+url2
        loc-=1

    #Sleep to not trigger the web scraper detection
    sleep(0.5*random())

    #Collect the zipdata from the attained URL
    zipdata = requests.get('http://www.bom.gov.au'+url2.replace('amp;', ''), cookies=cookies, headers={'User-Agent': 'Mozilla/5.0'})

    #This is a test case to ensure the request was sucessful because they will send a page with the text if the request was invailid
    if not ("Your request cannot be completed" in zipdata.text):

        #write Zipdata
        print(i[0], True)
        with open(f'Data/{i[0]}.zip', 'wb') as f:
            f.write(zipdata.content)
    else:
        print(i[0],False)

    #This is to bypass the web scraper detections on the page, it is not perfect but it works vast majority of the time
    sleep(0.5*random())

#Seperate the download and the compile given the download is likely to trip errors


#this is a defaulkt file name used by BOM
fname=lambda x: f'{x}/IDCJAC0001_{x}_Data1.csv'

#Open the main file tro compile to
with open('Main_data.csv', 'w') as Main:
    #set up headers
    Main.write('Name,Lat,long,Year,Month,Rain\n')

    #loop through the weather stations
    for i in data:

        #Unpack the given zip file and extract the data
        with zipfile.ZipFile(f'Data/{i[0]}.zip', 'r') as zipper:
            zipper.extractall(i[0])

        #open the extracted data, the file Data1 file, this is the monthly data, the Data12 file is the daily file
        with open(fname(i[0]), 'r') as f:

            #Write the extracted data to the man file
            Main.write('\n'.join([','.join(i[1:4]+x.split(',')[2:-1]) for x in f.read().strip('\n').split('\n')[1:]])+'\n')
        
        print(i[0])
            

