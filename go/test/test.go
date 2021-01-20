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
	source_longitude string
	source_latitude string
)

// Destination Coordinates
var (
	destination_longitude string
	destination_latitude string
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
		log.Fatal("Unable to parse file as CSV for " , err)
	}

	return records

}
//
func main()  {
	records := readCsvFile("File Path")
	token := os.Getenv("MAPMYINDIA_TOKEN")
	token_tollguru := os.Getenv("Tollgurukey")

	for i := 1; i < len(records); i++ {
		source_longitude, err := strconv.ParseFloat(records[i][6], 8)
		source_latitude, err := strconv.ParseFloat(records[i][5], 8)
		destination_longitude, err := strconv.ParseFloat(records[i][8], 8)
		destination_latitude, err := strconv.ParseFloat(records[i][7], 8)


		url := fmt.Sprintf("https://apis.mapmyindia.com/advancedmaps/v1/%s/route_adv/driving/%v,%v;%v,%v?geometries=polyline&overview=full", token, source_longitude, source_latitude, destination_longitude, destination_latitude)
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

		url_tollguru := "https://dev.tollguru.com/v1/calc/route"



		requestBody, err := json.Marshal(map[string]string{
			"source":         "mapbox",
			"polyline":       polyline,
			"vehicleType":    "2AxlesAuto",
			"departure_time": "2021-01-05T09:46:08Z",
		})

		request, err := http.NewRequest("POST", url_tollguru, bytes.NewBuffer(requestBody))
		request.Header.Set("x-api-key", token_tollguru)
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
		fmt.Printf("The toll rate for Source Longitude: %v  : Source Latitude: %v :Destination Longitude: %v, Destination Latitude: %v is %v\n",source_longitude,source_latitude,destination_longitude,destination_latitude,toll)
	}}
