import os
from flask import Flask
from flask.globals import request
from flask.templating import render_template
import yaml
import joblib
from prediction_service import prediction

webapp_root = "webapp"
params_path = "params.yaml"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
        return config

def predict(data):
    config = read_params(params_path)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)
    prediction = model.predict(data)
    return prediction

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form:
            data = dict(request.form)
            # data = [list(map(float, data))]
            responses = prediction.form_response(data)
            response_1 = round(responses[0], 2)
            response_2 = round(responses[1], 2)
            return render_template("index.html", response={'Heating load':response_1,
                                    'Cooling load':response_2})
            
            
        else:
            pass

    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5556, debug=True)
