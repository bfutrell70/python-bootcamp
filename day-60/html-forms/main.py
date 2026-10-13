from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def receive_data():
    # Do something
    if request.method == 'POST':
        form_data = request.form

        print("Data posted")
        print(form_data)
        print(form_data['username'])
        print(form_data['password'])
    else:
        print("What happened?")

    return render_template("login.html", username=form_data['username'], password=form_data['password'])    

if __name__ == "__main__":
    app.run(debug=True)