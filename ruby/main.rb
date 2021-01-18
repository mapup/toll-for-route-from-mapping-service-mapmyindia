require 'HTTParty'
require 'json'

# Source Details - New Delhi Lat-Long coordinates
SOURCE = { longitude: '77.18609', latitude: '28.68932' }
# Destination Details - Mumbai Lat-long coordinates
DESTINATION = { longitude: '72.89902', latitude: '19.09258' }

# GET Request to MapmyIndia for Polyline
KEY = ENV['MAPMYINDIA_KEY']
MAPMYINDIA_URL = "https://apis.mapmyindia.com/advancedmaps/v1/#{KEY}/route_adv/driving/#{SOURCE[:longitude]},#{SOURCE[:latitude]};#{DESTINATION[:longitude]},#{DESTINATION[:latitude]}?geometries=polyline&overview=full"
RESPONSE = HTTParty.get(MAPMYINDIA_URL).body
json_parsed = JSON.parse(RESPONSE)

# Extracting polyline from JSON
mapmyindia_polyline = json_parsed['routes'].map { |x| x['geometry'] }.pop

# Sending POST request to TollGuru
TOLLGURU_URL = 'https://dev.tollguru.com/v1/calc/route'
TOLLGURU_KEY = ENV['TOLLGURU_KEY']
headers = {'content-type' => 'application/json', 'x-api-key' => TOLLGURU_KEY}
body = {'source' => "mapmyindia", 'polyline' => mapmyindia_polyline, 'vehicleType' => "2AxlesAuto", 'departure_time' => "2021-01-05T09:46:08Z"}
tollguru_response = HTTParty.post(TOLLGURU_URL,:body => body.to_json, :headers => headers)