from flask import Flask, request, redirect, session
import os, base64
app=Flask(__name__)
app.secret_key="s"
shops={"Rongai Shoe Center":{"own":"admin","lat":-1.3956,"lng":36.7562,"area":"Rongai"}}
prods=[{"name":"Jordan 1","price":4500,"img":"https://via.placeholder.com/400","stock":10}]
S='<style>body{margin:0;background:#f0f2f5;padding-bottom:90px;font-size:24px;font-family:Arial}.card{background:white;border-radius:16px;padding:18px;margin:12px;box-shadow:0 3px 10px #aaa}.btn{padding:20px;border-radius:12px;width:100%;margin-top:10px;font-weight:bold;border:none;font-size:24px}.btn-o{background:#f68b1e;color:white}.btn-b{background:#000;color:white}.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:14px 0;border-top:3px solid #f68b1e}#map{height:85vh;width:100%}input{width:100%;padding:18px;margin:8px 0;border-radius:12px;border:2px solid #ddd;font-size:20px}</style>'
H='<div style="background:#f68b1e;padding:14px;display:flex;gap:12px"><div style="background:white;color:#f68b1e;width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:28px">E</div><b style="color:white;font-size:28px">EAZYMADE MARKET</b></div>'
B='<div class="bottom"><a href="/">🏪<br>Market</a><a href="/map">📍<br>GPS</a><a href="/post">📸<br>Post</a><a href="/register">👤<br>Join</a></div>'

@app.route("/")
def home():
 h=S+H+'<div style="background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:26px;border-radius:16px;margin:12px;text-align:center"><h2 style="font-size:36px">EAZYMADE MARKET</h2><a href="/map"><button class="btn" style="background:white;color:#f68b1e">VIEW MAP FULL PAGE</button></a></div>'
 for p in prods:
  h+='<div class="card"><img src="'+p["img"]+'" style="width:100%;height:220px;object-fit:cover;border-radius:12px"><br><b style="font-size:26px">'+p["name"]+'</b><br>KSh '+str(p["price"])+' | Stock '+str(p["stock"])+'</div>'
 h+=B
 return h

@app.route("/map")
def mp():
 return S+H+'<div id="map"></div><link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script><script>var m=L.map("map").setView([-1.3956,36.7562],15);L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(m);L.marker([-1.3956,36.7562]).addTo(m).bindPopup("Rongai").openPopup();</script>'+B

@app.route("/post",methods=["GET","POST"])
def post():
 if request.method=="POST":
  img="https://via.placeholder.com/400"
  f=request.files.get("pic")
  if f and f.filename!="":
   img="data:image/jpeg;base64,"+base64.b64encode(f.read()).decode()
  elif request.form.get("img")!="":
   img=request.form.get("img")
  prods.append({"name":request.form["name"],"price":request.form["price"],"img":img,"stock":request.form["stock"]})
  return redirect("/")
 return S+H+'<div class="card"><h2>Post - Upload From Phone</h2><form method="post" enctype="multipart/form-data">Name:<input name="name" required>Price:<input name="price" required>Stock:<input name="stock" required><b>Phone Pic:</b><input type="file" name="pic" accept="image/*" capture="environment" style="border:3px dashed #f68b1e;background:#fff3e0;padding:24px">OR URL:<input name="img"><button class="btn btn-o">POST WITH PHONE PIC</button></form></div>'+B

@app.route("/register",methods=["GET","POST"])
def reg():
 if request.method=="POST":
  return redirect("/")
 return S+H+'<div class="card"><h2>Register - BIG</h2><form method="post">Name:<input required>Shop:<input required>Till (private):<input required><button type="button" class="btn btn-b" onclick="navigator.geolocation.getCurrentPosition(p=>{lat.value=p.coords.latitude;lng.value=p.coords.longitude})">Get GPS</button>Lat:<input id="lat" value="-1.3956">Lng:<input id="lng" value="36.7562"><button class="btn" style="background:green;color:white">Register</button></form></div>'+B

if __name__=="__main__":
 app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
