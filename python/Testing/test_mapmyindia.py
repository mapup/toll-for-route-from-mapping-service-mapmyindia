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
                'source': "here",
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

'''Testing'''
#Importing Functions
from csv import reader,writer
import time
temp_list=[]
with open('testCases_with_geocode.csv','r') as f:
    csv_reader=reader(f)
    for count,i in enumerate(csv_reader):
        #if count>2:
        #   break
        if count==0:
            i.extend(("Input_polyline","Tollguru_Tag_Cost","Tollguru_Cash_Cost","Tollguru_QueryTime_In_Sec"))
        else:
            try:
                source_longitude,source_latitude=i[5],i[4]
                destination_longitude,destination_latitude=i[7],i[6]
                polyline=get_polyline_from_mapmyindia(source_longitude,source_latitude,destination_longitude,destination_latitude)
                i.append(polyline)
            except:
                i.append("Routing Error") 
            
            start=time.time()
            try:
                rates=get_rates_from_tollguru(polyline)
            except:
                i.append(False)
            time_taken=(time.time()-start)
            if rates=={}:
                i.append((None,None))
            else:
                try:
                    tag=rates['tag']
                except:
                    tag=None
                try:
                    cash=rates['cash']
                except :
                    cash=None
                i.extend((tag,cash))
            i.append(time_taken)
        #print(f"{len(i)}   {i}\n")
        temp_list.append(i)

with open('testCases_result.csv','w') as f:
    writer(f).writerows(temp_list)

'''Testing Ends'''