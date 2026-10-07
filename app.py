from flask import Flask, request, redirect, session
import os, datetime, json

app = Flask(__name__)
app.secret_key = "eazymade-final-logo"
OFFICE_PASS = "0116782556"

users = {
    "admin": {"name":"John Thuo","phone":"0116782556","role":"admin","till":"0116782556","password":"0116782556","shop":"Rongai Shoe Center","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=365),"lat":-1.3956,"lng":36.7562,"area":"Rongai Town"}
}
products = [
    {"id":1,"name":"Jordan 1","price":4500,"image":"https://images.unsplash.com/photo-1600269452121-4f2416e55c28?w=500","seller":"admin","shop":"Rongai Shoe Center","stock":10,"lat":-1.3956,"lng":36.7562},
]
shops = {
    "Rongai Shoe Center": {"owner":"admin","till":"0116782556","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=30),"lat":-1.3956,"lng":36.7562,"area":"Rongai Town, Magadi Road"}
}

def ok(u):
    x = users.get(u)
    if not x:
        return False
    return x.get("approved") and datetime.datetime.now() < x.get("expiry")

STYLE = "<style>body{font-family:Arial;margin:0;background:#f0f2f5}.card{background:white;border-radius:12px;padding:12px;margin:8px;box-shadow:0 2px 8px #ddd}.btn{padding:11px;border-radius:8px;width:100%;margin-top:6px;font-weight:bold;border:none}.btn-o{background:#f68b1e;color:white}.btn-b{background:#000;color:white}.btn-g{background:green;color:white}.small{font-size:11px;color:#666}input,select{width:100%;padding:11px;margin:5px 0;border-radius:8px;border:1px solid #ddd}#map{height:380px;border-radius:12px}</style>"

HEADER = "<div style=background:#000;color:#0f0;padding:4px;text-align:center;font-size:10px>ARTIFICIAL MARKET - Till 0116782556</div><div style=background:#f68b1e;padding:10px;display:flex;justify-content:space-between;align-items:center><div style=display:flex;align-items:center;gap:8px><div style=background:white;color:#f68b1e;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold>E</div><b style=color:white>EAZYMADE</b></div><div style=color:white;font-size:12px><a href=/map style=color:white>Map</a> | <a href=/ style=color:white>Market</a> | <a href=/office style=color:white>Office</a></div></div>"

@app.route("/")
def home():
    h = STYLE + HEADER
    h += "<div style=background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:18px;border-radius:12px;margin:8px;text-align:center><div style=background:white;color:#f68b1e;width:60px;height:60px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:bold;margin:0 auto>E</div><h2>EAZYMADE ARTIFICIAL MARKET</h2><p>See whole shop stock BEFORE you go - Real GPS - Logo E</p><a href=/map><button class=btn style=background:white;color:#f68b1e>VIEW MARKET MAP - Real GPS</button></a><a href=/register><button class=btn style=background:black;color:white>Everyone Register</button></a></div>"
    h += "<div class=card><h3>Shops - Enter Whole Shop (Your Aim)</h3>"
    for sname, sinfo in shops.items():
        if not ok(sinfo['owner']):
            continue
        h += "<div class=card style=border-left:5px solid #f68b1e><b>" + sname + "</b> - Whole Shop 10 pairs<br><span class=small>" + sinfo['area'] + " | GPS " + str(sinfo['lat']) + " Till " + sinfo['till'] + "</span><br><a href=/shop/" + sinfo['owner'] + "><button class=btn style=background:#f68b1e;color:white>Enter Whole Shop - See All Stock</button></a><a href=https://www.google.com/maps?q=" + str(sinfo['lat']) + "," + str(sinfo['lng']) + " target=_blank><button class=btn style=background:#000;color:white>GPS Navigate</button></a></div>"
    h += "</div>"
    return h

@app.route("/map")
def map_page():
    h = STYLE + HEADER + "<div class=card><h2>Real Kenya GPS Map</h2><div id=map></div></div><link rel=stylesheet href=https://unpkg.com/leaflet@1.9.4/dist/leaflet.css><script src=https://unpkg.com/leaflet@1.9.4/dist/leaflet.js></script><script>var map=L.map('map').setView([-1.3956,36.7562],14);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);L.marker([-1.3956,36.7562]).addTo(map).bindPopup('Rongai Shoe Center - Whole Shop');</script><div class=card><b>Rongai Shoe Center</b> - 10 pairs - <a href=/shop/admin><button class=btn style=background:#f68b1e;color:white>Enter Shop</button></a> <a href=https://www.google.com/maps?q=-1.3956,36.7562 target=_blank><button class=btn style=background:#000;color:white>Navigate GPS</button></a></div>"
    return h

@app.route("/shop/<seller>")
def shop_one(seller):
    u = users.get(seller,{})
    sname = u.get("shop","Shop")
    info = shops.get(sname,{})
    h = STYLE + HEADER
    h += "<div style=background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:15px;border-radius:12px;margin:8px><h2>" + sname + " - WHOLE SHOP HOSTING</h2><p>View BEFORE you go - Total pairs available - Logo E</p><p>GPS " + str(info.get("lat","")) + " | Till " + u.get("till","") + " (Pay seller directly)</p></div>"
    h += "<div class=card><a href=https://www.google.com/maps?q=" + str(info.get("lat",-1.3956)) + "," + str(info.get("lng",36.7562)) + " target=_blank><button class=btn style=background:#000;color:white>Open GPS in Google Maps - Real Navigation</button></a></div>"
    return h

@app.route("/register", methods=["GET","POST"])
def reg():
    if request.method=="POST":
        uname = request.form["username"].lower()
        role = request.form["role"]
        lat = float(request.form["lat"] or -1.3956)
        lng = float(request.form["lng"] or 36.7562)
        exp = datetime.datetime.now() + datetime.timedelta(days=30)
        users[uname] = {"name":request.form["fullname"],"phone":request.form["phone"],"role":role,"till":request.form["till"],"password":request.form["password"],"shop":request.form["shop"],"approved":False,"expiry":exp,"lat":lat,"lng":lng,"area":request.form["area"]}
        shops[request.form["shop"]] = {"owner":uname,"till":request.form["till"],"approved":False,"expiry":exp,"lat":lat,"lng":lng,"area":request.form["area"]}
        return redirect("/")
    h = STYLE + HEADER + "<div class=card style=max-width:500px;margin:20px auto><h2>Register - Everyone + Logo + GPS + Till</h2><form method=post>Name:<input name=fullname required>Phone:<input name=phone required>Username:<input name=username required>Password:<input name=password type=password required>Role:<select name=role><option value=buyer>Buyer</option><option value=seller>Seller - Own Till + GPS + Whole Shop</option></select>Shop Name:<input name=shop required>Till (customers pay YOU):<input name=till required>Area:<input name=area>Lat:<input name=lat id=lat value=-1.3956 required>Lng:<input name=lng id=lng value=36.7562 required><button type=button class=btn style=background:#000;color:white onclick=navigator.geolocation.getCurrentPosition(function(p){document.getElementById('lat').value=p.coords.latitude;document.getElementById('lng').value=p.coords.longitude;})>Get My Current GPS Location</button><button class=btn style=background:green;color:white>Register</button></form></div>"
    return h

@app.route("/office", methods=["GET","POST"])
def office():
    if request.method=="POST":
        if request.form.get("password")!="0116782556":
            return "Wrong"
        session["office"]=True
    if not session.get("office"):
        return STYLE+HEADER+"<div class=card style=max-width:400px;margin:40px auto><h2>Office - Logo E</h2><form method=post><input name=password type=password placeholder=0116782556><button class=btn style=background:#000;color:white>Enter</button></form></div>"
    h = STYLE+HEADER+"<div class=card><h2>Office - Till 0116782556 - Logo E</h2>"
    for sname, info in shops.items():
        h += "<div class=card>" + sname + " Till " + info["till"] + " GPS " + str(info["lat"]) + " - Approved</div>"
    h += "</div>"
    return h

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
