import json
import urllib.request
from pprint import pprint

class LocationNotFoundError(Exception):
    pass

class Location:
    def __init__(self, location):
        self.location = location
        self.jsonData = self.getLocationData(location.replace(" ", "+"))
        self.placeName = self.jsonData["result"]["name"]
        self.addressComponents = self.jsonData["result"]["address_components"]
        self.placeAddress = self.jsonData["result"]["formatted_address"]
        self.placeLat = self.jsonData["result"]["geometry"]["location"]["lat"]
        self.placeLon = self.jsonData["result"]["geometry"]["location"]["lng"]
        self.placeID = self.jsonData["result"]["place_id"]

        for i in len (self.addressComponents):
            if "postal_town" in self.addressComponents[i]["types"]:
                self.town = self.addressComponents[i]["long_name"]
                break


    def getLocationData(self, location):
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + location + "&key=AIzaSyAd2-II-xiYnGx8bxvieAX8zJEWZYSFL4U"
        try:
            placeID = self.jsonParseURL(url)["results"][0]["place_id"]
        except IndexError:
            raise LocationNotFoundError()
        
        url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + placeID + "&key=AIzaSyAd2-II-xiYnGx8bxvieAX8zJEWZYSFL4U"
        return self.jsonParseURL(url)

        
    def getLocalPlaces(self):
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=things+to+do+near+" + self.location + "&key=AIzaSyAd2-II-xiYnGx8bxvieAX8zJEWZYSFL4U"
        return self.jsonParseURL(url)


    def printDataOfTopLocation(self):
        print("Name: " + self.placeName + "\nAddress: " + self.placeAddress
              + "\nLat: " + str(self.placeLat) + "\nLon: " + str(self.placeLon))
        

    def getDirections(self, otherLocation):
        otherPlace = location(otherLocation)
        url = "https://maps.googleapis.com/maps/api/directions/json?origin=place_id:" + self.placeID + "&destination=place_id:" + otherPlace.placeID + "&mode=transit&key=AIzaSyAd2-II-xiYnGx8bxvieAX8zJEWZYSFL4U"
        jsonfile = self.jsonParseURL(url)

        startAddress = jsonfile["routes"][0]["legs"][0]["start_address"]
        endAddress = jsonfile["routes"][0]["legs"][0]["end_address"]
        arrivalTime = jsonfile["routes"][0]["legs"][0]["arrival_time"]["text"]
        departureTime = jsonfile["routes"][0]["legs"][0]["departure_time"]["text"]
        distance = jsonfile["routes"][0]["legs"][0]["distance"]["text"]
        duration = jsonfile["routes"][0]["legs"][0]["duration"]["text"]
        steps = jsonfile["routes"][0]["legs"][0]["steps"]

        print("From " + self.placeName + " to " + otherPlace.placeName + ":\n")
        for i in range(0, len(steps)):
            if steps[i]["travel_mode"] == "WALKING":
                print(steps[i]["html_instructions"])
            elif steps[i]["travel_mode"] == "TRANSIT":
                print("Take the " + steps[i]["transit_details"]["line"]["short_name"] + " line from " +
                      steps[i]["transit_details"]["departure_stop"]["name"] + " to " +
                      steps[i]["transit_details"]["arrival_stop"]["name"])

                      
        print(distance + ", departing " + departureTime + " and arriving " +
              arrivalTime)


    def jsonParseURL(self, url):
        response = urllib.request.urlopen(url)
        data = response.read()
        text = data.decode('utf-8')

        jsonfile = json.loads(text)
        return (jsonfile)



class DayPlanner:
    def __init__(self, focus):
        self.focus = focus
        self.location = Location(focus)

    def findPlacesToVisit(self):
        localPlaces = self.location.getLocalPlaces()
        
