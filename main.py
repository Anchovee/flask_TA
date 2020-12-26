from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/administrator/sqlite/example.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primay_key=True)
    state = db.Column(db.String(2))
    name = db.Column(db.String(50))

class Form(FlaskForm):
    state = SelectField('state', choices=[('CA', 'California'), ('NV', 'Nevada')])
    city = SelectField('city', choices=[])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    form.city.choices = [(city.id, city.name) for city in City.query.filter_by(state='CA').all()]

    return render_template('dropdown.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)