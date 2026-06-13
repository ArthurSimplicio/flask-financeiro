from flask import jsonify

def response(type:str, message:str, status:int):
    return jsonify({type: message}), status