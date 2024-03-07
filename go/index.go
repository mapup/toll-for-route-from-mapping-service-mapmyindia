package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"
)

var (
	MAPMYINDIA_API_KEY string = os.Getenv("MAPMYINDIA_API_KEY")
	TOLLGURU_API_KEY   string = os.Getenv("TOLLGURU_API_KEY")
)

const (
	MAPMYINDIA_API_URL = "https://apis.mapmyindia.com/advancedmaps/v1"

	TOLLGURU_API_URL  = "https://apis.tollguru.com/toll/v2"
	POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service"

	// New Delhi
	source_latitude  float32 = 28.68932119156764
	source_longitude float32 = 77.18609677688849

	// Mumbai
	destination_latitude  float32 = 19.092580173664984
	destination_longitude float32 = 72.89902799500808
)

// Explore https://tollguru.com/toll-api-docs to get the best of all the parameters that tollguru has to offer
var requestParams = map[string]interface{}{
	"vehicle": map[string]interface{}{
		"type": "2AxlesAuto",
	},
	// Visit https://en.wikipedia.org/wiki/Unix_time to know the time format
	"departure_time": "2021-01-05T09:46:08Z",
}

func main() {

	//	Getting polyline from MapmyIndia

	// Key for MapmyIndia
	url := fmt.Sprintf("%s/%s/route_adv/driving/%v,%v;%v,%v?geometries=polyline&overview=full", MAPMYINDIA_API_URL, MAPMYINDIA_API_KEY, source_longitude, source_latitude, destination_longitude, destination_latitude)
	spaceClient := http.Client{
		Timeout: time.Second * 15, // Timeout after 15 seconds
	}

	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		log.Fatal(err)
	}

	req.Header.Set("User-Agent", "spacecount-tutorial")

	res, getErr := spaceClient.Do(req)
	if getErr != nil {
		log.Fatal(getErr)
	}

	if res.Body != nil {
		defer res.Body.Close()
	}

	body, readErr := ioutil.ReadAll(res.Body)
	if readErr != nil {
		log.Fatal(readErr)
	}
	var result map[string]interface{}

	jsonErr := json.Unmarshal(body, &result)
	if jsonErr != nil {
		log.Fatal(result)
	}

	polyline := result["routes"].([]interface{})[0].(map[string]interface{})["geometry"].(string)
	fmt.Printf("\n\n%v\n\n", polyline)

	// Tollguru API request

	url_tollguru := fmt.Sprintf("%s/%s", TOLLGURU_API_URL, POLYLINE_ENDPOINT)

	params := map[string]interface{}{
		"source":   "mapmyindia",
		"polyline": polyline,
	}

	for k, v := range requestParams {
		params[k] = v
	}

	requestBody, err := json.Marshal(params)

	request, err := http.NewRequest("POST", url_tollguru, bytes.NewBuffer(requestBody))
	request.Header.Set("x-api-key", TOLLGURU_API_URL)
	request.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(request)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	body, error := ioutil.ReadAll(resp.Body)
	if error != nil {
		log.Fatal(err)
	}

	fmt.Println("\nresponse Body:\n", string(body))
}
