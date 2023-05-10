from flask import Flask,render_template,request,url_for,flash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)


app.config['SECRET_KEY']="secret key!!!"
app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://root:hello@localhost/connect2serve_db_1'
db=SQLAlchemy(app)




class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    ph_no = db.Column(db.String(20), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    events = db.relationship('Events', backref='user', lazy=True)

class Events(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_address = db.Column(db.String(300), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    event_url = db.Column(db.String(300), nullable=False)
    event_date = db.Column(db.String(10), nullable=False)
    event_time = db.Column(db.String(10), nullable=False)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username=request.form.get('user_name')
        email=request.form.get('email')
        password=request.form.get('password')
        role=request.form.get('role')
        district=request.form.get('district')
        ph_no=request.form.get('ph_no')
        validate=Users.query.filter_by(email=email).first()
       
        if validate is None:
            data= Users(username=username,email=email,password=password,role=role,district=district,ph_no=ph_no)
            db.session.add(data)
            db.session.commit()

            return "created "

        else:
            return "not created"

    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('user_name')
        password=request.form.get('password')
        email=request.form.get('email')
        validate=Users.query.filter_by(email=email).first()
        if validate :
            username_check = Users.query.filter_by(username=username).first()
            password_check= Users.query.filter_by(password=password).first()
            if username_check and password_check:
                return "logged in"
            else:
                return "not logged in"
    return render_template('index.html')




if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)