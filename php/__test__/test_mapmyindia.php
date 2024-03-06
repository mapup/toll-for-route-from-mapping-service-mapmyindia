<?php
error_reporting(0);
//using mapmyindia API

$MAPMYINDIA_API_KEY = getenv('MAPMYINDIA_API_KEY');
$MAPMYINDIA_API_URL = "https://apis.mapmyindia.com/advancedmaps/v1";

$TOLLGURU_API_KEY = getenv('TOLLGURU_API_KEY');
$TOLLGURU_API_URL = "https://apis.tollguru.com/toll/v2";
$POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service";

//Source and Destination Coordinates..
function getPolyline($source_longitude,$source_latitude,$destination_longitude,$destination_latitude) {
  global $MAPMYINDIA_API_KEY, $MAPMYINDIA_API_URL;

  $url = $MAPMYINDIA_API_URL.'/'.$MAPMYINDIA_API_KEY.'/route_adv/driving/'.$source_longitude.','.$source_latitude.';'.$destination_longitude.','.$destination_latitude.'?geometries=polyline&overview=full';

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

  //polyline..
  $p_mapmyindia = $data_mapmyindia['routes']['0']['geometry'];
  return $p_mapmyindia;
}
require_once(__DIR__.'/test_location.php');
foreach ($locdata as $item) {
$source_longitude = $item['from_long'];
$source_latitude = $item['from_lat'];
$destination_longitude = $item['to_long'];
$destination_latitude = $item['to_lat'];
$polyline_mapmyindia = getPolyline($source_longitude,$source_latitude,$destination_longitude,$destination_latitude);
//using tollguru API..
$curl = curl_init();

curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);


$postdata = array(
	"source" => "gmaps",
	"polyline" => $polyline_mapmyindia
);

//json encoding source and polyline to send as postfields..
$encode_postData = json_encode($postdata);

curl_setopt_array($curl, array(
  CURLOPT_URL => $TOLLGURU_API_URL . "/" . $POLYLINE_ENDPOINT,
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

//response from tollguru..
$data = json_decode($response, true);

$tag = $data['route']['costs']['tag'];
$cash = $data['route']['costs']['cash'];

$dumpFile = fopen("dump.txt", "a") or die("unable to open file!");
fwrite($dumpFile, "from =>");
fwrite($dumpFile, $item['from'].PHP_EOL);
fwrite($dumpFile, "to =>");
fwrite($dumpFile, $item['to'].PHP_EOL);
fwrite($dumpFile, "polyline =>".PHP_EOL);
fwrite($dumpFile, $polyline_jawmaps.PHP_EOL);
fwrite($dumpFile, "tag =>");
fwrite($dumpFile, $tag.PHP_EOL);
fwrite($dumpFile, "cash =>");
fwrite($dumpFile, $cash.PHP_EOL);
fwrite($dumpFile, "*************************************************************************".PHP_EOL);

echo "tag = ";
print_r($data['route']['costs']['tag']);
echo "\ncash = ";
print_r($data['route']['costs']['cash']);
echo "\n";
echo "**************************************************************************\n";
}
?>
