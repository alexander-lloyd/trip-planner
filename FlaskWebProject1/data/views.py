from flask import request, jsonify, abort
from . import data
from ..models import Location


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

    Output of getLocalPlaces()

    {


    }





    :return:
    """
    location = request.args.get('location')
    if location:
        l_data = Location(location)
        attractions = l_data.getLocalPlaces()
        return attractions
    return abort(400)
