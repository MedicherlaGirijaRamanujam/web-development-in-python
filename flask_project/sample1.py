from flask import Flask,redirect,url_for,render_template,request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project_database import Register,Base

engine=create_engine('sqlite:///bvc.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine

DBSession=sessionmaker(bind=engine)
session=DBSession()




app=Flask('__name__')

@app.route("/home")#
def hello():
	return "<h1>hello welcome to bvc college haha</h1>girija"

@app.route("/about")
def about():
		return "about page"

@app.route("/data/<name>")
def data(name):
	name="lallu"
	rollno=68
	return "my name is {} and my rollno is {}".format(name,rollno)

@app.route("/admin")
def admin():
	return "<h2>welcome to admin page</h2>"

@app.route("/student")
def student():
	return "<font color='red'>hello welcome to student page"

@app.route("/faculty")
def faculty():
	return "welcome to faculty data"

@app.route("/person/<uname>/<regdno>")
def person(uname,regdno):
	return render_template("sample1.html",name=uname,regdno=regdno)

@app.route("/user/<name>")
def user(name):
	if name=='admin':
		return redirect(url_for('admin'))
	elif name=='student':
		return redirect(url_for('student'))
	elif name=='faculty':
		return redirect(url_for('faculty'))
	else:
		return "no url found"


@app.route("/table/<int:num>")
def table(num):
	return render_template("table.html",n=num)


dummy_data=[{'name':'lakshman',
'org':'TCS',
'dob':'2jun1997'},

{'name':'girija',
'org':'bvc',
'dob':'1apr2000'}]

@app.route("/show")
def data_show():
	return render_template("show_data.html",d=dummy_data)




@app.route("/Register")
def reg():
	return render_template("register.html")



@app.route("/show_data")
def showData():
	register=session.query(Register).all()
	return render_template('show.html',register=register)



@app.route('/add',methods=["POST","GET"])
def addData():
	if request.method=='POST':
		newData=Register(name=request.form['name'],
		surname=request.form['surname'],
		roll_no=request.form['roll_no'],
		mobile=request.form['mobile'],
		Branch=request.form['Branch'])
		session.add(newData)
		session.commit()
		return redirect(url_for('showData'))
	else:
		return render_template('new.html')


@app.route('/<int:register_id>/edit',methods=["POST","GET"])
def editData(register_id):

	editedData=session.query(Register).filter_by(id=register_id).one()

	if request.method=="POST":
		editedData.name=request.form['name']
		editedData.surname=request.form['surname']
		editedData.roll_no=request.form['roll_no']
		editedData.mobile=request.form['mobile']

		session.add(editedData)
		session.commit()
		return redirect(url_for('showData'))
	else:
		return render_template('edit.html',register=editedData)





@app.route('/<int:register_id>/delete',methods=["POST","GET"])
def deleteData(register_id):

	deletedData=session.query(Register).filter_by(id=register_id).one()
	if request.method=="POST":

		session.delete(deletedData)
		session.commit()
		return redirect(url_for('showData',register_id=register_id))
	else:
		return render_template('delete.html',register=deletedData)










if __name__ == '__main__':
	app.run(debug=True)