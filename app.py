from flask import Flask, request, redirect, session
import os, base64
app=Flask(__name__)
app.secret_key="v20-all"
shops={"Rongai Shoe Center":{"own":"admin","till":"0116782556","ok":True,"lat":-1.3956,"lng":36.7562,"area":"Rongai Town"}}
prods=[{"id":1,"name":"Jordan 1","price":4500,"img":"https://via.placeholder.com/400","shop":"Rongai Shoe Center","stock":10}]
users={"admin":{"shop":"Rongai Shoe Center","pass":"0116782556"}}

S='<style>body{margin:0;background:#f0f2f5;padding-bottom:110px;font-size:24px;font-family:Arial}.card{background:white;border-radius:16px;padding:18px;margin:12px;box-shadow:0 3px 10px #aaa}.btn{padding:20px;border-radius:12px;width:100%;margin-top:10px;font-weight:bold;border:none;font-size:24px}.btn-o{background:#f68b1e;color:white}.btn-b{background:#000;color:white}.btn-g{background:green;color:white}.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:14px 0;border-top:3px solid #f68b1e;z-index:9999}.nav{text-align:center;font-size:16px;font-weight:bold;text-decoration:none;color:#000;position:relative}.badge{background:red;color:white;border-radius:50%;padding:2px 8px;font-size:14px;position:absolute;top:-8px;right:0}#map{height:85vh;width:100%}input{width:100%;padding:18px;margin:8px 0;border-radius:12px;border:2px solid #ddd;font-size:20px}</style>'
H='<div style="background:#f68b1e;padding:14px;display:flex;gap:12px"><div style="background:white;color:#f68b1e;width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:28px">E</div><b style="color:white;font-size:28px">EAZYMADE MARKET</b></div>'

def bot():
 c=len(session.get("cart",[]))
 b='<span class=badge>'+str(c)+'</span>' if c>0 else ''
 return '<div class=bottom><a href="/" class=nav>🏪<br>Market</a><a href="/map" class=nav>📍<br>GPS</a><a href="/post" class=nav>📸<br>Post</a><a href="/cart" class=nav>🛒<br>Cart'+b+'</a><a href="/register" class=nav>👤<br>Join</a></div>'

@app.route("/")
def home():
 h=S+H+'<div style="background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:26px;border-radius:16px;margin:12px;text-align:center"><h2 style="font-size:34px">EAZYMADE MARKET</h2><p>All Shops - Whole Page Map - Big Font</p><a href="/map"><button class=btn style="background:white;color:#f68b1e">VIEW GPS MAP - ALL SHOPS</button></a></div>'
 for n,s in shops.items():
  if not s["ok"]: continue
  cnt=sum(1 for p in prods if p["shop"]==n)
  tot=sum(int(p["stock"]) for p in prods if p["shop"]==n)
  h+='<div class=card style="border-left:8px solid #f68b1e"><b style="font-size:26px">'+n+'</b><br><span style="font-size:20px">'+s["area"]+' - '+str(cnt)+' types - '+str(tot)+' pairs TOTAL (Whole Shop)</span><br><a href="/shop/'+s["own"]+'"><button class="btn btn-o">Enter Whole Shop - '+str(tot)+' pairs</button></a><a href="https://www.google.com/maps?q='+str(s["lat"])+','+str(s["lng"])+'" target=_blank><button class="btn btn-b">GPS Navigate to Shop</button></a></div>'
 for p in prods:
  h+='<div class=card><img src="'+p["img"]+'" style="width:100%;height:220px;object-fit:cover;border-radius:12px;background:#eee"><br><b style="font-size:24px">'+p["name"]+'</b> ('+p["shop"]+')<br>KSh '+str(p["price"])+' | Stock '+str(p["stock"])+'<br><a href="/add/'+str(p["id"])+'"><button class="btn btn-o">🛒 Add to Cart - BIG</button></a></div>'
 h+=bot()
 return h

@app.route("/shop/<own>")
def shop(own):
 s=next((shops[n] for n in shops if shops[n]["own"]==own),None)
 if not s: return redirect("/")
 h=S+H+'<div class=card><h2 style="font-size:30px">'+own+' WHOLE SHOP</h2><p>View before visiting - '+str(sum(int(p["stock"]) for p in prods if p["shop"]==s.get("area") or True))+' pairs</p><a href="https://www.google.com/maps?q='+str(s["lat"])+','+str(s["lng"])+'" target=_blank><button class="btn btn-b">Navigate GPS - Full Page</button></a></div>'
 for p in [x for x in prods if x["shop"]==next((n for n in shops if shops[n]["own"]==own), "") or x["shop"] in shops]:
  if p["shop"]!=next((n for n in shops if shops[n]["own"]==own),None):
   pass
 h=S+H
 shop_name = next((n for n in shops if shops[n]["own"]==own), list(shops.keys())[0])
 h+='<div class=card><h2>'+shop_name+' - WHOLE SHOP</h2><b>'+str(sum(int(x["stock"]) for x in prods if x["shop"]==shop_name))+' pairs TOTAL</b><br><a href="https://www.google.com/maps?q='+str(shops[shop_name]["lat"])+','+str(shops[shop_name]["lng"])+'" target=_blank><button class="btn btn-b">GPS Navigate</button></a></div>'
 for p in [x for x in prods if x["shop"]==shop_name]:
  h+='<div class=card><img src="'+p["img"]+'" style="width:100%;height:200px;object-fit:cover;border-radius:12px"><br><b>'+p["name"]+'</b> KSh '+str(p["price"])+' Stock '+str(p["stock"])+'<br><a href="/add/'+str(p["id"])+'"><button class="btn btn-o">Add to Cart</button></a></div>'
 h+=bot()
 return h

@app.route("/add/<int:pid>")
def add(pid):
 c=session.get("cart",[])
 c.append(pid)
 session["cart"]=c
 return redirect("/cart")

@app.route("/cart")
def cart():
 c=session.get("cart",[])
 h=S+H+'<div class=card><h2>🛒 Cart - Whole Shop Total</h2>'
 tot=0
 cnt=0
 for pid in c:
  p=next((x for x in prods if x["id"]==pid),None)
  if p:
   h+='<div class=card style="border-left:6px solid #f68b1e"><img src="'+p["img"]+'" style="width:100%;height:120px;object-fit:cover"><br>'+p["name"]+' KSh '+str(p["price"])+'</div>'
   tot+=int(p
