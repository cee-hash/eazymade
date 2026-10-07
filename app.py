from flask import Flask, request, redirect, session
import os, base64
app = Flask(__name__)
app.secret_key = "v21safe"
shops = {"Rongai Shoe Center": {"own": "admin", "till": "0116782556", "ok": True, "lat": -1.3956, "lng": 36.7562, "area": "Rongai Town"}}
prods = [{"id": 1, "name": "Jordan 1", "price": 4500, "img": "https://via.placeholder.com/400", "shop": "Rongai Shoe Center", "stock": 10}]
users = {"admin": {"shop": "Rongai Shoe Center", "pass": "0116782556"}}

STYLE = "body{margin:0;background:#f0f2f5;padding-bottom:110px;font-size:24px;font-family:Arial}.card{background:white;border-radius:16px;padding:18px;margin:12px;box-shadow:0 3px 10px #aaa}.btn{padding:20px;border-radius:12px;width:100%;margin-top:10px;font-weight:bold;border:none;font-size:24px}.btn-o{background:#f68b1e;color:white}.btn-b{background:#000;color:white}.btn-g{background:green;color:white}.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:14px 0;border-top:3px solid #f68b1e}#map{height:85vh;width:100%}input,select{width:100%;padding:18px;margin:8px 0;border-radius:12px;border:2px solid #ddd;font-size:20px}"
HEAD = "<div style=background:#f68b1e;padding:14px;display:flex;gap:12px><div style=background:white;color:#f68b1e;width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:28px>E</div><b style=color:white;font-size:28px>EAZYMADE MARKET</b></div>"

def bottom_nav():
  c = len(session.get("cart", []))
  badge = ""
  if c > 0:
    badge = "<span style=background:red;color:white;border-radius:50%;padding:2px 8px;font-size:14px;position:absolute;top:-8px;right:0>" + str(c) + "</span>"
  return "<div class=bottom><a href=/ style=text-align:center;font-size:16px;font-weight:bold;text-decoration:none;color:#000;position:relative>Market</a><a href=/map style=text-align:center;font-size:16px;font-weight:bold;text-decoration:none;color:#000>GPS</a><a href=/post style=text-align:center;font-size:16px;font-weight:bold;text-decoration:none;color:#000>Post</a><a href=/cart style=text-align:center;font-size:16px;font-weight:bold;text-decoration:none;color:#000;position:relative>Cart" + badge + "</a><a href=/register style=text-align:center;font-size:16px;font-weight:bold;text-decoration:none;color:#000>Join</a></div>"

@app.route("/")
def home():
  html = "<style>" + STYLE + "</style>" + HEAD
  html += "<div style=background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:26px;border-radius:16px;margin:12px;text-align:center><h2>MARKET ALL SHOPS</h2><a href=/map><button class=btn style=background:white;color:#f68b1e>VIEW MAP ALL SHOPS</button></a></div>"
  for name, s in shops.items():
    if not s["ok"]:
      continue
    cnt = 0
    tot = 0
    for p in prods:
      if p["shop"] == name:
        cnt += 1
        tot += int(p["stock"])
    html += "<div class=card style=border-left:8px solid #f68b1e><b style=font-size:26px>" + name + "</b><br>" + s["area"] + " - " + str(cnt) + " types - " + str(tot) + " pairs TOTAL<br><a href=/shop/" + s["own"] + "><button class=btn-o style=padding:20px;border-radius:12px;width:100%;margin-top:10px;font-weight:bold;border:none;font-size:24px;background:#f68b1e;color:white>Enter Whole Shop " + str(tot) + " pairs</button></a></div>"
  for p in prods:
    html += "<div class=card><img src=" + p["img"] + " style=width:100%;height:220px;object-fit:cover;border-radius:12px;background:#eee><br><b>" + p["name"] + "</b> (" + p["shop"] + ")<br>KSh " + str(p["price"]) + " Stock " + str(p["stock"]) + "<br><a href=/add/" + str(p["id"]) + "><button class=btn-o style=padding:20px;border-radius:12px;width:100%;margin-top:10px;font-weight:bold;border:none;font-size:24px;background:#f68b1e;color:white>Add to Cart</button></a></div>"
  html += bottom_nav()
  return html

@app.route("/add/<int:pid>")
def add(pid):
  c = session.get("cart", [])
  c.append(pid)
  session["cart"] = c
  return redirect("/cart")

@app.route("/cart")
def cart():
  c = session.get("cart", [])
  html = "<style>" + STYLE + "</style>" + HEAD + "<div class=card><h2>Cart Whole Shop</h2>"
  tot = 0
  cnt = 0
  for pid in c:
    for p in prods:
      if p["id"] == pid:
        html += "<div class=card><img src=" + p["img"] + " style=width:100%;height:120px;object-fit:cover><br>" + p["name"] + " KSh " + str(p["price"]) + "</div>"
        tot += int(p["price"])
        cnt += 1
  html += "<div class=card style=background:#000;color:white><b style=font-size:26px>TOTAL " + str(cnt) + " pairs KSh " + str(tot) + "</b></div>"
  html += "<a href=https://wa.me/254116782556?text=Order><button style=padding:20px;border-radius:12px;width:100%;margin-top:10px;font-weight:bold;border:none;font-size:24px;background:green;color:white>Order WhatsApp Private Till</button></a>"
  html += "<a href=/><button style=padding:20px;border-radius:12px;width:100%;margin-top:10px;font-weight:bold;border:none;font-size:24px;background:#000;color:white>Continue</button></a>"
  html += "<a href=/clear><button style=padding:20px;border-radius:12px;width:100%;margin-top:10px;font-weight:bold;border:none;font-size:24px;background:#ccc>Clear</button></a></div>" + bottom_nav()
  return html

@app.route("/clear")
def clear():
  session["cart"] = []
  return redirect("/")

@app.route("/map")
def mp():
  mks = ""
  for n, s in shops.items():
    if s["ok"]:
      mks += "L.marker([" + str(s["lat"]) + "," + str(s["lng"]) + "]).addTo(m).bindPopup(\"" + n + "<br><a href=/shop/" + s["own"] + ">Enter Shop</a>\");"
  html = "<style>" + STYLE + "</style>" + HEAD + "<div id=map></div><link rel=stylesheet href=https://unpkg.com/leaflet@1.9.4/dist/leaflet.css><script src=https://unpkg.com/leaflet@1.9.4/dist/leaflet.js></script><script>var m=L.map('map').setView([-1.3956,36.7562],13);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(m);" + mks + "</script>" + bottom_nav()
  return html

@app.route("/post", methods=["GET", "POST"])
def post():
  if request.method == "POST":
    img = "https://via.placeholder.com/400"
    f = request.files.get("pic")
    if f and f.filename!= "":
      img = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
    prods.append({"id": len(prods)+1, "name": request.form["name"], "price": request.form["price"], "img": img, "shop": request.form.get("shop") or "Rongai Shoe Center", "stock": request.form["stock"]})
    return redirect("/")
  opts = ""
  for n in shops:
    if shops[n]["ok"]:
      opts += "<option>" + n + "</option>"
  html = "<style>" + STYLE + "</style>" + HEAD + "<div class=card><h2>Post Upload Phone All Shops</h2><form method=post enctype=multipart/form-data>Shop:<select name=shop>" + opts + "</select>Name:<input name=name required>Price:<input name=price required>Stock:<input name=stock required><b>Phone Pic:</b><input type=file name=pic accept=image/* capture=environment style=border:3px dashed #f68b1e;background:#fff3e0;padding:24px><button style=padding:20px;border-radius:12px;width:100%;margin-top:10px;font-weight:bold;border:none;font-size:24px;background:#f68b1e;color:white>POST WITH PHONE PIC</button></form></div
