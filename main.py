from flask import Flask, render_template
from forms import centralForm

app = Flask(__name__)

# security measure to prevent against forgery attacks
app.config['SECRET_KEY'] = '87895ec872aed029e6073ef018ba980c'

data = [
    {'key': 'result'}
]

@app.route("/")
def homeFun():
    return render_template('home.html', data=data)

@app.route("/query")
def queryFun():
    form = centralForm()
    return render_template('query.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)