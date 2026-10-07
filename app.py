from flask import Flask, request, redirect, session
import os, datetime

app = Flask(__name__)
app.secret_key = "v14-big-font"
OFFICE_PASS = "0116782556"

users = {
    "admin": {"name":"John Thuo","phone":"0116782556","role":"admin","till":"0116782556","password":"0116782556","shop":"Rongai Shoe Center","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=365),"lat":-1.3956,"lng":36.7562,"area":"Rongai Town"}
}
products = [
    {"id":1,"name":"Jordan 1","price":4500,"image":"https://images.unsplash.com/photo-1600269452121-4f2416e55c28?w=500","seller":"admin","shop":"Rongai Shoe Center","stock":10,"size":"42","lat":-1.3956,"lng":36.7562},
]
shops = {
    "Rongai Shoe Center": {"owner":"admin","till":"0116782556","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=30),"lat":-1.3956,"lng":36.7562,"area":"Rongai Town, Magadi Road"}
}

def ok(u):
    x = users.get(u)
    if not x:
        return False
    return x.get("approved") and datetime.datetime.now() < x.get("expiry")

STYLE = "<style>body{font-family:Arial;margin:0;background:#f0f2f5;padding-bottom:80px;font-size:16px}h2{font-size:24px}h3{font-size:20px}b{font-size:17px}.card{background:white;border-radius:14px;padding:14px;margin:10px;box-shadow:0 2px 8px #ddd;font-size:16px}.btn{padding:14px;border-radius:10px;width:100%;margin-top:8px;font-weight:bold;border:none;font-size:16px}.btn-o{background:#f68b1e;color:white;font-size:17px}.btn-b{background:#000;color:white;font-size:17px}.btn-g{background:green;color:white;font-size:17px}.small{font-size:14px;color:#666}input,select{width:100%;padding:14px;margin:6px 0;border-radius:10px;border:1px solid #ddd;font-size:16px}#map{height:420px;border-radius:14px}.bottom-nav{position:fixed;bottom:0;left:0;right:0;background:white;border-top:2px solid #f68b1e;display:flex;justify-content:space-around;padding:10px 0;z-index:2000;box-shadow:0 -2px 10px #ccc}.nav-item{text-align:center;font-size:13px;font-weight:bold;color:#000;text-decoration:none}.nav-item.active{color:#f68b1e}.nav-icon{font-size:24px;display:block}</style>"

HEADER = "<div style=background:#000;color:#0f0;padding:6px;text-align:center;font-size:12px>ARTIFICIAL MARKET - Till 0116782556 - Logo E</div><div style=background:#f68b1e;padding:12px;display:flex;justify-content:space-between;align-items:center><div style=display:flex;align-items:center;gap:10px><div style=background:white;color:#f68b1e;width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:22px>E</div><div><b style=color:white;font-size:20px>EAZYMADE</b><br><span style=color:white;font-size:12px>Artificial Market</span></div></div><div style=color:white;font-size:14px><a href=/office style=color:white;text-decoration:none>Office</a></div></div>"

BOTTOM = "<div class=bottom-nav><a href=/ class=nav-item><span class=nav-icon>🏪</span>Market</a><a href=/map class=nav-item><span class=nav-icon>📍</span>GPS Map</a><a href=/post class=nav-item><span class=nav-icon>📸</span>Post Stock</a><a href=/register class=nav-item><span class=nav-icon>👤</span>Register</a></div>"

@app.route("/")
def home():
    h = STYLE + HEADER
    h += "<div style=background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:22px;border-radius:14px;margin:10px;text-align:center><div style=background:white;color:#f68b1e;width:70px;height:70px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:bold;margin:0 auto>E</div><h2 style=font-size:26px;margin:10px 0>EAZYMADE ARTIFICIAL MARKET</h2><p style=font-size:17px>See whole shop stock BEFORE you go - Real GPS - Big Font</p><button class=btn style=background:white;color:#f68b1e;font-size:18px onclick=window.location.href='/map'>VIEW MARKET MAP - Real GPS</button><button class=btn style=background:black;color:white;font-size:18px onclick=window.location.href='/register'>Everyone Register - Buyer/Seller</button></div>"
    h += "<div class=card><h3 style=font-size:22px>🏬 Shops - Enter Whole Shop (Your Aim)</h3>"
    for sname, sinfo in shops.items():
        if not ok(sinfo['owner']):
            continue
        cnt = len([p for p in products if p["shop"]==sname])
        tot = sum([p["stock"] for p in products if p["shop"]==sname])
        h += "<div class=card style=border-left:6px solid #f68b1e><b style=font-size:19px>" + sname + "</b><br><span style=font-size:16px>" + str(cnt) + " types | " + str(tot) + " pairs in stock</span><br><span class=small style=font-size:14px>" + sinfo['area'] + " | GPS " + str(sinfo['lat']) + " | Till " + sinfo['till'] + "</span><br><a href=/shop/" + sinfo['owner'] + "><button class=btn btn-o>Enter Whole Shop - See All Stock</button></a><a href=https://www.google.com/maps?q=" + str(sinfo['lat']) + "," + str(sinfo['lng']) + " target=_blank><button class=btn btn-b>📍 GPS Navigate - Real</button></a></div>"
    h += "</div><div style=display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px>"
    for p in products:
        if not ok(p["seller"]):
            continue
        h += "<div class=card><img src=" + p["image"] + " style=width:100%;height:130px;object-fit:cover><b style=font-size:18px>" + p["name"] + "</b><br><span style=font-size:15px>Stock " + str(p["stock"]) + " | " + p["shop"] + "</span><br><b style=font-size:18px;color:#f68b1e>KSh " + str(p["price"]) + "</b></div>"
    h += "</div>" + BOTTOM
    return h

@app.route("/map")
def map_page():
    h = STYLE + HEADER + "<div class=card><h2 style=font-size:24px>📍 Real Kenya GPS Map</h2><p style=font-size:16px>Real location from sellers - Boda can navigate</p><div id=map></div></div><link rel=stylesheet href=https://unpkg.com/leaflet@1.9.4/dist/leaflet.css><script src=https://unpkg.com/leaflet@1.9.4/dist/leaflet.js></script><script>var map=L.map('map').setView([-1.3956,36.7562],14);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);L.marker([-1.3956,36.7562]).addTo(map).bindPopup('Rongai Shoe Center - Whole Shop 10 pairs');</script><div class=card><h3>Shop on Map</h3><b>Rongai Shoe Center</b><br>10 pairs<br><a href=/shop/admin><button class=btn btn-o>Enter Whole Shop</button></a><a href=https://www.google.com/maps?q=-1.3956,36.7562 target=_blank><button class=btn btn-b>📍 Navigate with Google Maps</button></a></div>" + BOTTOM
    return h

@app.route("/shop/<seller>")
def shop_one(seller):
    u = users.get(seller,{})
    sname = u.get("shop","Shop")
    info = shops.get(sname,{})
    s_prods = [p for p in products if p["seller"]==seller]
    tot = sum([p["stock"] for p in s_prods])
    h = STYLE + HEADER
    h += "<div style=background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:20px;border-radius:14px;margin:10px><h2 style=font-size:24px>" + sname + " - WHOLE SHOP</h2><p style=font-size:18px>" + str(len(s_prods)) + " types, " + str(tot) + " pairs TOTAL - View BEFORE visiting</p><p style=font-size:16px>GPS " + str(info.get("lat","")) + " | Till " + u.get("till","") + "</p></div>"
    h += "<div class=card><a href=https://www.google.com/maps?q=" + str(info.get("lat",-1.3956)) + "," + str(info.get("lng",36.7562)) + " target=_blank><button class=btn btn-b style=font-size:18px>📍 Open GPS in Google Maps - Real Navigation</button></a></div><div style=display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px>"
    for p in s_prods:
        h += "<div class=card style=border:2px solid #f68b1e><img src=" + p["image"] + " style=width:100%;height:140px;object-fit:cover><b style=font-size:18px>" + p["name"] + "</b><br><span style=font-size:15px>Stock " + str(p["stock"]) + " | Size " + p["size"] + "</span><br><b style=font-size:18px;color:#f68b1e>KSh " + str(p["price"]) + "</b></div>"
    h += "</div>" + BOTTOM
    return h

@app.route("/post", methods=["GET","POST"])
def post_page():
    if request.method=="POST":
        nid = len(products)+1
        seller = "admin"
        shop = users[seller]["shop"]
        lat = users[seller]["lat"]
        lng = users[seller]["lng"]
        products.append({"id":nid,"name":request.form["name"],"price":int(request.form["price"]),"image":request.form["image"],"seller":seller,"shop":shop,"stock":int(request.form["stock"]),"size":request.form["size"],"lat":lat,"lng":lng})
        return redirect("/shop/" + seller)
    h = STYLE + HEADER + "<div class=card style=max-width:500px;margin:20px auto><h2 style=font-size:24px>📸 Post to Whole Shop</h2><p style=font-size:16px>Big font - GPS auto - Customer sees before coming</p><form method=post>Shoe Name:<input name=name required>Price KSh:<input name=price type=number required>Size:<input name=size>Stock pairs:<input name=stock type=number required>Image URL:<input name=image required value=https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500><button class=btn btn-o style=font-size:18px>POST TO WHOLE SHOP</button></form></div>" + BOTTOM
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
    h = STYLE + HEADER + "<div class=card style=max-width:500px;margin:20px auto><h2 style=font-size:24px>Register - Everyone</h2><p style=font-size:16px>Big font - Own Till - Real GPS - Whole Shop</p><form method=post>Name:<input name=fullname required>Phone:<input name=phone required>Username:<input name=username required>Password:<input name=password type=password required>Role:<select name=role><option value=buyer>Buyer</option><option value=seller>Seller - Own Till + GPS + Whole Shop</option></select>Shop Name:<input name=shop required>Till (customers pay YOU):<input name=till required>Area:<input name=area>Lat:<input name=lat id=lat value=-1.3956 required>Lng:<input name=lng id=lng value=36.7562 required><button type=button class=btn btn-b onclick=navigator.geolocation.getCurrentPosition(function(p){document.getElementById('lat').value=p.coords.latitude;document.getElementById('lng').value=p.coords.longitude;})>📍 Get My Current GPS Location</button><button class=btn btn-g style=font-size:18px>Register
