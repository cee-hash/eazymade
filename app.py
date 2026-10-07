from flask import Flask, request, redirect, session
import os, datetime

app = Flask(__name__)
app.secret_key = "v15-big"
OFFICE_PASS = "0116782556"

users = {
 "admin": {"name":"John","shop":"Rongai Shoe Center","till":"0116782556","password":"0116782556","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=365),"lat":-1.3956,"lng":36.7562,"area":"Rongai Town"}
}
products = [
 {"id":1,"name":"Jordan 1","price":4500,"image":"https://via.placeholder.com/400","seller":"admin","shop":"Rongai Shoe Center","stock":10,"size":"42","lat":-1.3956,"lng":36.7562}
]
shops = {
 "Rongai Shoe Center": {"owner":"admin","till":"0116782556","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=30),"lat":-1.3956,"lng":36.7562,"area":"Rongai Town, Magadi Road"}
}

def ok(u):
 x=users.get(u)
 return x and x.get("approved") and datetime.datetime.now() < x.get("expiry")

STYLE = """
<style>
body{font-family:Arial;margin:0;background:#f0f2f5;padding-bottom:90px;font-size:22px}
h2{font-size:32px;font-weight:bold}
h3{font-size:28px;font-weight:bold}
b{font-size:22px}
.card{background:white;border-radius:16px;padding:18px;margin:12px;box-shadow:0 3px 10px #bbb}
.btn{padding:20px;border-radius:12px;width:100%;margin-top:10px;font-weight:bold;border:none;font-size:22px}
.btn-o{background:#f68b1e;color:white}
.btn-b{background:#000;color:white}
.btn-g{background:green;color:white}
.small{font-size:18px;color:#555}
input,select{width:100%;padding:18px;margin:8px 0;border-radius:12px;border:2px solid #ddd;font-size:20px}
.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:14px 0;border-top:3px solid #f68b1e;z-index:9999;box-shadow:0 -3px 12px #999}
.nav{text-align:center;font-size:16px;font-weight:bold;text-decoration:none;color:#000}
.nav-icon{font-size:32px}
#map{height:85vh;width:100%;border-radius:0}
</style>
"""

HEAD = """
<div style="background:#000;color:#0f0;padding:8px;text-align:center;font-size:14px">ARTIFICIAL MARKET - Till 0116782556 - Logo E</div>
<div style="background:#f68b1e;padding:14px;display:flex;align-items:center;gap:12px">
<div style="background:white;color:#f68b1e;width:50px;height:50px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:26px">E</div>
<b style="color:white;font-size:26px">EAZYMADE</b>
</div>
"""

BOTTOM = """
<div class="bottom">
<a href="/" class="nav"><span class="nav-icon">🏪</span><br>Market</a>
<a href="/map" class="nav"><span class="nav-icon">📍</span><br>GPS MAP</a>
<a href="/post" class="nav"><span class="nav-icon">📸</span><br>Post</a>
<a href="/register" class="nav"><span class="nav-icon">👤</span><br>Join</a>
</div>
"""

@app.route("/")
def home():
 h = STYLE + HEAD
 h += """
<div style="background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:26px;border-radius:16px;margin:12px;text-align:center">
<div style="background:white;color:#f68b1e;width:80px;height:80px;border-radius:50%;margin:0 auto;display:flex;align-items:center;justify-content:center;font-size:42px;font-weight:bold">E</div>
<h2>EAZYMADE ARTIFICIAL MARKET</h2>
<p style="font-size:22px">See whole shop stock BEFORE you go - Big Font</p>
<a href="/map"><button class="btn" style="background:white;color:#f68b1e;font-size:24px">📍 VIEW MARKET MAP - Whole Page</button></a>
<a href="/register"><button class="btn btn-b">👤 Everyone Register</button></a>
</div>
"""
 h += '<div class="card"><h3>🏬 Shops - Enter Whole Shop</h3>'
 for sname,sinfo in shops.items():
  if not ok(sinfo["owner"]):
   continue
  h += '<div class="card" style="border-left:8px solid #f68b1e">'
  h += '<b style="font-size:26px">'+sname+'</b><br>'
  h += '<span style="font-size:20px">10 pairs - Whole Shop</span><br>'
  h += '<span class="small">'+sinfo["area"]+' | Till '+sinfo["till"]+'</span><br>'
  h += '<a href="/shop/'+sinfo["owner"]+'"><button class="btn btn-o">Enter Whole Shop - See All Stock</button></a>'
  h += '<a href="https://www.google.com/maps?q='+str(sinfo["lat"])+','+str(sinfo["lng"])+'" target="_blank"><button class="btn btn-b">📍 GPS Navigate - Big</button></a>'
  h += '</div>'
 h += '</div>' + BOTTOM
 return h

@app.route("/map")
def map_page():
 h = STYLE + HEAD
 h += """
<div style="height:85vh;width:100%;position:relative">
<div id="map"></div>
<div style="position:absolute;bottom:100px;left:10px;right:10px;z-index:1000;background:white;padding:14px;border-radius:14px;box-shadow:0 4px 12px #000">
<b style="font-size:22px">Rongai Shoe Center</b><br>
<span style="font-size:18px">Whole Shop - 10 pairs</span><br>
<a href="/shop/admin"><button class="btn btn-o">Enter Shop</button></a>
<a href="https://www.google.com/maps?q=-1.3956,36.7562" target="_blank"><button class="btn btn-b">📍 Navigate GPS</button></a>
</div>
</div>
"""
 h += '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>'
 h += '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'
 h += '<script>var map=L.map("map").setView([-1.3956,36.7562],15);L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);L.marker([-1.3956,36.7562]).addTo(map).bindPopup("Rongai Shoe Center - Whole Shop").openPopup();</script>'
 h += BOTTOM
 return h

@app.route("/shop/<seller>")
def shop_one(seller):
 u = users.get(seller,{})
 sname = u.get("shop","Shop")
 h = STYLE + HEAD
 h += '<div style="background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:24px;border-radius:16px;margin:12px"><h2 style="font-size:28px">'+sname+' - WHOLE SHOP</h2><p style="font-size:22px">10 pairs TOTAL - View BEFORE visiting</p></div>'
 h += '<div class="card"><a href="https://www.google.com/maps?q=-1.3956,36.7562" target="_blank"><button class="btn btn-b" style="font-size:24px">📍 Open GPS in Google Maps - FULL</button></a></div>'
 h += BOTTOM
 return h

@app.route("/post", methods=["GET","POST"])
def post_page():
 if request.method=="POST":
  products.append({"id":len(products)+1,"name":request.form["name"],"price":int(request.form["price"]),"image":request.form["image"],"seller":"admin","shop":"Rongai Shoe Center","stock":int(request.form["stock"]),"size":request.form["size"],"lat":-1.3956,"lng":36.7562})
  return redirect("/")
 h = STYLE + HEAD
 h += """
<div class="card" style="max-width:600px;margin:20px auto">
<h2>Post to Whole Shop - BIG</h2>
<form method="post">
Name:<input name="name" required>
Price:<input name="price" type="number" required>
Size:<input name="size">
Stock:<input name="stock" type="number" required>
Image URL:<input name="image" required>
<button class="btn btn-o">POST - BIG BUTTON</button>
</form>
</div>
"""
 h += BOTTOM
 return h

@app.route("/register", methods=["GET","POST"])
def reg():
 if request.method=="POST":
  uname = request.form["username"].lower()
  lat = float(request.form["lat"] or -1.3956)
  lng = float(request.form["lng"] or 36.7562)
  exp = datetime.datetime.now()+datetime.timedelta(days=30)
  users[uname] = {"name":request.form["fullname"],"shop":request.form["shop"],"till":request.form["till"],"password":request.form["password"],"approved":False,"expiry":exp,"lat":lat,"lng":lng,"area":request.form["area"]}
  shops[request.form["shop"]] = {"owner":uname,"till":request.form["till"],"approved":False,"expiry":exp,"lat":lat,"lng":lng,"area":request.form["area"]}
  return redirect("/")
 h = STYLE + HEAD
 h += """
<div class="card" style="max-width:600px;margin:20px auto">
<h2 style="font-size:30px">Register - BIG FONT</h2>
<form method="post">
Name:<input name="fullname" required>
Phone:<input name="phone" required>
Username:<input name="username" required>
Password:<input name
