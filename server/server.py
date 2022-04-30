from flask import Flask, request, jsonify
import util

app  = Flask(__name__)

# # runs a server on 5000 port and supports an API called hello which returns "hi"
@app.route('/classify_image', methods = ['GET', 'POST'])
def classify_image():
    image_data = request.form['image_data']

    response = jsonify(util.classify_image(image_data))

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == "__main__":
    print("Staring Python Flask Server For Avenger Image Classification")
    util.load_saved_artifacts()
    app.run(port=5000)

# Running the program above outputs "Running on http://127.0.0.1:5000" 
# Helpful website: https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/