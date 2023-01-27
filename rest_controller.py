"""
Create a REST controller that performs CRUD operations on a DynamoDB table.
"""

import flask
import boto3

app = flask.Flask(__name__)

TABLE_NAME = "demo_table"
ddb_client = boto3.client("dynamodb")

# GET method to retrieve all the records
@app.route("/records", methods=["GET"])
def get_all_records():
    """
    Retrieve all the records from the table
    """
    try:
        response = ddb_client.scan(TableName=TABLE_NAME)
        return flask.jsonify(response["Items"])
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500

# GET method to retrieve a single record by ID
@app.route("/records/<id>", methods=["GET"])
def get_record(id):
    """
    Retrieve a single record by ID
    """
    try:
        response = ddb_client.get_item(
            TableName=TABLE_NAME,
            Key={"id": {"S": id}}
        )
        return flask.jsonify(response["Item"])
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500

# GET method to retrieve a single record by name
@app.route("/records/<name>", methods=["GET"])
def get_record_by_name(name):
    """
    Retrieve a single record by name
    """
    try:
        response = ddb_client.get_item(
            TableName=TABLE_NAME,
            Key={"name": {"S": name}}
        )
        return flask.jsonify(response["Item"])
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500

# POST method to create a new record
@app.route("/records", methods=["POST"])
def create_record():
    """
    Create a new record
    """
    try:
        data = flask.request.get_json()
        ddb_client.put_item(
            TableName=TABLE_NAME,
            Item={
                "id": {"S": data["id"]},
                "name": {"S": data["name"]},
                "age": {"N": str(data["age"])}
            }
        )
        return flask.jsonify({"message": "Record created successfully"}), 201
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# PUT method to update a record by ID
@app.route("/records/<id>", methods=["PUT"])
def update_record(id):
    """
    Update a record by ID
    """
    try:
        data = flask.request.get_json()
        ddb_client.update_item(
            TableName=TABLE_NAME,
            Key={"id": {"S": id}},
            UpdateExpression="set name=:n, age=:a",
            ExpressionAttributeValues={
                ":n": {"S": data["name"]},
                ":a": {"N": str(data["age"])}
            },
            ReturnValues="UPDATED_NEW"
        )
        return flask.jsonify({"message": "Record updated successfully"}), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500

# DELETE method to delete a record by ID
@app.route("/records/<id>", methods=["DELETE"])
def delete_record(id):
    """
    Delete a record by ID
    """
    try:
        ddb_client.delete_item(
            TableName=TABLE_NAME,
            Key={"id": {"S": id}}
        )
        return flask.jsonify({"message": "Record deleted successfully"}), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500
