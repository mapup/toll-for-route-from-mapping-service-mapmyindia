#Importing modules
import json
import requests

'''Fetching Polyline from MapmyIndia'''

#API key for MapmyIndia
key=''

#Source and Destination Coordinates
#New Delhi
source_longitude='77.18609677688849'
source_latitude='28.68932119156764'
#Mumbai
destination_longitude='72.89902799500808'
destination_latitude='19.092580173664984'

#Query MapmyIndia with Key and Source-Destination coordinates
url='https://apis.mapmyindia.com/advancedmaps/v1/{a}/route_adv/driving/{b},{c};{d},{e}?geometries=polyline&overview=full'.format(a=key,b=source_longitude,c=source_latitude,d=destination_longitude,e=destination_latitude)

#converting the response to json
response=requests.get(url).json()

#checking for errors in response 
if str(response).find('message')>-1:
    raise Exception("{}: {} , check latitude,longitude perhaps".format(response['code'],response['message']))
elif str(response).find('responsecode')>-1 and response['responsecode']=='401':
    raise Exception("{} {}".format(response['error_code'],response['error_description']))
else:
    #The response is a dict where Polyline is inside first element named "routes" , first element is a list , go to 1st element there
    #you will find a key named "geometry" which is essentially the Polyline''' 
    
    #Extracting polyline
    polyline=response["routes"][0]['geometry']




'''Calling Tollguru API'''

#API key for Tollguru
Tolls_Key = ''

#Tollguru querry url
Tolls_URL = 'https://dev.tollguru.com/v1/calc/route'

#Tollguru resquest parameters
headers = {
            'Content-type': 'application/json',
            'x-api-key': Tolls_Key
          }
params = {
            'source': "mapmyindia",
            'polyline': polyline ,                      #  this is polyline that we fetched from the mapping service     
            'vehicleType': '2AxlesAuto',                #'''TODO - Need to provide users a slist of acceptable values for vehicle type'''
            'departure_time' : "2021-01-05T09:46:08Z"   #'''TODO - Specify time formats'''
        }

#Requesting Tollguru with parameters
response_tollguru= requests.post(Tolls_URL, json=params, headers=headers).json()

#checking for errors or printing rates
if str(response_tollguru).find('message')==-1:
    print('\n The Rates Are ')
    #extracting rates from Tollguru response is no error
    print(*response_tollguru['summary']['rates'].items(),end="\n\n")
else:
    raise Exception(response_tollguru['message'])

