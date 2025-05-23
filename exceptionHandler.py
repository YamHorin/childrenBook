from flask import jsonify

def exception_json_value(exception):
    return jsonify({"error": f"Missing required field: {str(exception)}"}), 400 
def exception_no_json():
    return jsonify({"error": "No JSON data provided"}), 400  # Handle missing JSON
def exception_internal_server_issue(exception):
    return jsonify({"error of the server": f"server crash: {exception}"}), 500 