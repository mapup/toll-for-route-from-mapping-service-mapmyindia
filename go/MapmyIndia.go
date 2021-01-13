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

//Source Coordinates
const (
	source_longitude float64 = 77.18609677688849
	source_latitude float64 = 28.68932119156764
)

// Destination Coordinates
const (
	destination_longitude float64 = 72.89902799500808
	destination_latitude float64 = 19.092580173664984
)
func main() {

	//	Getting polyline from MapmyIndia

	// Key for MapmyIndia
	key_MapmyIndia := os.Getenv("MAPMYINDIA_KEY")

	url := fmt.Sprintf("https://apis.mapmyindia.com/advancedmaps/v1/%s/route_adv/driving/%v,%v;%v,%v?geometries=polyline&overview=full", key_MapmyIndia, source_longitude, source_latitude, destination_longitude, destination_latitude)
	spaceClient := http.Client{
		Timeout: time.Second * 15, // Timeout after 2 seconds
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

	url_tollguru := "https://dev.tollguru.com/v1/calc/route"

	// key for Tollguru
	key_tollguru := os.Getenv("Tollgurukey")

	requestBody, err := json.Marshal(map[string]string{
		"source":         "mapmyindia",
		"polyline":       polyline,
		"vehicleType":    "2AxlesAuto",
		"departure_time": "2021-01-05T09:46:08Z",
	})

	request, err := http.NewRequest("POST", url_tollguru, bytes.NewBuffer(requestBody))
	request.Header.Set("x-api-key", key_tollguru)
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
