# Importing modules
import json
import requests
import os

MAPMYINDIA_API_KEY = os.environ.get("MAPMYINDIA_API_KEY")
MAPMYINDIA_API_URL = "https://apis.mapmyindia.com/advancedmaps/v1"

TOLLGURU_API_KEY = os.environ.get("TOLLGURU_API_KEY")
TOLLGURU_API_URL = "https://apis.tollguru.com/toll/v2"
POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service"

# New Delhi
source_longitude, source_latitude = (
    77.18609677688849,
    28.68932119156764,
)

# Mumbai
destination_longitude, destination_latitude = (
    72.89902799500808,
    19.09258017366498,
)

# Explore https://tollguru.com/toll-api-docs to get best of all the parameter that tollguru has to offer
request_parameters = {
    "vehicle": {
        "type": "2AxlesAuto",
    },
    # Visit https://en.wikipedia.org/wiki/Unix_time to know the time format
    "departure_time": "2021-01-05T09:46:08Z",
}

def get_polyline_from_mapmyindia(
    source_longitude, source_latitude, destination_longitude, destination_latitude
):
    """Extrating Polyline from MapmyIndia"""

    # Query MapmyIndia with Key and Source-Destination coordinates
    url = "{a}/{b}/route_adv/driving/{c},{d};{e},{f}?geometries=polyline&overview=full".format(
        b=MAPMYINDIA_API_KEY,
        c=source_longitude,
        d=source_latitude,
        e=destination_longitude,
        f=destination_latitude,
    )
    # Converting the response to JSON
    response = requests.get(url).json()
    # Checking for errors in response
    if str(response).find("message") > -1:
        raise Exception(
            "{}: {} , check latitude,longitude perhaps".format(
                response["code"], response["message"]
            )
        )
    elif str(response).find("responsecode") > -1 and response["responsecode"] == "401":
        raise Exception(
            "{} {}".format(response["error_code"], response["error_description"])
        )
    else:
        # Extracting polyline
        polyline_from_mapmyindia = response["routes"][0]["geometry"]
        return polyline_from_mapmyindia


def get_rates_from_tollguru(polyline):
    """Calling Tollguru API"""

    # TollGuru query URL
    Tolls_URL = f"{TOLLGURU_API_URL}/{POLYLINE_ENDPOINT}"
    # TollGuru request parameters
    headers = {"Content-type": "application/json", "x-api-key": TOLLGURU_API_KEY}
    params = {
        **request_parameters,
        "source": "mapmyindia",
        "polyline": polyline,  #  this is polyline that we fetched from the mapping service
    }

    # Requesting TollGuru with parameters
    response_tollguru = requests.post(Tolls_URL, json=params, headers=headers).json()
    # Checking for errors or printing rates
    if str(response_tollguru).find("message") == -1:
        return response_tollguru["route"]["costs"]
    else:
        raise Exception(response_tollguru["message"])


"""Program Starts"""
# Step 1 : Get polyline from MapmyIndia
polyline_from_mapmyindia = get_polyline_from_mapmyindia(
    source_longitude, source_latitude, destination_longitude, destination_latitude
)

# Step 2 : Get rates from TollGuru API
rates_from_tollguru = get_rates_from_tollguru(polyline_from_mapmyindia)

# Step 3 : Print the rates of all the available modes of payment
if rates_from_tollguru == {}:
    print("The route doesn't have tolls")
else:
    print(f"The rates are \n {rates_from_tollguru}")

"""Program Ends"""
