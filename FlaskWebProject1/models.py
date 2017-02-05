import json
from pprint import pprint
import datetime
from datetime import timedelta
import requests

KEY = "AIzaSyAAVzNBEhnJujWK9UwjvDqz_pa-TQnkJp8"
TIME_SPENT_AT_ATTRACTIONS = 3


class LocationNotFoundError(Exception):
    pass

class APIQueryLimitReachedError(Exception):
    pass


def jsonParseURL(url):    
    response = requests.get(url)
    data = response.text
    jsonfile = json.loads(data)

    if jsonfile["status"] == "OVER_QUERY_LIMIT":
        print("Query limit reached")
        raise APIQueryLimitReachedError()

##    pprint(jsonfile)
    return (jsonfile)


class Location:
    def __init__(self, location):
        self.location = location
        self.jsonData = self.getLocationData(location.replace(" ", "+"))
        self.placeName = self.jsonData["result"]["name"]
        self.addressComponents = self.jsonData["result"]["address_components"]
        self.town = location
        self.placeAddress = self.jsonData["result"]["formatted_address"]
        self.placeLat = self.jsonData["result"]["geometry"]["location"]["lat"]
        self.placeLon = self.jsonData["result"]["geometry"]["location"]["lng"]
        self.placeID = self.jsonData["result"]["place_id"]
        self.tripDuration = 0

        for i in range (0, len (self.addressComponents)):
            if "postal_town" in self.addressComponents[i]["types"]:
                self.town = self.addressComponents[i]["long_name"]
                break
            elif "locality" in self.addressComponents[i]["types"]:
                self.town = self.addressComponents[i]["long_name"]
                break
            

    def getLocationData(self, location):
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + location + "&key=" + KEY
        try:
            placeID = jsonParseURL(url)["results"][0]["place_id"]
        except IndexError:
            raise LocationNotFoundError()
        
        url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + placeID + "&key=" + KEY
        return jsonParseURL(url)

        
    def getLocalPlaces(self):
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=popular+attractions+near+" + self.town + "&key=" + KEY
        url = url.replace(" ", "+")

        return jsonParseURL(url)


    def printDataOfTopLocation(self):
        print("Name: " + self.placeName + "\nAddress: " + self.placeAddress
              + "\nLat: " + str(self.placeLat) + "\nLon: " + str(self.placeLon))
        


class Route:
    def __init__(self, start, end=None, waypoints=[]):
        self.start = start
        self.end = end
        self.waypoints = waypoints


##    def waypoints(self, focus, waypoints):
##        

    
    def getDirections(self, time=""):
        if self.waypoints == []:
            if time == "":
                url = "https://maps.googleapis.com/maps/api/directions/json?origin=place_id:" + self.start.placeID + "&destination=place_id:" + self.end.placeID + "&mode=transit&key=" + KEY
            else:
                url = "https://maps.googleapis.com/maps/api/directions/json?origin=place_id:" + self.start.placeID + "&destination=place_id:" + self.end.placeID + "&departure_time=" + time + "&mode=transit&key=" + KEY

            jsonfile = jsonParseURL(url)

        else:
            wayps = "&waypoints=optimize:true"
            for i in self.waypoints:
                wayps += ("|place_id:" + i)

            if time == "":
                url = "https://maps.googleapis.com/maps/api/directions/json?origin=place_id:" + self.start.placeID + "&destination=place_id:" + self.start.placeID + wayps + "&mode=transit&key=" + KEY
            else:
                url = "https://maps.googleapis.com/maps/api/directions/json?origin=place_id:" + self.start.placeID + "&destination=place_id:" + self.start.placeID + wayps + "&departure_time=" + time + "&mode=transit&key=" + KEY


        startAddress = jsonfile["routes"][0]["legs"][0]["start_address"]
        endAddress = jsonfile["routes"][0]["legs"][0]["end_address"]
        arrivalTime = jsonfile["routes"][0]["legs"][0]["arrival_time"]["text"]
        departureTime = jsonfile["routes"][0]["legs"][0]["departure_time"]["text"]
        distance = jsonfile["routes"][0]["legs"][0]["distance"]["text"]
        duration = jsonfile["routes"][0]["legs"][0]["duration"]["value"]
        steps = jsonfile["routes"][0]["legs"][0]["steps"]

        print("From " + self.start.placeName + " to " + self.end.placeName + ":\n")
        for i in range(0, len(steps)):
            if steps[i]["travel_mode"] == "WALKING":
                print(steps[i]["html_instructions"])
            elif steps[i]["travel_mode"] == "TRANSIT":
                try:
                    print("Take the " + steps[i]["transit_details"]["line"]["short_name"] + " line from " +
                    steps[i]["transit_details"]["departure_stop"]["name"] + " to " +
                    steps[i]["transit_details"]["arrival_stop"]["name"])
                except KeyError:
                    print("Take the " + steps[i]["transit_details"]["line"]["name"] + " line from " +
                    steps[i]["transit_details"]["departure_stop"]["name"] + " to " +
                    steps[i]["transit_details"]["arrival_stop"]["name"])

                      
        print(distance + ", departing " + departureTime + " and arriving " +
              arrivalTime + "\n\n")

        self.tripDuration = duration




class DayPlanner:
    def __init__(self, focus):
        self.focus = focus
        self.location = Location(focus)

    def findPlacesToVisit(self, noOfPlaces):
        localPlaces = self.location.getLocalPlaces()["results"]

        i = 0
        time = datetime.datetime(2017, 2, 6, 9, 0, 0)
        currLocation = self.location
        
        for j in range(0, len(localPlaces)):
            nextLocation = Location(localPlaces[j]["name"])
            route = Route(currLocation, nextLocation)
            route.getDirections(str(int(time.timestamp())))
            time += timedelta(seconds=currLocation.tripDuration)
            time += timedelta(hours=TIME_SPENT_AT_ATTRACTIONS)
            currLocation = nextLocation
            i += 1

            if i == noOfPlaces:
                break
        
