from flask import Flask, request, redirect, session
import os, datetime

app = Flask(__name__)
app.secret_key = "v14"
OFFICE_PASS = "0116782556"

users = {
 "admin": {"name":"John","shop":"Rongai Shoe Center","till":"0116782556","password":"0116782556","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=365),"lat":-1.3956,"lng":36.7562,"area":"Rongai Town"}
}
products = [
 {"id":1,"name":"Jordan 1","price":4500,"image":"https://via.placeholder.com/300","seller":"admin","shop":"Rongai Shoe Center","stock":10,"size":"42","lat":-1.3956,"lng":36.7562}
]
shops = {
 "Rongai Shoe Center": {"owner":"admin","till":"0116782556","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=30),"lat":-1.3956,"lng":36.7562,"area":"Rongai Town"}
}

def ok(u):
 x=users.get(u)
 return x and x.get("approved") and datetime.datetime.now() < x.get("expiry")

STYLE = """
<style>
body{font-family:Arial;margin:0;background:#f0f2f5;padding-bottom:80px;font-size:18px}
.card{background:white;border-radius:14px;padding:14px;margin:10px;box-shadow:0 2px 8px #ddd}
.btn{padding:16px;border-radius:10px;width:100%;margin-top:8px;font-weight:bold;border:none;font-size:18px}
.btn-o{background:#f68b1e;color:white}
.btn-b{background:#000;color:white}
.btn-g{background:green;color:white}
.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:12px 0;border-top:2px solid #f68b1e;z-index:2000}
.nav{text-align:center;font-size:14px;font-weight:bold;text-decoration:none;color:#000}
</style>
"""

HEAD = """
<div style="background:#000;color:#0f0;padding:6px;text-align:center;font-size:12px">ARTIFICIAL MARKET - Till 0116782556</div>
<div style="background:#f68b1e;padding:12px;display:flex;align-items:center;gap:10px">
<div style="background:white;color:#f68b1e;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:22px">E</div>
<b style="color:white;font-size:22px">EAZYMADE</b>
</div>
"""

BOTTOM = """
<div class="bottom">
<a href="/" class="nav">🏪<br>Market</a>
<a href="/map" class="nav">📍<br>GPS</a>
<a href="/post" class="nav">📸<br>Post</a>
<a href="/register" class="nav">👤<br>Register</a>
</div>
"""

@app.route("/")
def home():
 h = STYLE + HEAD
 h += """
<div style="background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:22px;border-radius:14px;margin:10px;text-align:center">
<div style="background:white;color:#f68b1e;width:70px;height:70px;border-radius:50%;margin:0 auto;display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:bold">E</div>
<h2>EAZYMADE ARTIFICIAL MARKET</h2>
<p style="font-size:18px">See whole shop stock BEFORE you go</p>
<a href="/map"><button class="btn" style="background:white;color:#f68b1e">VIEW MARKET MAP - Real GPS</button></a>
<a href="/register"><button class="btn btn-b">Everyone Register</button></a>
</div>
"""
 h += '<div class="card"><h3>Shops - Whole Shop</h3>'
 for sname,sinfo in shops.items():
  if not ok(sinfo["owner"]):
   continue
  h += '<div class="card" style="border-left:6px solid #f68b1e">'
  h += '<b style="font-size:20px">'+sname+'</b><br>'
  h += sinfo["area"]+' | Till '+sinfo["till"]+'<br>'
  h += '<a href="/shop/'+sinfo["owner"]+'"><button class="btn btn-o">Enter Whole Shop</button></a>'
  h += '<a href="https://www.google.com/maps?q='+str(sinfo["lat"])+','+str(sinfo["lng"])+'" target="_blank"><button class="btn btn-b">GPS Navigate</button></a>'
  h += '</div>'
 h += '</div>' + BOTTOM
 return h

@app.route("/map")
def map_page():
 h = STYLE + HEAD
 h += '<div class="card"><h2>Real Kenya GPS Map</h2><div id="map" style="height:400px;background:#ddd"></div></div>'
 h += '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>'
 h += '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'
 h += '<script>var map=L.map("map").setView([-1.3956,36.7562],14);L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);L.marker([-1.3956,36.7562]).addTo(map).bindPopup("Rongai Shoe Center");</script>'
 h += BOTTOM
 return h

@app.route("/shop/<seller>")
def shop_one(seller):
 u = users.get(seller,{})
 sname = u.get("shop","Shop")
 h = STYLE + HEAD
 h += '<div style="background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:20px;border-radius:14px;margin:10px"><h2>'+sname+' - WHOLE SHOP</h2><p>View BEFORE you go</p></div>'
 h += '<div class="card"><a href="https://www.google.com/maps?q=-1.3956,36.7562" target="_blank"><button class="btn btn-b">Open GPS in Google Maps</button></a></div>'
 h += BOTTOM
 return h

@app.route("/post", methods=["GET","POST"])
def post_page():
 if request.method=="POST":
  nid = len(products)+1
  products.append({"id":nid,"name":request.form["name"],"price":int(request.form["price"]),"image":request.form["image"],"seller":"admin","shop":"Rongai Shoe Center","stock":int(request.form["stock"]),"size":request.form["size"],"lat":-1.3956,"lng":36.7562})
  return redirect("/")
 h = STYLE + HEAD
 h += """
<div class="card" style="max-width:500px;margin:20px auto">
<h2>Post to Whole Shop</h2>
<form method="post">
Name:<input name="name" required>
Price:<input name="price" type="number" required>
Size:<input name="size">
Stock:<input name="stock" type="number" required>
Image URL:<input name="image" required value="https://via.placeholder.com/300">
<button class="btn btn-o">POST</button>
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
<div class="card" style="max-width:500px;margin:20px auto">
<h2>Register - Everyone</h2>
<form method="post">
Name:<input name="fullname" required>
Phone:<input name="phone" required>
Username:<input name="username" required>
Password:<input name="password" type="password" required>
Shop Name:<input name="shop" required>
Till:<input name="till" required>
Area:<input name="area">
Lat:<input name="lat" id="lat" value="-1.3956" required>
Lng:<input name="lng" id="lng" value="36.7562" required>
<button type="button" class="btn btn-b" onclick="getGPS()">Get My GPS</button>
<button class="btn btn-g">Register</button>
</form>
</div>
<script>
function getGPS(){
 navigator.geolocation.getCurrentPosition(function(p){
  document.getElementById('lat').value=p.coords.latitude;
  document.getElementById('lng').value=p.coords.longitude;
 });
}
</script>
"""
 h += BOTTOM
 return h

@app.route("/office", methods=["GET","POST"])
def office():
 if request.method=="POST":
  if request.form.get("password")!="0116782556":
   return "Wrong"
  session["office"]=True
 if not session.get("office"):
  return STYLE+HEAD+'<div class="card" style="max-width:400px;margin:40px auto"><h2>Office</h2><form method="post"><input name="password" type="password" placeholder="0116782556"><button class="btn btn-b">Enter</button></form></div>'+BOTTOM
 h = STYLE+HEAD+'<div class="card"><h2>Office - Till 0116782556</h2></div>'+BOTTOM
 return h

if __name__=="__main__":
 app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
