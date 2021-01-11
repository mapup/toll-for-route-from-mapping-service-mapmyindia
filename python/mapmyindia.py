#Importing modules
import json
import requests

'''Fetching Polyline from mapmyindia'''

#API key for mapmyindia
key=''

#Source and Destination Coordinates
#Dallas, TX
source_longitude='-96.7970'
source_latitude='32.7767'
#New York, NY
destination_longitude='-74.0060'
destination_latitude='40.7128'

#Query mapmyindia with Key and Source-Destination coordinates
url='https://maps.googleapis.com/maps/api/directions/json?origin={a},${b}&destination=${c},${d}&key=${e}'.format(a=source_latitude,b=source_longitude,c=destination_latitude,d=destination_longitude,e=key)

#converting the response to json
response=requests.get(url).json()

#checking for errors in response 
if str(response).find('message')==-1:
    pass
else:
    raise Exception(response['message'])

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

