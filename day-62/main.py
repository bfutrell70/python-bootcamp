from dataclasses import fields
import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL(require_tld=True)])
    opening_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closing_time = StringField('Closing Time e.g. 9:30PM', validators=[DataRequired()])
    coffee_rating = StringField('Coffee Rating', validators=[DataRequired()])
    wifi_strength_rating = StringField('WiFi Strength Rating', validators=[DataRequired()])
    power_rating = StringField('Power Rating', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


    
# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")

        def build_rating_string(value, character):
            def is_number(s):
                try:
                    float(s)
                    return True
                except ValueError:
                    return False
            
            if (is_number(value)):
                r = int(value)
                if r > 0:
                    if r > 5:
                        r = 5
                        
                    return character * r
                else:
                    return "✘"

            else:
                return value    

        fields = []
        fields.append(form.cafe.data)
        fields.append(form.cafe_location.data)
        fields.append(form.opening_time.data)
        fields.append(form.closing_time.data)
        fields.append(build_rating_string(form.coffee_rating.data, "☕"))
        fields.append(build_rating_string(form.wifi_strength_rating.data, "💪"))
        fields.append(build_rating_string(form.power_rating.data, "🔌"))

        # Finds the directory where your script is saved
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
        # Joins the script directory with your target file name
        file_path = os.path.join(script_dir, "cafe-data.csv")
    
        with open(file_path, mode="a", newline='', encoding='utf-8') as csv_file:
            csv_file.write(f"{', '.join(fields)}\n")
            pass

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    # Finds the directory where your script is saved
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Joins the script directory with your target file name
    file_path = os.path.join(script_dir, "cafe-data.csv")

    with open(file_path, newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
