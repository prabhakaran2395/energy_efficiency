import os
from flask import Flask
from flask.globals import request
from flask.templating import render_template
from prediction_service import prediction

webapp_root = "webapp"
params_path = "params.yaml"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if request.form:
                data = dict(request.form)
                responses = prediction.form_response(data)
                response_1 = round(responses[0], 2)
                response_2 = round(responses[1], 2)
                return render_template("index.html", response={'Heating load': response_1,
                                                               'Cooling load': response_2})

            else:
                pass

        except Exception as e:
            error = {"error": e}
            return render_template("404.html", error=error)

    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5556, debug=False)
