from flask import jsonify

def success_response(message="Success", data=None, status=200):
    response = {
        "status": "success",
        "message": message
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status

def error_response(message="Internal Server Error", status=500):
    response = {
        "status": "error",
        "message": message
    }
    return jsonify(response), status

def not_found_response(message="Not Found"):
    return error_response(message, 404)

def user_created_response(user_id):
    message = f"User {user_id} created successfully"
    return success_response(message=message, data={"user_id": user_id})

def user_deleted_response(user_id):
    message = f"User {user_id} deleted successfully"
    return success_response(message=message, data={"user_id": user_id})
