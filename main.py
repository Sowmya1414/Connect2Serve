from flask import Flask,render_template,request,url_for

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username=request.form.get('user_name')
        email=request.form.get('email')
        password=request.form.get('password')
        role=request.form.get('role')
        district=request.form.get('district')
        k=username+" "+email+ " " + password+" "+role+" "+district
        return k
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True)