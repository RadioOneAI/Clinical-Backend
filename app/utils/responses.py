from flask import jsonify

def ok(data=None, message="OK", code=200):
    return jsonify({"success": True, "message": message, "data": data}), code

def fail(message="Error", errors=None, code=400):
    payload = {"success": False, "message": message}
    if errors is not None:
        payload["errors"] = errors
    return jsonify(payload), code
