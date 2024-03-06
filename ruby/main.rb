require 'HTTParty'
require 'json'

MAPMYINDIA_API_KEY = ENV["MAPMYINDIA_API_KEY"]
MAPMYINDIA_API_URL = "https://apis.mapmyindia.com/advancedmaps/v1"

TOLLGURU_API_KEY = ENV["TOLLGURU_API_KEY"]
TOLLGURU_API_URL = "https://apis.tollguru.com/toll/v2"
POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service"

# Source Details - New Delhi Lat-Long coordinates
source = { longitude: '77.18609', latitude: '28.68932' }
# Destination Details - Mumbai Lat-long coordinates
destination = { longitude: '72.89902', latitude: '19.09258' }

# GET Request to MapmyIndia for Polyline
KEY = ENV['MAPMYINDIA_KEY']
MAPMYINDIA_URL = "#{MAPMYINDIA_API_URL}/#{KEY}/route_adv/driving/#{source[:longitude]},#{source[:latitude]};#{destination[:longitude]},#{destination[:latitude]}?geometries=polyline&overview=full"
RESPONSE = HTTParty.get(MAPMYINDIA_URL).body
json_parsed = JSON.parse(RESPONSE)

# Extracting polyline from JSON
mapmyindia_polyline = json_parsed['routes'].map { |x| x['geometry'] }.pop

# Sending POST request to TollGuru
tollguru_url = "#{TOLLGURU_API_URL}/#{POLYLINE_ENDPOINT}" 
headers = {'content-type' => 'application/json', 'x-api-key' => TOLLGURU_API_KEY}
body = {'source' => "mapmyindia", 'polyline' => mapmyindia_polyline, 'vehicleType' => "2AxlesAuto", 'departure_time' => "2021-01-05T09:46:08Z"}
tollguru_response = HTTParty.post(tollguru_url,:body => body.to_json, :headers => headers)
