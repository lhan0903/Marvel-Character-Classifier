from flask import Flask, request, jsonify

app  = Flask(__name__)

# # runs a server on 5000 port and supports an API called hello which returns "hi"
# @app.route('/classify_image', methods = ['GET', 'POST'])
# def classify_image():
#     return "hi"

@app.route('/hello/<name>')
def hello(name):
    return "HI" + name


if __name__ == "__main__":
    app.run(port=5000)

# Running the program above outputs "Running on http://127.0.0.1:5000" 
# Helpful website: https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/