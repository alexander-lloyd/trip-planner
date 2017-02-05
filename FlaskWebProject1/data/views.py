import pickle
import time
from flask import request, jsonify, abort, session
from . import data
from ..models import Location


# TODO: Handle Exceptions

@data.route('/autocomplete')
def autocomplete():
    """

    :return: Json in the form:

    {
    "suggestions": [ "United Arab Emirates", "United Kingdom", "United States" ]
    }

    """
    query = request.args.get('term', '')
    if len(query) >= 4:
        l = Location(query)
        suggestions = l.getSuggested()
        return jsonify(suggestions)


@data.route('/suggested-places')
def suggested():
    """

    parameter location -> Address for suggested Attractions.
    Note Address preferred

    Output of getLocalPlaces() ->

    {
       data: [
       {'name':...,
        'address':...,
        'stars':...,
        'image_url':...},
        {'name':...,
        'address':...,
        'stars':...,
        'image_url':...},
    }
    :return: Request Object
    """
    pickled = session.get("location")
    location = pickle.loads(pickled)
    print("Location after pickle" + str(location))
    print(location.location)
    if location is not None:
        print(location)
        attractions = location.getLocalPlaces()
        print(attractions)
        return jsonify({'data': attractions})
        # return jsonify({
        #         "data": [
        #             {'name': "A",
        #              'address': "B",
        #              'stars': 3,}]
        #     })


@data.route('/auto_fill')
def auto_fill():
    print("Starting Auto Fill")
    l = request.args.get('location')
    location = Location(l)
    print(location.jsonData)
    print("Location before pickle " + str(location))
    print(location.location)
    session.clear()
    session['location'] = pickle.dumps(location)
    print(session['location'])
    return l
