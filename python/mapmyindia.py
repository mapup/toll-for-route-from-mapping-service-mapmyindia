#Importing modules
import json
import requests
import os

#API key for MapmyIndia
key=os.environ.get("MapmyIndia_API_Key")
#API key for Tollguru
Tolls_Key =os.environ.get("TOLLGURU_API_KEY")

'''Extrating Polyline from MapmyIndia'''
def get_polyline_from_mapmyindia(source_longitude,source_latitude,destination_longitude,destination_latitude):
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
        #Extracting polyline
        polyline_from_mapmyindia=response["routes"][0]['geometry']
        return(polyline_from_mapmyindia)
                

'''Calling Tollguru API'''
def get_rates_from_tollguru(polyline):
    #Tollguru querry url
    Tolls_URL = 'https://dev.tollguru.com/v1/calc/route'
    #Tollguru resquest parameters
    headers = {
                'Content-type': 'application/json',
                'x-api-key': Tolls_Key
                }
    params = {   
                # explore https://tollguru.com/developers/docs/ to get best off all the parameter that tollguru offers 
                'source': "mapmyindia",
                'polyline': polyline ,                      #  this is polyline that we fetched from the mapping service     
                'vehicleType': '2AxlesAuto',                #'''Visit https://tollguru.com/developers/docs/#vehicle-types to know more options'''
                'departure_time' : "2021-01-05T09:46:08Z"   #'''Visit https://en.wikipedia.org/wiki/Unix_time to know the time format'''
                }
    #Requesting Tollguru with parameters
    response_tollguru= requests.post(Tolls_URL, json=params, headers=headers).json()
    #checking for errors or printing rates
    if str(response_tollguru).find('message')==-1:
        return(response_tollguru['route']['costs'])
    else:
        raise Exception(response_tollguru['message'])

'''Program Starts'''
#Step 1 : Get Sourcer and Destination name and fetch their geocodes
source_longitude,source_latitude=77.18609677688849,28.68932119156764                     #New Delhi
destination_longitude,destination_latitude=72.89902799500808,19.09258017366498           #Mumbai

#Step 2 : Get polyline from MapmyIndia
polyline_from_mapmyindia=get_polyline_from_mapmyindia(source_longitude,source_latitude,destination_longitude,destination_latitude)

#Step 3 : Get rates from TollGuru API
rates_from_tollguru=get_rates_from_tollguru(polyline_from_mapmyindia)

#Print the rates of all the available modes of payment
if rates_from_tollguru=={}:
    print("The route doesn't have tolls")
else:
    print(f"The rates are \n {rates_from_tollguru}")

'''Program Ends'''