package main

import (
	"bytes"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
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
)

var (
	source_longitude string
	source_latitude  string

	destination_longitude string
	destination_latitude  string
)

// Reading the CSV file for test cases
func readCsvFile(filePath string) [][]string {
	// Open the file
	csvfile, err := os.Open(filePath)
	if err != nil {
		log.Fatalln("Couldn't open the csv file", err)
	}

	// Parse the file
	r := csv.NewReader(csvfile)
	records, err := r.ReadAll()
	if err != nil {
		log.Fatal("Unable to parse file as CSV for ", err)
	}

	return records

}

func main() {
	records := readCsvFile("File Path")

	for i := 1; i < len(records); i++ {
		source_longitude, err := strconv.ParseFloat(records[i][6], 8)
		source_latitude, err := strconv.ParseFloat(records[i][5], 8)
		destination_longitude, err := strconv.ParseFloat(records[i][8], 8)
		destination_latitude, err := strconv.ParseFloat(records[i][7], 8)

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

		// Tollguru API request

		url_tollguru := fmt.Sprintf("%s/%s", TOLLGURU_API_URL, POLYLINE_ENDPOINT)

		requestBody, err := json.Marshal(map[string]string{
			"source":         "mapmyindia",
			"polyline":       polyline,
			"vehicleType":    "2AxlesAuto",
			"departure_time": "2021-01-05T09:46:08Z",
		})

		request, err := http.NewRequest("POST", url_tollguru, bytes.NewBuffer(requestBody))
		request.Header.Set("x-api-key", TOLLGURU_API_KEY)
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

		var cost map[string]interface{}
		jsonEr := json.Unmarshal([]byte(body), &cost)
		if jsonEr != nil {
			log.Fatal(result)
		}

		toll := cost["route"].(map[string]interface{})["costs"].(map[string]interface{})["cash"]
		fmt.Printf("The toll rate for Source Longitude: %v  : Source Latitude: %v :Destination Longitude: %v, Destination Latitude: %v is %v\n", source_longitude, source_latitude, destination_longitude, destination_latitude, toll)
	}
}
