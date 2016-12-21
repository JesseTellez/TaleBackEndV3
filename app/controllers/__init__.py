#may introduce a circular referance
from flask import *

def get_success_response(results={}):
    """Format the success JSON response object"""
    results["success"] = True
    return jsonify(results)

def get_error_response(message):
    """"Format the error JSON response object"""
    response = jsonify({
        "success": False,
        "error": message
    })
    return response