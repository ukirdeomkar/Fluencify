import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# Create flask app
flask_app = Flask(__name__)
model = pickle.load(open("./mlp_300_32.sav", "rb"))

@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route("/predict", methods = ["POST"])
def predict():
    # float_features = [float(x) for x in request.form.values()]
    float_features = []
    for i in request.form.values():
        float_features.append(int(i))
    

    float_features = [float_features]
    features = np.array(float_features)
    # print("\n \nThe Shape of Features is " , features.shape , "\n\n")
    # print("\n \nThe Length of Float Features is " , len(float_features) , "\n\n")

    # print(features)
    prediction = model.predict(float_features)
    # i = np.argmax(prediction[0])
    return render_template("index.html", prediction_text = "The Fluency Level is {}".format(i+1))

if __name__ == "__main__":
    flask_app.run(debug=True)