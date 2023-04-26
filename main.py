from flask import Flask, render_template, redirect, url_for, flash
from forms import centralForm, addCompanyForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# security measure to prevent against forgery attacks
app.config['SECRET_KEY'] = '87895ec872aed029e6073ef018ba980c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
app.app_context().push()    # required for db commands for flask in python

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cmpName = db.Column(db.String(50), nullable=False)
    phoneNo = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Company('{self.cmpName}', '{self.phoneNo}', '{self.address}')"

# dummy Data: ;to remove
data = [
    {'key': 'result'}
]

@app.route("/")
def home():
    return render_template('home.html', data=data)

@app.route("/query", methods=['GET', 'POST'])
def query():
    form = centralForm()

    if form.validate_on_submit():
        results = Company.query.filter_by(cmpName=form.cmpName.data).all()

        return render_template('query.html', form=form, results=results)

    return render_template('query.html', form=form)

@app.route("/protectedQuery", methods=['GET', 'POST'])
def protectedQuery():
    form = centralForm()

    if form.validate_on_submit():
        results = Company.query.filter_by(cmpName=form.cmpName.data).all()

        return render_template('query.html', form=form, results=results)

    return render_template('query.html', form=form)

@app.route("/modDB", methods=['GET', 'POST'])
def modDB():
    form = addCompanyForm()

    if form.validate_on_submit():
        newCmp = Company(cmpName=form.cmpName.data,
                            phoneNo=form.phoneNo.data,
                            address=form.address.data
                            )
        db.session.add(newCmp)
        db.session.commit()
        # flash(f'{newCmp.cmpName} added to database') # functionality not added

        return redirect(url_for('modDB'))

    return render_template('modDB.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)