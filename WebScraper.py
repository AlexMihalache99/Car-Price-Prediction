from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd
from requests.models import Response
import time

#https://www.pistonheads.com/classifieds?Category=used-cars&Distance=2147483647&M=0&Postcode=SA1+8JF&YearFrom=2010&YearTo=2021

website = 'https://www.pistonheads.com/classifieds?Category=used-cars&Distance=2147483647&M=0&Postcode=SA1+8JF&YearFrom=2010&YearTo=2021'
session = HTMLSession()

#variable initialization
car_make = []
car_model = []
car_manufacture_year = []
car_price = []
car_mileage = []
car_gear_transmission = []
car_fuel_type = []
car_horse_power = []
car_body = []
car_colour = []
car_doors = []
car_fuel_economy = []
car_seats = []
car_engine_size = []
car_owners = []
extraction_time = []

"""
Method to get the html of a page
webiste - url of the page

return - html of the page

"""
def getData(website):
       response = session.get(website)
       soup = BeautifulSoup(response.text, 'html.parser')
       return soup

"""
Method to get to  the next page
soup - html of a page

return - url of the next page or none if it doesn't exist
"""
def getNextPage(soup):

       page = soup.find('ul', {'class' :'pages'})
       if not page.find('li', {'class' : 'disabled next'}):
              website = 'http://www.pistonheads.com' + str(page.find('li', {'class': 'next'}).find('a')['href'])
              return website
       else:
              return

"""
Method to click onto a car ad
soup - html of the car ad

return - url of the car ad or none if it doesn't exist
"""
def getIntoPage(soup):
       page = soup.find('div', {'class' :"listing-headline"})

       if page != None:
              ad = page.find('a')['href']
              return ad
       else: 
              return

nr = 0
while True:
       soup = getData(website)
       website = getNextPage(soup)
       nr+=1

       #finds all the cars
       cars = soup.find_all('div', {'class': 'result-contain'})

       for car in cars:

              #car make, car model, manufacture year
              try:
                     adTitle = car.find('h3').get_text()#extracting the whole ad title

                     age = adTitle[len(adTitle) - 5 :len(adTitle) - 1]
                     make = adTitle.split(' ')[0]
                     if make == 'Land':#special case when the make of the car is Land Rover
                            make = make + ' ' + adTitle.split(' ')[1]

                     model = adTitle[len(make) + 1:]
                     model = model.split(' (')[0]

                     car_make.append(make)
                     car_model.append(model)
                     car_manufacture_year.append(age)
              except:
                     car_make.append('n/a')
                     car_model.append('n/a')
                     car_manufacture_year.append('n/a')
              
              #car price
              try:
                     car_price.append(car.find('span', {'class':'price'}).get_text())
              except:
                     car_price.append('n/a')
              
              # boolean variables to know if 
              # those features are in the ad or not
              carMileageOn = False
              transmissionOn = False
              fuelOn = False
              hpOn = False
              
              for tag in car.find_all('li'):

                     #car car_mileage
                     if tag.find('i', {'class' : 'flaticon solid gauge-1'}) != None :
                            car_mileage.append(tag.get_text().strip())
                            carMileageOn = True
                     
                     #car gear transmission
                     elif  tag.find('i', {'class' : 'flaticon solid location-pin-4'}) != None :
                            car_gear_transmission.append(tag.get_text().strip())
                            transmissionOn = True
                     
                     #car fuel type
                     elif tag.find('i', {'class' : 'flaticon solid gas-1'}) != None :
                            car_fuel_type.append(tag.get_text().strip())
                            fuelOn = True

                     #car horse power
                     elif tag.find('i', {'class' : 'flaticon solid battery-charging-3'}) != None :
                            car_horse_power.append(tag.get_text().strip())
                            hpOn = True
              
              if carMileageOn ==False:
                     car_mileage.append('n/a')
              
              if transmissionOn ==False:
                     car_gear_transmission.append('n/a')
              
              if fuelOn ==False:
                     car_fuel_type.append('n/a')
              
              if hpOn ==False:
                     car_horse_power.append('n/a')

              if getIntoPage(car) != None:
                     ad = getIntoPage(car)
              

              carAd = getData(ad)

              # boolean variables to know if 
              # those features are in the ad or not
              carBodyOn = False
              carFuelEconomyOn = False
              carSeatsOn = False
              carEngineSizeOn = False
              carOwnersOn = False
              carColourOn = False
              carDoorsOn = False

              for tag in carAd.find_all('li', {'class':'🏎3fQDCJ 🏎2qBQr3'}):

                     if tag.find('span', {'class': '🏎pu9GZU'})!= None:

                            #car body type
                            if tag.find('span', {'class': '🏎pu9GZU'}).get_text() == "Body type":
                                   car_body.append(tag.find('span', {'class': '🏎wQdGX0'}).get_text())
                                   carBodyOn = True
                            
                            #car fuel economy
                            if tag.find('span', {'class': '🏎pu9GZU'}).get_text() == "Economy":
                                   car_fuel_economy.append(tag.find('span', {'class': '🏎wQdGX0'}).get_text())
                                   carFuelEconomyOn = True
                            
                            #car number of seats
                            if tag.find('span', {'class': '🏎pu9GZU'}).get_text() == "Seats":
                                   car_seats.append(tag.find('span', {'class': '🏎wQdGX0'}).get_text())
                                   carSeatsOn = True
                            
                            #car engine size
                            if tag.find('span', {'class': '🏎pu9GZU'}).get_text() == "Size":
                                   car_engine_size.append(tag.find('span', {'class': '🏎wQdGX0'}).get_text())
                                   carEngineSizeOn = True

                            #car number of previous car_owners 
                            if tag.find('span', {'class': '🏎pu9GZU'}).get_text() == "Owners":
                                   car_owners.append(tag.find('span', {'class': '🏎wQdGX0'}).get_text())
                                   carOwnersOn = True
                            
                            #car colour
                            if tag.find('span', {'class': '🏎pu9GZU'}).get_text() == "Colour":
                                   car_colour.append(tag.find('span', {'class': '🏎wQdGX0'}).get_text())
                                   carColourOn = True
                            
                            #car number of doors
                            if tag.find('span', {'class': '🏎pu9GZU'}).get_text() == "Doors":
                                   car_doors.append(tag.find('span', {'class': '🏎wQdGX0'}).get_text())
                                   carDoorsOn = True
                            
              
              if carBodyOn == False:
                     car_body.append('n/a')

              if carFuelEconomyOn == False:
                     car_fuel_economy.append('n/a')

              if carSeatsOn == False:
                     car_seats.append('n/a')

              if carEngineSizeOn == False:
                     car_engine_size.append('n/a')

              if carOwnersOn == False:
                     car_owners.append('n/a')

              if carColourOn == False:
                     car_colour.append('n/a')

              if carDoorsOn == False:
                     car_doors.append('n/a')


       #if we dont have a next page 
       # or we hit 100 pages then break
       if not website or nr == 100:
              break

#get the time of the extraction
scraped_month = time.gmtime().tm_mon
scraped_year = time.gmtime().tm_year
scraped_day = time.gmtime().tm_mday 

scraped_time = str(scraped_day) + "-" + str(scraped_month) + "-" + str(scraped_year)
for i in range(0, len(car_make)):
       extraction_time.append(scraped_time)

# adding data to a Panda DataFrame
data = pd.DataFrame(
   {'Make': car_make,
    'Model': car_model,
    'Year of manufacture' : car_manufacture_year,
    'Body' : car_body,
    'Doors' : car_doors,
    'Seats' : car_seats,
    'Colour' : car_colour,
    'Engine size' : car_engine_size,
    'Price': car_price,
    'Mileage': car_mileage,
    'Fuel type': car_fuel_type,
    'Fuel economy': car_fuel_economy,
    'Transmission': car_gear_transmission,
    'Horse power': car_horse_power,
    'Owners' : car_owners,
    'Extraction time': extraction_time
   }
)

#deleting data where the car name
# could have not been scraped
data = data.loc[data['Make'] != 'n/a']

# Data cleaning
# I want only numbers in the Excel file
data ['Mileage'] = data['Mileage'].apply(lambda x: x.strip('miles'))
data ['Horse power'] = data['Horse power'].apply(lambda x: x.strip('bhp'))
data ['Price'] = data['Price'].apply(lambda x: x.strip('+VAT'))
data ['Engine size'] = data['Engine size'].apply(lambda x: x.strip('L'))
data ['Fuel economy'] = data['Fuel economy'].apply(lambda x: x.strip('mpg'))

#data goes to an Excel file
data.to_excel('cars_info.xlsx', index = False)