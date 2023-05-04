from flask import Flask, render_template, redirect, url_for, flash
from forms import centralForm, addCompanyForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

import keyword, random

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


def multQueries(sql):
    result = ''  
    queries = sql.split(';')

    app.logger.debug('SQL Being run: ' + sql)

    if queries[-1]=='':
        queries = queries[:-1]  # get rid of the last empty element caused due to splitting

    for query in queries:
        query += ';' # add semicolon to each query
        query = text(query)
        if result=='':
            try:
                result = db.session.execute(query)
            except SQLAlchemyError as e:
                return "ERROR"
        else:
            try:
                db.session.execute(query)
            except SQLAlchemyError as e:
                return "ERROR"
    
    db.session.commit()

    return result

SQLKeywords = ['SELECT', 'FROM', 'WHERE', 'HAVING', 'DROP', 'TABLES', 'INSERT',
               '1=1', 'OR', 'DELETE', 'UPDATE', 'UNION', 'TRUNCATE']

def isSQLKeyword(word):    
    if keyword.iskeyword(word.upper()) or word.upper() in SQLKeywords:
        return True
    else:
        return False

def createKeyAppendedKeywords(key):
    appendedKeys = []
    for keyW in SQLKeywords:
        appendedKeys.append(keyW + str(key))

    return appendedKeys

def modifySQL(sql, newSQLKeywords):
    newSQL=""

    for word in sql.split(' '):
        if word.upper() in SQLKeywords:
            newSQL = newSQL + newSQLKeywords[SQLKeywords.index(word)] + ' '
        elif(word==';'):
            newSQL = newSQL + ";"
            break
        else:
            newSQL = newSQL + word + ' '
    
    app.logger.debug(f"modSQL: from --{sql}-- to --{newSQL}--")

    return newSQL

def checkStatus(sql):
    for word in sql.split(' '):
        word = word.strip("'")
        word = word.strip(";")
        app.logger.debug('STATUS CHEK: ' + "-" + word + "-")
        if word.upper() in SQLKeywords:
            return "bad"
        
    return "clear"

def cleanSQL(sql, newSQLKeywords):
    cleanSQL=""

    for word in sql.split(' '):
        if word.upper() in newSQLKeywords:
            cleanSQL = cleanSQL + SQLKeywords[newSQLKeywords.index(word)] + ' '
        elif(word==';'):
            newSQL = newSQL + ";"
            break
        else:
            cleanSQL = cleanSQL + word + ' '
    
    app.logger.debug(f"CLEANSQL: from --{sql}-- to --{cleanSQL}--")

    return cleanSQL

data = [] # remove at end.

@app.route("/")
def home():
    return render_template('home.html', data=data)

@app.route("/query", methods=['GET', 'POST'])
def query():
    form = centralForm()

    if form.validate_on_submit():
        sql = f"SELECT * FROM Company WHERE cmpName LIKE '{form.cmpName.data}'"
        results = multQueries(sql) 

        return render_template('query.html', form=form, results=results)

    return render_template('query.html', form=form)

@app.route("/protectedQuery", methods=['GET', 'POST'])
def protectedQuery():

    key = random.randint(100,999)
    newKeywords = createKeyAppendedKeywords(key)

    form = centralForm()

    if form.validate_on_submit():
        sql = "SELECT * FROM Company WHERE cmpName LIKE '{}'"
        sql = modifySQL(sql, newKeywords)
        app.logger.debug(sql)

        sql = sql.format(form.cmpName.data)
        status = checkStatus(sql)
        app.logger.debug(status)

        if status=="bad":
            return render_template('query.html', form=form, status=status)
        # else status is "clear"
        sql = cleanSQL(sql, newKeywords)
        app.logger.debug(sql)
        results = multQueries(sql)
        if type(results)== str and results == "ERROR":
            render_template('query.html', form=form, status="ERROR")

        return render_template('query.html', form=form, results=results, status=status)

    return render_template('query.html', form=form)

@app.route("/workingQuery", methods=['GET', 'POST'])
def workingQuery():
    form = centralForm()

    if form.validate_on_submit():
        results = Company.query.filter_by(cmpName=form.cmpName.data).all()

        return render_template('query.html', form=form, results=results)

    return render_template('queryNEW.html', form=form)

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

'''
sql =
... SELECT * FROM Company;
... INSERT INTO Company (cmpName, phoneNo, address)
... VALUES ('TESETET', "232357232", "addddr");
...
TEST'; INSERT INTO Company (cmpName, phoneNo, address) VALUES ('erhbfher', "27777772", "addr"); --
'''