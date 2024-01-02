from flask import Flask, request, render_template, session

from models import Session, House,Region,User,City,User_house
from predict_house_price import predict_house_price

app = Flask(__name__)
app.config['SECRET_KEY']='1234'



@app.route('/')
def start():
    db = Session()
    city=db.query(City).all()
    db.close()
    return render_template("estimate.html", city=city)

@app.route("/about_us")
def about_us():
    return render_template('about_us.html')

@app.route('/register')
def register():
   return render_template('register.html')

@app.route('/user_save', methods=["post"])
def user_save():
    db = Session()
    fname = request.form["first_name"]
    lname = request.form["last_name"]
    phn = request.form["phone"]
    eml = request.form["email"]
    c = User(first_name=fname, last_name=lname, phone=phn, email=eml)
    db.add(c)
    db.commit()
    db.close()
    return render_template('apartment_estimate.html')

@app.route('/house1', methods=["post"])
def house1():
    db=Session()
    t_bargain = request.form["bargain_type"]
    session["t_bargain"] = t_bargain
    t_house = request.form["house_type"]
    session["t_house"]=t_house
    city = request.form["city_id"]
    session["city"] = city
    region=db.query(Region).filter(Region.city==session["city"]).all()

    db.close()
    return render_template('apartment_estimate1.html',region=region, house_type= t_house,bargain_type=t_bargain,city=city)



@app.route('/house_save', methods=["post"])
def house_save():
    db = Session()
    t_bargain = request.form["bargain_type"]
    t_house = request.form["house_type"]
    city = request.form["city_id"]
    region = request.form["region_id"]
    area = request.form["area"]
    building_year = request.form["bargain_type"]
    title_deeds =  1 #request.form["elevator"]
    floor = 1 #request.form["elevator"]
    unit_per_floor = 1 #request.form["elevator"]
    total_unit = 1 #request.form["elevator"]
    elevator = 1 #request.form["elevator"]
    parking = 1 #request.form["elevator"]
    store_room = 1 #request.form["elevator"]
    price =  predict_house_price(area,region)
    c = User_house(house_type=session["t_house"], bargain_type=session["t_bargain"],city_id= session["city"],region_id=region,area=area,building_year=building_year,floor=floor, title_deeds=title_deeds,elevator=elevator,parking=parking,store_room=store_room,unit_per_floor=unit_per_floor,total_unit=total_unit,price=price)
    db.add(c)
    db.commit()
    db.close()
    return render_template('apartment_estimate2.html',t_house=t_house, t_bargain=t_bargain,city=city,region=region,area=area,building_year=building_year,title_deeds=title_deeds,floor=floor,unit_per_floor=unit_per_floor,total_unit=total_unit,elevator=elevator,parking=parking,store_room=store_room,price=price)


@app.route('/house_image')
def house_image():
    with open('img1.jpg', 'rb') as f:
        return f.read()


@app.route('/api/regions')
def regions_api():
    city_id = request.args.get('city_id')
    db = Session()
    city = db.query(City).filter(City.id == city_id).one()
    regions = db.query(Region).filter(Region.city == city.name).all()
    result = [{'id': r.id, 'title': r.name} for r in regions]
    return result


@app.route('/api/calculate')
def calculate_api():
    city_id = request.args.get('city_id')
    region_id = request.args.get('region_id')
    area = int(request.args.get('area'))
    building_year = request.args.get('building_year')
    floor = request.args.get('floor')
    title_deeds = request.args.get('title_deeds')
    elevator = request.args.get('elevator')
    parking = request.args.get('parking')
    store_room = request.args.get('store_room')
    result = predict_house_price(area, region_id)
    return {'price': result}


if __name__ == '__main__':
    app.run(host='0.0.0.0')
