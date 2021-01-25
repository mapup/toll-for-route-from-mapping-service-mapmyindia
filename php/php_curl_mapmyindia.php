<?php
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

//getting response from mapmyindia api...
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

//polyline..
$polyline_mapmyindia = $data_mapmyindia['routes']['0']['geometry'];


//using tollguru API..
$curl = curl_init();

curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);


$postdata = array(
	"source" => "here",
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
$data = var_dump(json_decode($response, true));
print_r($data);
?>
