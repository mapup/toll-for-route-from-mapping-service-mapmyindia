const request = require("request");
const polyline = require("polyline");

// REST API key from MapmyIndia
const key = process.env.MAPMYINDIA_API_KEY;
const tollguruKey = process.env.TOLLGURU_KEY;

// Dallas, TX
const source = {
    longitude: '-96.7970',
    latitude: '32.7767',
}

// New York, NY
const destination = {
    longitude: '-74.0060',
    latitude: '40.7128'
};

const url = `https://maps.googleapis.com/maps/api/directions/json?origin=${source.latitude},${source.longitude}&destination=${destination.latitude},${destination.longitude}&key=${key}`;


const head = arr => arr[0];
const flatten = (arr, x) => arr.concat(x);

// JSON path "$..points"
const getPoints = body => body.routes
  .map(x => x.legs)
  .reduce(flatten)
  .map(x => x.steps)
  .reduce(flatten)
  .map(x => x.polyline.points)
  .map(x => polyline.decode(x))
  .reduce(flatten);

const getPolyline = body => polyline.encode(getPoints(JSON.parse(body)));

const getRoute = (cb) => request.get(url, cb);

//const handleRoute = (e, r, body) => console.log(getPolyline(body));
//getRoute(handleRoute)

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
      body: JSON.stringify({ source: "mapmyindia", polyline: _polyline })
    },
    (e, r, body) => {
      console.log(e);
      console.log(body)
    }
  )
};

getRoute(handleRoute);
