#import all necessary libraries
from flask import Flask
from flask import render_template, redirect


app = Flask(__name__)

#import flask sqlalchemy
from flask_sqlalchemy import SQLAlchemy

database_file = "sqlite:///iphones.db"

app.config["SQLALCHEMY_DATABASE_URI"]=database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Iphone(db.Model):
    __tablename__="iphones_tbl"
    id_num = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    #id_num = db.Column(db.String(10), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(200))
    camera = db.Column(db.String(200))
    display = db.Column(db.String(200))
    price = db.Column(db.String(200))
    processor = db.Column(db.String(200))
    rating = db.Column(db.String(200))
    rom = db.Column(db.String(200))
        
    def __repr__(self):
        result_set="<SN: {}>".format(self.id_num)+"<Name: {}>".format(self.name)+",<Camera: {}>".format(self.camera)+",<Display: {}>".format(self.display)+",<Price: {}>".format(self.price)+",<Processor: {}>".format(self.processor)+",<Rating: {}>".format(self.rating)+",<Rom: {}>".format(self.rom)
        return result_set
        
#create the dab and tables    
db.create_all()

#upload scrapped data into db
import sqlalchemy as sa
import pandas as pd
con = sa.create_engine('sqlite:///iphones.db', convert_unicode=True)
chunks = pd.read_csv('iphones_flipkart.csv', chunksize=100000)
for chunk in chunks:
    chunk.to_sql(name='iphones_tbl', if_exists='append', index=False, con=con)

from flask import request

#home page
@app.route("/", methods = ["GET", "POST"])
def home(page=1):
    per_page=50
    
    if request.form:
        iphone = Iphone()
        iphone.id_num = request.form.get("id_num")
        iphone.name = request.form.get("name")
        iphone.camera = request.form.get("camera")
        iphone.display = request.form.get("display")
        iphone.price = request.form.get("price")
        iphone.processor = request.form.get("processor")
        iphone.rating = request.form.get("rating")
        iphone.rom = request.form.get("rom")
        db.session.add(iphone)
        db.session.commit()
    
    iphones = Iphone.query.order_by(Iphone.id_num.desc()).paginate(page,per_page,error_out=False)
    return render_template("home.html", iphones=iphones)

#delete a record from database    
@app.route("/delete", methods=["GET", "POST"])
def delete():
    id_num = request.form.get("id_num")
    iphone=Iphone.query.filter_by(id_num=id_num).first()
    db.session.delete(iphone)
    db.session.commit()
    return redirect("/")

#update a record in a database
@app.route("/update", methods=["GET", "POST"])
def update():
    id_num = request.form.get("id_num")
    iphone=Iphone.query.filter_by(id_num=id_num).first()
    if iphone:
        return render_template('edit.html', iphone=iphone)
    else:
        return 'Error loading #{id_num}'.format(id_num=id_num)

#save updated chages into database
@app.route("/save_changes", methods=["GET", "POST"])
def save_changes(page=1):
    per_page=50
    if request.form:
        id_num = request.form.get("id_num")
        iphone=Iphone.query.filter_by(id_num=id_num).first()
        #iphone.id_num = request.form.get("id_num")
        iphone.name = request.form.get("newname")
        iphone.camera = request.form.get("newcamera")
        iphone.display = request.form.get("newdisplay")
        iphone.price = request.form.get("newprice")
        iphone.processor = request.form.get("newprocessor")
        iphone.rating = request.form.get("newrating")
        iphone.rom = request.form.get("newrom")
        #db.session.add(iphone)
        db.session.commit()
    
    iphones = Iphone.query.order_by(Iphone.id_num.desc()).paginate(page,per_page,error_out=False)
    return render_template("home.html", iphones=iphones)
    #iphones = Iphone.query.all()
    #return render_template("home.html", iphones=iphones)
    
#run the application
if __name__=="__main__":
    app.run(debug=True)