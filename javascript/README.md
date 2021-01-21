# [MapmyIndia](https://www.mapmyindia.com/api/)

### Get API key to access MapmyIndia (if you have an API key skip this)
#### Step 1: Get API Key
* Create an account to access [MapmyIndia API Dashboard](https://www.mapmyindia.com/api/dashboard)
* go to signup/login link https://www.mapmyindia.com/api/login

#### Step 2: Getting you key
* Once you are logged in, go to https://www.mapmyindia.com/api/dashboard
* You will be presented with different keys, the key that we are looking
  for is `REST API Key for Web/Android/iOS`

With this in place, make a GET request: https://apis.mapmyindia.com/advancedmaps/v1/${key}/route_adv/driving/${source.longitude},${source.latitude};${destination.longitude},${destination.latitude}?geometries=polyline&overview=full

### Note:
* we will be sending `geometries` as `polyline` and `overview` as `full`.
* Setting overview as full sends us complete route. Default value for `overview` is `simplified`, which is an approximate (smoothed) path of the resulting directions.
* MapmyIndia accepts source and destination, as semicolon seperated

```javascript

const request = require("request");

// REST API key from MapmyIndia
const key = process.env.MAPMYINDIA_KEY;
const tollguruKey = process.env.TOLLGURU_KEY

// New Delhi
const source = {
    longitude: '77.18609677688849',
    latitude: '28.68932119156764',
}

// Mumbai
const destination = {
    longitude: '72.89902799500808',
    latitude: '19.092580173664984'
};

const url = `https://apis.mapmyindia.com/advancedmaps/v1/${key}/route_adv/driving/${source.longitude},${source.latitude};${destination.longitude},${destination.latitude}?geometries=polyline&overview=full`

const head = arr => arr[0]
// JSON path "$..geometry"
const getGeometry = body => body.routes.map(x => x.geometry)
const getPolyline = body => head(getGeometry(JSON.parse(body)));

const getRoute = (cb) => request.get(url, cb);

const handleRoute = (e, r, body) => console.log(getPolyline(body));

getRoute(handleRoute)
```

Note:

We extracted the polyline for a route from MapmyIndia API

We need to send this route polyline to TollGuru API to receive toll information

## [TollGuru API](https://tollguru.com/developers/docs/)

### Get key to access TollGuru polyline API
* create a dev account to receive a free key from TollGuru https://tollguru.com/developers/get-api-key
* suggest adding `vehicleType` parameter. Tolls for cars are different than trucks and therefore if `vehicleType` is not specified, may not receive accurate tolls. For example, tolls are generally higher for trucks than cars. If `vehicleType` is not specified, by default tolls are returned for 2-axle cars. 
* Similarly, `departure_time` is important for locations where tolls change based on time-of-the-day.

the last line can be changed to following

```javascript

const tollguruUrl = 'https://dev.tollguru.com/v1/calc/route';

const handleRoute = (e, r, body) =>  {

  console.log(body);
  const _polyline = getPolyline(body);
  console.log(_polyline);

  request.post(
    {
      url: tollguruUrl,
      headers: {
        'content-type': 'application/json',
        'x-api-key': tollguruKey
      },
      body: JSON.stringify({
        source: "mapmyindia",
        polyline: _polyline,
        vehicleType: "2AxlesAuto",
        departure_time: "2021-01-05T09:46:08Z"
      })
    },
    (e, r, body) => {
      console.log(e);
      console.log(body)
    }
  )
};

getRoute(handleRoute);
```

The working code can be found in index.js file.

## License
ISC License (ISC). Copyright 2020 &copy;TollGuru. https://tollguru.com/

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
