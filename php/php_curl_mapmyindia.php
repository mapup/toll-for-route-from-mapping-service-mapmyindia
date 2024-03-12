<?php
//using mapmyindia API

$MAPMYINDIA_API_KEY = getenv('MAPMYINDIA_API_KEY');
$MAPMYINDIA_API_URL = "https://apis.mapmyindia.com/advancedmaps/v1";

$TOLLGURU_API_KEY = getenv('TOLLGURU_API_KEY');
$TOLLGURU_API_URL = "https://apis.tollguru.com/toll/v2";
$POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service";

// From and To locations
// New Delhi
$source_longitude='77.18609677688849';
$source_latitude='28.68932119156764';

// Mumbai coordinates
$destination_longitude='72.89902799500808';
$destination_latitude='19.092580173664984';

// Explore https://tollguru.com/toll-api-docs to get the best of all the parameters that tollguru has to offer
$request_parameters = array(
    "vehicle" => array(
        "type" => "2AxlesAuto",
    ),
    // Visit https://en.wikipedia.org/wiki/Unix_time to know the time format
    "departure_time" => "2021-01-05T09:46:08Z",
);

$url = $MAPMYINDIA_API_URL.'/'.$MAPMYINDIA_API_KEY.'/route_adv/driving/'.$source_longitude.','.$source_latitude.';'.$destination_longitude.','.$destination_latitude.'?geometries=polyline&overview=full';

// Connection
$mapmyindia = curl_init();

curl_setopt($mapmyindia, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($mapmyindia, CURLOPT_SSL_VERIFYPEER, false);

curl_setopt($mapmyindia, CURLOPT_URL, $url);
curl_setopt($mapmyindia, CURLOPT_RETURNTRANSFER, true);

// Getting response from MapMyIndia API
$response = curl_exec($mapmyindia);
$err = curl_error($mapmyindia);

curl_close($mapmyindia);

if ($err) {
	  echo "cURL Error #:" . $err;
} else {
	  echo "200 : OK\n";
}

// Extracting polyline from the JSON response
$data_mapmyindia = json_decode($response, true);

// Polyline
$polyline_mapmyindia = $data_mapmyindia['routes']['0']['geometry'];

// Using TollGuru API
$curl = curl_init();

curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);

$postdata = array(
	"source" => "mapmyindia",
  "polyline" => $polyline_mapmyindia,
  ...$request_parameters,
);

// JSON encoding source and polyline to send as postfields
$encode_postData = json_encode($postdata);

curl_setopt_array($curl, array(
  CURLOPT_URL => $TOLLGURU_API_URL . "/" . $POLYLINE_ENDPOINT,
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",


  // Sending MapMyIndia polyline to TollGuru
  CURLOPT_POSTFIELDS => $encode_postData,
  CURLOPT_HTTPHEADER => array(
    "content-type: application/json",
    "x-api-key: " . $TOLLGURU_API_KEY),
));

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
	  echo "cURL Error #:" . $err;
} else {
	  echo "200 : OK\n";
}

// Response from TollGuru
$data = var_dump(json_decode($response, true));
print_r($data);
?>
