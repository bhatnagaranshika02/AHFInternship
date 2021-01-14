from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask('__main__')
db=SQLAlchemy(app)

def dish_serializer(dish):
	return {"dishID":dish.id,
			"dishName":dish.dish_name,
			"dishCost":dish.dish_cost,
			"dishImage":dish.dish_image

			}

class User(db.Model):
    __tablename__ = 'users'

    id=db.Column(
    	db.Integer,
    	primary_key=True)

    username = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False,
    )
    password = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )

    def __init__(self,username,password):
    	self.username=username
    	self.password=password

    def __repr__(self):
        return '<User {}>'.format(self.username)
   
class Dishes(db.Model):

    __tablename__ = 'dishes'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    dish_name = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )

    dish_cost = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )

    dish_image=db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False)

    def __init__(self,dish_name,dish_cost,dish_image):
    	self.dish_name=dish_name
    	self.dish_cost=dish_cost
    	self.dish_image=dish_image

db.create_all()

@app.route('/dishes/<dish_id>',methods=['GET','PUT','DELETE','PATCH'])
@app.route('/dishes',methods=['POST','GET','DELETE'])
def dishes(dish_id=None):
	username=request.headers.get('username')
	password=request.headers.get('password')

	if request.method=="POST":
		dishName = request.form["dishName"]
		dishCost = request.form["dishCost"]
		if request.files:
			dishImage = request.files["dishImage"]
			dishImage.save(os.path.join( dishImage.filename))
			print("Image saved")


		dish=Dishes(dishName,dishCost,dishImage.filename)
		db.session.add(dish)
		db.session.commit()
		return jsonify(dish.id)

	if request.method=="PUT":
		dishName = request.form["dishName"]
		dishCost = request.form["dishCost"]
		dishImage = dishName
		dish=Dishes.query.filter_by(dish_name=dishName).first()
		dish.dish_name=dishName
		dish.dish_cost=dishCost
		dish.dish_image=dishImage
		db.session.commit()
		return jsonify(dish.id)

	if request.method=="GET" and dish_id!=None:
		dish=Dishes.query.filter_by(id=dish_id).first()
		return jsonify(dish_serializer(dish))

	if request.method=="GET" and dish_id==None:
		dish_list=Dishes.query.all()
		dishlist=list(map(dish_serializer,dish_list))
		return jsonify(dishlist)

	if request.method=="DELETE" and dish_id!=None:
		dish=Dishes.query.filter_by(id=dish_id).first()
		dish_id=dish.id
		db.session.delete(dish)
		db.session.commit()
		return jsonify(dish_id)

	if request.method=="DELETE" and dish_id==None:
		dishes=Dishes.query.all()
		id_list=[]
		for dish in dishes:
			id_list.append(dish.id)
			db.session.delete(dish)
		db.session.commit()
		return jsonify(id_list)

	if request.method=="PATCH" and dish_id!=None:
		pass		

'''
def dish_serializer(obj):
	return {"dishName":obj.dish_name,
			"dishCost":obj.dish_cost}

@app.route('/CreateDish',methods=['POST'])
def CreateDish():
	username = request.form["username"]
	password = request.form["password"]
	dishName = request.form["dishName"]
	dishCost = request.form["dishCost"]
	
	dish_obj=Dish(dishName,dishCost)
	dishes[dishName]=dish_obj

	return jsonify('dish created '+dishName)

@app.route('/UpdateDish',methods=['PUT'])
def UpdateDish():
	username = request.form["username"]
	password = request.form["password"]
	dishName = request.form["dishName"]
	dishCost = request.form["dishCost"]
	if dishName in dishes:
		dishes[dishName].dishCost=dishCost
		return jsonify(dishName+"dish Updated")
	else:
		return jsonify("dish not found")

@app.route('/ExistingDish',methods=["GET"])
def ExistingDish():
	username = request.form["username"]
	password = request.form["password"]
	dishName = request.form["dishName"]
	if dishName in dishes:
		return jsonify("Cost is"+dishes[dishName].dishCost)
	else:
		return jsonify("We don't cook this")

@app.route('/DishInfo',methods=['GET'])
def DishInfo():
	username = request.form["username"]
	password = request.form["password"]
	dishlist=list(map(dish_serializer,dishes.values()))
	return jsonify(dishlist)

@app.route('/DeleteDish',methods=['DELETE'])
def DeleteDish():
	username = request.form["username"]
	password = request.form["password"]
	dishName = request.form["dishName"]
	if dishName in dishes:
		dishes.pop(dishName)
		return jsonify("Dish deleted")
	else:
		return jsonify("Dish doesn't exist")

@app.route('/DeleteAll',methods=['DELETE'])
def DeleteAll():
	username = request.form["username"]
	password = request.form["password"]
	l=[]

	if len(dishes)==0:
		return jsonify("No dishes to delete")

	for i in dishes.copy():
		l.append(i)
		dishes.popitem()
		
	return jsonify(l)
'''
app.run()
