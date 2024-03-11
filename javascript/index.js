const request = require("request");
const polyline = require("polyline");


const MAPMYINDIA_API_KEY = process.env.MAPMYINDIA_API_KEY;
const MAPMYINDIA_API_URL = "https://apis.mapmyindia.com/advancedmaps/v1";

const TOLLGURU_API_KEY = process.env.TOLLGURU_API_KEY;
const TOLLGURU_API_URL = "https://apis.tollguru.com/toll/v2";
const POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service";

const source = { latitude: 28.68932119156764, longitude: 77.18609677688849 }; // New Delhi
const destination = { latitude: 19.092580173664984, longitude: 72.89902799500808, }; // Mumbai

// Explore https://tollguru.com/toll-api-docs to get the best of all the parameters that tollguru has to offer
const requestParameters = {
  "vehicle": {
    "type": "2AxlesAuto",
  },
  // Visit https://en.wikipedia.org/wiki/Unix_time to know the time format
  "departure_time": "2021-01-05T09:46:08Z",
}

const url = `${MAPMYINDIA_API_URL}/${MAPMYINDIA_API_KEY}/route_adv/driving/${source.longitude},${source.latitude};${destination.longitude},${destination.latitude}?geometries=polyline&overview=full`

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

const tollguruUrl = `${TOLLGURU_API_URL}/${POLYLINE_ENDPOINT}`;

const handleRoute = (e, r, body) => {

  console.log(body);
  const _polyline = getPolyline(body);
  console.log(_polyline);

  request.post(
    {
      url: tollguruUrl,
      headers: {
        'content-type': 'application/json',
        'x-api-key': TOLLGURU_API_KEY
      },
      body: JSON.stringify({
        source: "mapmyindia",
        polyline: _polyline,
        ...requestParameters,
      })
    },
    (e, r, body) => {
      console.log(e);
      console.log(body)
    }
  )
};

getRoute(handleRoute);
