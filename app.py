from flask import Flask,render_template,request,url_for,flash,redirect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_migrate import Migrate
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from datetime import datetime
app=Flask(__name__)


app.config['SECRET_KEY']="secret key!!!"
app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://root:hello@localhost/connect2serve_db_1'
db=SQLAlchemy(app)
migrate= Migrate(app,db)



login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False,unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(10000), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    ph_no = db.Column(db.String(20), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    events = db.relationship('Events', backref='user')
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash , password)


class Events(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_address = db.Column(db.String(300), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    event_url = db.Column(db.String(300), nullable=False)
    event_date = db.Column(db.String(10), nullable=False)
    event_time = db.Column(db.String(10), nullable=False)
    about_event= db.Column(db.Text(1000),nullable=False)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username=request.form.get('user_name')
        email=request.form.get('email')
        password=request.form.get('password')
        role=request.form.get('role')
        district=request.form.get('district')
        ph_no=request.form.get('ph_no')
        user=Users.query.filter_by(username=username).first()
       
        if user is None:
            hashed=generate_password_hash(password,"sha256")
            data= Users(username=username,email=email,password_hash=hashed,role=role,district=district,ph_no=ph_no)
            db.session.add(data)
            db.session.commit()
            #  flash('Account created successfully')
            return redirect(url_for('home'))

        else:
            #  flash('There is some error. Try again...')
            return render_template('home.html')
            

    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('user_name')
        password=request.form.get('password')
        user=Users.query.filter_by(username=username).first()
        if user :
            if  check_password_hash(user.password_hash,password):
                login_user(user)
                return render_template('home.html')
                
            else:
                # flash('worng password')
                return redirect(url_for('home'))
        else:
            # flash("user doesn't exist!")
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("you have been logged out")
    return redirect(url_for('home'))


@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html',)

@app.route('/delete/<int:id>',methods=['POST','GET'])
@login_required
def delete(id):
    if id==current_user.id:    
        delete=Users.query.get_or_404(id)
        try:
            db.session.delete(delete)
            db.session.commit()
            logout_user()
            return render_template('home.html')
        except:
            return redirect(url_for('dashboard'))
    return render_template('dashboard.html')


@app.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id):
    name_update=Users.query.get_or_404(id)
    if request.method=="POST":

        name_update.password=request.form.get('password')
        name_update.ph_no=request.form.get('ph_no')
        name_update.district=request.form.get('district')

        try:
            db.session.commit()
            return redirect(url_for('dashboard')) 
        except:
            return render_template('update.html',id=id)
    return render_template('update.html',id=id)

@app.route('/events',methods=['POST','GET'])
def events_page():
    events_=Events.query.order_by(Events.event_date)
    return render_template('events.html',events=events_)

@app.route('/about')
def about():
    return render_template('about.html')
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html") , 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html") , 500

if __name__=='__main__':
    app.run(debug=True)