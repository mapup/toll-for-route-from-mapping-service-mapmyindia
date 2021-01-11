# [MapmyIndia](https://www.mapmyindia.com/api/)

### Get API key to access MapmyIndia (if you have an API key skip this)
#### Step 1: Get API Key
* Create an account to access [MapmyIndia API Dashboard](https://www.mapmyindia.com/api/dashboard)
* go to [signup/login](https://www.mapmyindia.com/api/login)

#### Step 2: Getting you key
* Once you are logged in, go to [MapmyIndia API Dashboard](https://www.mapmyindia.com/api/dashboard)
* You will be presented with different keys, the key that we are looking
  for is `REST API Key for Web/Android/iOS`

With this in place, make a GET request:='https://apis.mapmyindia.com/advancedmaps/v1/{a}/route_adv/driving/{b},{c};{d},{e}?geometries=polyline&overview=full'.format(a=key,b=source_longitude,c=source_latitude,d=destination_longitude,e=destination_latitude)
### Note:
* REQUEST should include `geometries` as `polyline` and `overview` as `full`.
* Setting overview as full sends us complete route. Default value for `overview` is `simplified`, which is an approximate (smoothed) path of the resulting directions.
* MapmyIndia accepts source and destination, as semicolon seperated

```python
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
```

Note:

We extracted the polyline for a route from MapmyIndia API

We need to send this route polyline to TollGuru API to receive toll information

## [TollGuru API](https://tollguru.com/developers/docs/)

### Get key to access TollGuru polyline API
* create a dev account to [receive a free key from TollGuru](https://tollguru.com/developers/get-api-key)
* suggest adding `vehicleType` parameter. Tolls for cars are different than trucks and therefore if `vehicleType` is not specified, may not receive accurate tolls. For example, tolls are generally higher for trucks than cars. If `vehicleType` is not specified, by default tolls are returned for 2-axle cars. 
* Similarly, `departure_time` is important for locations where tolls change based on time-of-the-day.

the last line can be changed to following

```python

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
            'vehicleType': '2AxlesAuto',              
            'departure_time' : "2021-01-05T09:46:08Z"   
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


```

The working code can be found in index.js file.

## License
ISC License (ISC). Copyright 2020 &copy;TollGuru. https://tollguru.com/

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
