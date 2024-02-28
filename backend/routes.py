from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture['id'] == id:
            return jsonify(picture), 200
    return {'message': 'picutre not found'}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json
    for picture in data:
        if picture['id'] == new_picture['id']:
            message= "picture with id {0} already present".format(new_picture['id'])
            return {"Message": message}, 302

    data.append(new_picture)
    return jsonify(id=new_picture['id']), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_picture = request.json

    for i in range(len(data)):
        if new_picture['id'] == data[i]['id']:
            data[i] = new_picture
            return jsonify(message="successfuly updated"), 200

    return jsonify(message="Picture not found"), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for i in range(len(data)):
        if id == data[i]['id']:
            data.pop(i)
            return jsonify(message="successfuly updated"), 204

    return jsonify(message="Picture not found"), 404
