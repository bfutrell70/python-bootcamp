from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    # return render_template("index.html")
    return render_template("brian.html")

# if this file is run as a script perform a task
if __name__ == "__main__":
    app.run(debug=True)