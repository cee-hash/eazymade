from flask import Flask, request, redirect, session
import os, base64
app=Flask(__name__)
app.secret_key="v18-cart"
shops={"Rongai Shoe Center":{"own":"admin","lat":-1.3956,"lng":36.7562,"area":"Rongai"}}
prods=[{"id":1,"name":"Jordan 1","price":4500,"img":"https://via.placeholder.com/400","stock":10}]

S='<style>body{margin:0;background:#f0f2f5;padding-bottom:110px;font-size:24px;font-family:Arial}.card{background:white;border-radius:16px;padding:18px;margin:12px;box-shadow:0 3px 10px #aaa}.btn{padding:20px;border-radius:12px;width:100%;margin-top:10px;font-weight:bold;border:none;font-size:24px}.btn-o{background:#f68b1e;color:white}.btn-b{background:#000;color:white}.btn-g{background:green;color:white}.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:14px 0;border-top:3px solid #f68b1e;z-index:9999}.nav{text-align:center;font-size:18px;font-weight:bold;text-decoration:none;color:#000;position:relative}.badge{background:red;color:white;border-radius:50%;padding:2px 8px;font-size:16px;position:absolute;top:-8px;right:0}#map{height:85vh;width:100%}input{width:100%;padding:18px;margin:8px 0;border-radius:12px;border:2px solid #ddd;font-size:20px}</style>'
H='<div style="background:#f68b1e;padding:14px;display:flex;gap:12px"><div style="background:white;color:#f68b1e;width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:28px">E</div><b style="color:white;font-size:28px">EAZYMADE MARKET</b></div>'

def bot():
 c=len(session.get("cart",[]))
 b='<span class="badge">'+str(c)+'</span>' if c>0 else ''
 return '<div class="bottom"><a href="/" class="nav">🏪<br>Market</a><a href="/map" class="nav">📍<br>GPS</a><a href="/post" class="nav">📸<br>Post</a><a href="/cart" class="nav">🛒<br>Cart'+b+'</a><a href="/register" class="nav">👤<br>Join</a></div>'

@app.route("/")
def home():
 h=S+H+'<div style="background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:26px;border-radius:16px;margin:12px;text-align:center"><h2 style="font-size:36px">EAZYMADE MARKET</h2><p style="font-size:22px">Cart added - Big font - Whole shop</p><a href="/map"><button class="btn" style="background:white;color:#f68b1e">VIEW MAP FULL PAGE</button></a></div>'
 for p in prods:
  h+='<div class="card"><img src="'+p["img"]+'" style="width:100%;height:220px;object-fit:cover;border-radius:12px"><br><b style="font-size:26px">'+p["name"]+'</b><br>KSh '+str(p["price"])+' | Stock '+str(p["stock"])+'<br><a href="/add/'+str(p["id"])+'"><button class="btn btn-o">🛒 Add to Cart - BIG</button></a><a href="/shop/admin"><button class="btn btn-b">Enter Whole Shop</button></a></div>'
 h+=bot()
 return h

@app.route("/add/<int:pid>")
def add(pid):
 cart=session.get("cart",[])
 cart.append(pid)
 session["cart"]=cart
 return redirect("/cart")

@app.route("/cart")
def cart():
 cart=session.get("cart",[])
 h=S+H+'<div class="card"><h2 style="font-size:32px">🛒 My Cart - Whole Shop Total</h2>'
 total=0
 count=0
 for pid in cart:
  p=next((x for x in prods if x["id"]==pid),None)
  if p:
   h+='<div class="card" style="border-left:8px solid #f68b1e"><img src="'+p["img"]+'" style="width:100%;height:140px;object-fit:cover;border-radius:12px"><br><b>'+p["name"]+'</b> - KSh '+str(p["price"])+'</div>'
   total+=int(p["price"])
   count+=1
 h+='<div class="card" style="background:#000;color:white"><b style="font-size:28px">Total: '+str(count)+' pairs - KSh '+str(total)+'</b><br><span style="font-size:20px">Whole shop pairs counted</span></div>'
 h+='<a href="https://wa.me/254116782556?text=Hi I want '+str(count)+' pairs total KSh '+str(total)+'"><button class="btn btn-g" style="font-size:26px">📱 Order via WhatsApp - Private Till</button></a><a href="/"><button class="btn btn-b">Continue Shopping</button></a><a href="/clear"><button class="btn" style="background:#ccc">Clear Cart</button></a></div>'+bot()
 return h

@app.route("/clear")
def clear():
 session["cart"]=[]
 return redirect("/")

@app.route("/map")
def mp():
 return S+H+'<div id="map"></div><link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script><script>var m=L.map("map").setView([-1.3956,36.7562],15);L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(m);L.marker([-1.3956,36.7562]).addTo(m).bindPopup("Rongai Shoe Center - Whole Shop").openPopup();</script>'+bot()

@app.route("/post",methods=["GET","POST"])
def post():
 if request.method=="POST":
  img="https://via.placeholder.com/400"
  f=request.files.get("pic")
  if f and f.filename!="":
   img="data:image/jpeg;base64,"+base64.b64encode(f.read()).decode()
  elif request.form.get("img")!="":
   img=request.form.get("img")
  prods.append({"id":len(prods)+1,"name":request.form["name"],"price":request.form["price"],"img":img,"stock":request.form["stock"]})
  return redirect("/")
 return S+H+'<div class="card"><h2>Post - Upload From Phone</h2><form method="post" enctype="multipart/form-data">Name:<input name="name" required>Price:<input name="price" required>Stock:<input name="stock" required><b>Phone Pic:</b><input type="file" name="pic" accept="image/*" capture="environment" style="border:3px dashed #f68b1e;background:#fff3e0;padding:24px">OR URL:<input name="img"><button class="btn btn-o">POST WITH PHONE PIC</button></form></div>'+bot()

@app.route("/register",methods=["GET","POST"])
def reg():
 if request.method=="POST":
  return redirect("/")
 return S+H+'<div class="card"><h2>Register - BIG</h2><form method="post">Name:<input required>Shop:<input required>Till (private hidden):<input required><button type="button" class="btn btn-b" onclick="navigator.geolocation.getCurrentPosition(p=>{lat.value=p.coords.latitude;lng.value=p.coords.longitude})">Get GPS</button>Lat:<input id="lat" value="-1.3956">Lng:<input id="lng" value="36.7562"><button class="btn" style="background:green;color:white">Register</button></form></div>'+bot()

if __name__=="__main__":
 app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
