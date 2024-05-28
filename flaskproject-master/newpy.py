from flask import Blueprint


blueprint = Blueprint("courses", __name__, template_folder="templates", static_folder="static")

@blueprint.route("/")
def index():
    return "Hello World"

