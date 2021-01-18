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
