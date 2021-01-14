# [MapmyIndia](https://www.mapmyindia.com/api/)

### Get API key to access MapmyIndia (if you have an API key skip this)
#### Step 1: Get API Key
* Create an account to access [MapmyIndia API Dashboard](https://www.mapmyindia.com/api/dashboard)
* go to [signup/login](https://www.mapmyindia.com/api/login)

#### Step 2: Getting you key
* Once you are logged in, go to [MapmyIndia API Dashboard](https://www.mapmyindia.com/api/dashboard)
* You will be presented with different keys, the key that we are looking
  for is `REST API Key for Web/Android/iOS`

With this in place, make a GET request: https://apis.mapmyindia.com/advancedmaps/v1/'.$key.'/route_adv/driving/'.$source_longitude.','.$source_latitude.';'.$destination_longitude.','.$destination_latitude.'?geometries=polyline&overview=full

### Note:
* REQUEST should include `geometries` as `polyline` and `overview` as `full`.
* Setting overview as full sends us complete route. Default value for `overview` is `simplified`, which is an approximate (smoothed) path of the resulting directions.
* MapmyIndia accepts source and destination, as semicolon seperated

```php

//using mapmyindia API

//Source and Destination Coordinates..
//New Delhi coordinates
$source_longitude='77.18609677688849';
$source_latitude='28.68932119156764';
// Mumbai coordinates
$destination_longitude='72.89902799500808';
$destination_latitude='19.092580173664984';
$key = 'mapmyindia_key';

$url = 'https://apis.mapmyindia.com/advancedmaps/v1/'.$key.'/route_adv/driving/'.$source_longitude.','.$source_latitude.';'.$destination_longitude.','.$destination_latitude.'?geometries=polyline&overview=full';

//connection..
$mapmyindia = curl_init();

curl_setopt($mapmyindia, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($mapmyindia, CURLOPT_SSL_VERIFYPEER, false);

curl_setopt($mapmyindia, CURLOPT_URL, $url);
curl_setopt($mapmyindia, CURLOPT_RETURNTRANSFER, true);

//getting response from googleapis..
$response = curl_exec($mapmyindia);
$err = curl_error($mapmyindia);

curl_close($mapmyindia);

if ($err) {
	  echo "cURL Error #:" . $err;
} else {
	  echo "200 : OK\n";
}

//extracting polyline from the JSON response..
$data_mapmyindia = json_decode($response, true);
$data_new = $data_mapmyindia['routes'];
$new_data = $data_new['0'];
$pol_data = $new_data['geometry'];

//polyline..
$polyline_mapmyindia = $pol_data;

```

### Note:

* We extracted the polyline for a route from MapmyIndia API

* We need to send this route polyline to TollGuru API to receive toll information

## [TollGuru API](https://tollguru.com/developers/docs/)

### Get key to access TollGuru polyline API
* create a dev account to [receive a free key from TollGuru](https://tollguru.com/developers/get-api-key)
* suggest adding `vehicleType` parameter. Tolls for cars are different than trucks and therefore if `vehicleType` is not specified, may not receive accurate tolls. For example, tolls are generally higher for trucks than cars. If `vehicleType` is not specified, by default tolls are returned for 2-axle cars. 
* Similarly, `departure_time` is important for locations where tolls change based on time-of-the-day and can be passed through `$postdata`.

the last line can be changed to following

```php

//using tollguru API..
$curl = curl_init();

curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);


$postdata = array(
	"source" => "google",
	"polyline" => $polyline_mapmyindia
);

//json encoding source and polyline to send as postfields..
$encode_postData = json_encode($postdata);

curl_setopt_array($curl, array(
CURLOPT_URL => "https://dev.tollguru.com/v1/calc/route",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "POST",


//sending mapmyindia polyline to tollguru
CURLOPT_POSTFIELDS => $encode_postData,
CURLOPT_HTTPHEADER => array(
				      "content-type: application/json",
				      "x-api-key: tollguru_api_key"),
));

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
	  echo "cURL Error #:" . $err;
} else {
	  echo "200 : OK\n";
}

//response from tollguru..
var_dump(json_decode($response, true));
// $data = var_dump(json_decode($response, true));
//print_r($data);

```

The working code can be found in php_curl_mapmyindia.php file.

## License
ISC License (ISC). Copyright 2020 &copy;TollGuru. https://tollguru.com/

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
