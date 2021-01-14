def dish_serializer(obj):
        return {"dishName":obj.dish_name,"\t dishCost":obj.dishCost}
        
@app.route('/CreateDish',methods=['POST'])
def CreateDish():
	
	dishName = request.form["dishName"]
	dishCost = request.form["dishCost"]
	
#image (body)
	dish_obj=Dish(dishName,dishCost)
	dishes[dishName]=dish_obj

	return jsonify('dish created : '+ dishName)

@app.route('/UpdateDish',methods=['PUT'])
def UpdateDish():
	username = request.form["username"]
	password = request.form["password"]
	dishName = request.form["dishName"]
	dishCost = request.form["dishCost"]
	if dishName in dishes:
		    dishes[dishName].dishCost=dishCost
            return jsonify(dishName+'Updated')
	else:
		    return "dish not found."

@app.route('/ExistingDish',methods=["GET"])
def ExistingDish():
	username = request.form["username"]
	password = request.form["password"]
	dishName = request.form["dishName"]
	if dishName in dishes:
                a = dishes[dishName].dishCost
                return jsonify("Cost is:"+a)
    return jsonify("We dont cook this")

@app.route('DishInfo',methods=['GET'])
def DishInfo():
	username = request.form["username"]
	password = request.form["password"]
	dishList = list(map(dish_serializer,dishes.values()))
	return jsonify(dishList)
	

@app.route('/DeleteDish',methods=['DELETE'])
def DeleteDish():
	username = request.form["username"]
	password = request.form["password"]
	dishName = request.form["dishName"]
	if dishName in dishes:
                dishes.pop(dishName)
                return "dish deleted"

@aoo.route('/deleteAll',methods=["DELETE"])
def DeleteAll():
        username = request.form["username"]
	    password = request.form["password"]
	    l=[]
	    if len(dishes)==0:
            return "No dishes to delete."
	    for i in dishes:
            l.append(i)
            dishes.pop(i)
        return jsonify(l)

        

app.run()
