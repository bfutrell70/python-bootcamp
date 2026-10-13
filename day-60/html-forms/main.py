from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def receive_data():
    form_data = request.form
    return render_template("login.html", username=form_data['username'], password=form_data['password'])    

if __name__ == "__main__":
    app.run(debug=True)