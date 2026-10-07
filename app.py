from flask import Flask, request, redirect, session
import os, datetime
app = Flask(__name__)
app.secret_key = "v16-short"
users = {"admin": {"shop":"Rongai Shoe Center","till":"0116782556","pass":"0116782556","ok":True,"lat":-1.3956,"lng":36.7562,"area":"Rongai Town"}}
shops = {"Rongai Shoe Center": {"own":"admin","till":"0116782556","ok":True,"lat":-1.3956,"lng":36.7562,"area":"Rongai Town"}}
products = [{"id":1,"name":"Jordan 1","price":4500,"img":"https://via.placeholder.com/400","shop":"Rongai Shoe Center","stock":10}]

def ok(u):
 x=users.get(u)
 return x and x.get("ok")

STYLE = '<style>body{margin:0;background:#f0f2f5;padding-bottom:90px;font-size:24px;font-family:Arial}.card{background:white;border-radius:16px;padding:18px;margin:12px;box-shadow:0 3px 10px #aaa}.btn{padding:20px;border-radius:12px;width:100%;margin-top:10px;font-weight:bold;border:none;font-size:24px}.btn-o{background:#f68b1e;color:white}.btn-b{background:#000;color:white}.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:14px 0;border-top:3px solid #f68b1e;z-index:9999}.nav{text-align:center;font-size:18px;font-weight:bold;text-decoration:none;color:#000}#map{height:85vh;width:100%}input{width:100%;padding:18px;margin:8px 0;border-radius:12px;border:2px solid #ddd;font-size:20px}</style>'
HEAD = '<div style="background:#f68b1e;padding:14px;display:flex;align-items:center;gap:12px"><div style="background:white;color:#f68b1e;width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:28px">E</div><b style="color:white;font-size:28px">EAZYMADE MARKET</b></div>'
BOT = '<div class="bottom"><a href="/" class="nav">🏪<br>Market</a><a href="/map" class="nav">📍<br>GPS MAP</a><a href="/post" class="nav">📸<br>Post</a><a href="/register" class="nav">👤<br>Join</a></div>'

@app.route("/")
def home():
 h = STYLE+HEAD
 h += '<div style="background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:26px;border-radius:16px;margin:12px;text-align:center"><div style="background:white;color:#f68b1e;width:90px;height:90px;border-radius:50%;margin:0 auto;display:flex;align-items:center;justify-content:center;font-size:48px;font-weight:bold">E</div><h2 style="font-size:36px">EAZYMADE ARTIFICIAL MARKET</h2><p style="font-size:24px">See whole shop BEFORE you go</p><a href="/map"><button class="btn" style="background:white;color:#f68b1e">VIEW GPS MAP - FULL PAGE</button></a></div>'
 h += '<div class="card"><h3 style="font-size:28px">Shops - Whole Shop</h3>'
 for n,s in shops.items():
  h += '<div class="card" style="border-left:8px solid #f68b1e"><b style="font-size:26px">'+n+'</b><br><span style="font-size:22px">10 pairs - Whole Shop</span><br><span style="font-size:18px">'+s["area"]+'</span><br><a href="/shop/'+s["own"]+'"><button class="btn btn-o">Enter Whole Shop</button></a><a href="https://www.google.com/maps?q='+str(s["lat"])+','+str(s["lng"])+'" target="_blank"><button class="btn btn-b">GPS Navigate</button></a></div>'
 h += '</div>'
 for p in products:
  h += '<div class="card"><img src="'+p["img"]+'" style="width:100%;height:160px;object-fit:cover;border-radius:12px"><br><b style="font-size:24px">'+p["name"]+'</b><br>Stock '+str(p["stock"])+' | KSh '+str(p["price"])+'</div>'
 h += BOT
 return h

@app.route("/map")
def mp():
 h = STYLE+HEAD
 h += '<div id="map"></div><div style="position:absolute;bottom:100px;left:10px;right:10px;z-index:1000" class="card"><b>Rongai Shoe Center</b><br><a href="/shop/admin"><button class="btn btn-o">Enter Whole Shop</button></a><a href="https://www.google.com/maps?q=-1.3956,36.7562" target="_blank"><button class="btn btn-b">Navigate GPS</button></a></div>'
 h += '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script><script>var m=L.map("map").setView([-1.3956,36.7562],15);L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(m);L.marker([-1.3956,36.7562]).addTo(m).bindPopup("Rongai Shoe Center").openPopup();</script>'+BOT
 return h

@app.route("/shop/<seller>")
def shop(seller):
 h = STYLE+HEAD
 h += '<div style="background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:24px;border-radius:16px;margin:12px"><h2>WHOLE SHOP - 10 pairs TOTAL</h2><p>View BEFORE visiting - No phone shown</p></div><div class="card"><a href="https://www.google.com/maps?q=-1.3956,36.7562" target="_blank"><button class="btn btn-b" style="font-size:26px">Open GPS in Google Maps - FULL</button></a></div>'+BOT
 return h

@app.route("/post", methods=["GET","POST"])
def post():
 if request.method=="POST":
  products.append({"id":len(products)+1,"name":request.form["name"],"price":request.form["price"],"img":request.form["img"],"shop":"Rongai Shoe Center","stock":request.form["stock"]})
  return redirect("/")
 h = STYLE+HEAD+'<div class="card" style="max-width:600px;margin:20px auto"><h2 style="font-size:30px">Post New Stock - Whole Shop</h2><form method="post">Name:<input name="name" required>Price:<input name="price" required>Stock:<input name="stock" required>Image URL:<input name="img" required><button class="btn btn-o">POST NOW - Works</button></form></div>'+BOT
 return h

@app.route("/register", methods=["GET","POST"])
def reg():
 if request.method=="POST":
  uname=request.form["user"].lower()
  users[uname]={"shop":request.form["shop"],"till":request.form["till"],"pass":request.form["pass"],"ok":False,"lat":float(request.form["lat"] or -1.3956),"lng":float(request.form["lng"] or 36.7562),"area":request.form["area"]}
  shops[request.form["shop"]]={"own":uname,"till":request.form["till"],"ok":False,"lat":float(request.form["lat"] or -1.3956),"lng":float(request.form["lng"] or 36.7562),"area":request.form["area"]}
  return redirect("/")
 h = STYLE+HEAD+'<div class="card" style="max-width:600px;margin:20px auto"><h2 style="font-size:30px">Register - BIG FONT</h2><form method="post">Name:<input name="fullname" required>Username:<input name="user" required>Password:<input name="pass" type="password" required>Shop Name:<input name="shop" required>Your Till (private - not shown):<input name="till" required>Area:<input name="area">Lat:<input name="lat" id="lat" value="-1.3956">Lng:<input name="lng" id="lng" value="36.7562"><button type="button" class="btn btn-b" onclick="navigator.geolocation.getCurrentPosition(p=>{lat.value=p.coords.latitude;lng.value=p.coords.longitude})">Get My GPS Location</button><button class="btn" style="background:green;color:white">Register</button></form></div>'+BOT
 return h

@app.route("/office", methods=["GET","POST"])
def off():
 if request.method=="POST":
  if request.form.get("password")!="0116782556":
   return "Wrong"
  session["off"]=True
 if not session.get("off"):
  return STYLE+HEAD+'<div class="card" style="max-width:400px;margin:40px auto"><h2>Office Login</h2><form method="post"><input name="password" type="password" placeholder="Enter office pass"><button class="btn btn-b">Enter</button></form></div>'+BOT
 h=STYLE+HEAD+'<div class="card"><h2>Office - Private Tills Hidden</h2>'
 for n,s in shops.items():
  h+='<div class="card">'+n+' - Till hidden private - Area '+s["area"]+'</div>'
 h+='</div>'+BOT
 return h

if __name__=="__main__":
 app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
