from flask import Flask,request,redirect,session
import os,base64
app=Flask(__name__)
app.secret_key="v36dynamic"

shops={}
prods=[]
chats={}

def css():
 a="body{margin:0;background:#f0f2f5;padding-bottom:130px;font-family:Arial;font-size:28px}"
 b=".top{background:linear-gradient(90deg,#f68b1e,#ff9a3d);padding:16px;display:flex;gap:10px;position:sticky;top:0;z-index:100}"
 c=".card{background:white;border-radius:20px;padding:22px;margin:14px;box-shadow:0 5px 15px #0001;border-left:8px solid #f68b1e}"
 d=".btn{display:block;padding:22px;border-radius:16px;width:100%;text-align:center;text-decoration:none!important;font-weight:bold;font-size:24px;margin-top:12px;box-sizing:border-box;color:white!important}"
 e=".btn-o{background:#f68b1e}"
 f=".btn-b{background:#111}"
 g=".btn-w{background:white;color:#f68b1e!important;border:3px solid #f68b1e}"
 h=".bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:14px 0;border-top:4px solid #f68b1e;z-index:999}"
 i=".nav{text-align:center;text-decoration:none;color:#222;font-size:18px;font-weight:bold}"
 j="#map{height:65vh;width:100%;border-radius:18px}"
 k=".price{color:#f68b1e;font-weight:bold;font-size:28px}"
 return a+b+c+d+e+f+g+h+i+j+k

def nav():
 c=len(session.get("cart",[]))
 t="("+str(c)+")" if c>0 else ""
 return "<div class=bottom><a href='/' class='nav'>Market<br>🏪</a><a href='/map' class='nav'>GPS<br>📍</a><a href='/register' class='nav'>Register<br>➕</a><a href='/post' class='nav'>Post<br>📸</a><a href='/cart' class='nav'>Cart "+t+"<br>🛒</a><a href='/ai' class='nav'>AI<br>🤖</a></div>"

@app.route("/")
def home():
 s=css()
 h="<style>"+s+"</style>"
 h+="<div class=top><b style=color:white;font-size:32px>EAZYMADE MARKET</b></div>"
 h+="<div class='card' style='background:linear-gradient(135deg,#f68b1e,#000);color:white;text-align:center;border-left:none'><b style=font-size:32px>🛍️ All Shops</b><p style=font-size:22px>Big Font 28px - Map 65vh</p><p style=font-size:20px>"+str(len(shops))+" shops registered - dynamic</p><a href='/map' class='btn' style='background:white;color:#f68b1e!important'>📍 VIEW MAP FULL PAGE</a><a href='/register' class='btn' style='background:#0a8a0a;color:white'>➕ REGISTER YOUR SHOP</a><a href='/ai' class='btn btn-b'>🤖 AI Find Shoes</a></div>"
 if len(shops)==0:
  h+="<div class=card><b style=font-size:28px>No shops yet</b><br>Be first to register!<br><a href='/register' class='btn btn-o'>Register Shop Now</a></div>"
 for name in shops:
  sh=shops[name]
  tot=0
  for p in prods:
   if p["shop"]==name:
    tot+=int(p["stock"])
  h+="<div class=card><b style=font-size:28px>🏬 "+name+"</b><br><span style=font-size:20px>"+sh["area"]+" - "+str(tot)+" pairs TOTAL</span><a href='/shop/"+sh["own"]+"' class='btn btn-o'>Enter Whole Shop - "+str(tot)+" pairs</a><a href='/chat/"+sh["own"]+"' class='btn btn-b'>💬 Chat Before Visit</a><a href='https://www.google.com/maps?q="+str(sh["lat"])+","+str(sh["lng"])+"' target='_blank' class='btn btn-w'>📍 GPS Navigate</a></div>"
 for p in prods:
  h+="<div class=card><img src='"+p["img"]+"' style='width:100%;height:220px;object-fit:cover;border-radius:16px'><br><b style=font-size:26px>"+p["name"]+"</b><br><span class=price>KSh "+str(p["price"])+"</span> - "+p["shop"]+"<br>Stock "+str(p["stock"])+" pairs<a href='/add/"+str(p["id"])+"' class='btn btn-o'>🛒 Add to Cart</a></div>"
 h+="<div class=card><b style=font-size:30px>📍 All Shops Map 65vh</b><div id='map'></div></div>"
 h+="<link rel=stylesheet href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'><script src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'></script><script>var m=L.map('map').setView([-1.3956,36.7562],12);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(m);"
 for n in shops:
  sh=shops[n]
  h+="L.marker(["+str(sh["lat"])+","+str(sh["lng"])+"]).addTo(m).bindPopup('"+n+"');"
 h+="</script>"
 h+=nav()
 return h

@app.route("/map")
def mp():
 return home()

@app.route("/add/<int:pid>")
def add(pid):
 c=session.get("cart",[])
 c.append(pid)
 session["cart"]=c
 return redirect("/cart")

@app.route("/cart")
def cart():
 s=css()
 c=session.get("cart",[])
 h="<style>"+s+"</style><div class=top><b style=color:white>CART 28px</b></div>"
 tot=0
 cnt=0
 for pid in c:
  for p in prods:
   if p["id"]==pid:
    h+="<div class=card>"+p["name"]+" KSh "+str(p["price"])+"</div>"
    tot+=int(p["price"])
    cnt+=1
 h+="<div class=card style=background:#111;color:white;text-align:center><b style=font-size:32px>TOTAL "+str(cnt)+" pairs KSh "+str(tot)+"</b></div>"
 h+="<div class=card><a href='https://wa.me/254116782556?text=Order "+str(cnt)+" pairs KSh "+str(tot)+"' class='btn' style='background:#0a8a0a;color:white'>💬 WhatsApp Order</a><a href='/' class='btn btn-b'>Continue Shopping</a><a href='/clear' class='btn btn-w'>Clear Cart</a></div>"+nav()
 return h

@app.route("/clear")
def clear():
 session["cart"]=[]
 return redirect("/")

@app.route("/shop/<own>")
def shop(own):
 s=css()
 sn=""
 for n in shops:
  if shops[n]["own"]==own:
   sn=n
 if sn=="":
  return redirect("/")
 tot=0
 for p in prods:
  if p["shop"]==sn:
   tot+=int(p["stock"])
 h="<style>"+s+"</style><div class=top><b style=color:white>"+sn+"</b></div><div class=card style='background:linear-gradient(135deg,#f68b1e,#ff9a3d);color:white'><b style=font-size:30px>"+sn+"</b><br><b style=font-size:28px>"+str(tot)+" pairs TOTAL Whole Shop</b></div>"
 for p in prods:
  if p["shop"]==sn:
   h+="<div class=card><b>"+p["name"]+"</b> KSh "+str(p["price"])+"<a href='/add/"+str(p["id"])+"' class='btn btn-o'>Add to Cart</a></div>"
 h+=nav()
 return h

@app.route("/register",methods=["GET","POST"])
def register():
 s=css()
 if request.method=="POST":
  shop_name=request.form.get("shop","").strip()
  user=request.form.get("user","").strip().lower()
  area=request.form.get("area","").strip()
  till=request.form.get("till","").strip()
  if shop_name!="" and user!="":
   if shop_name not in shops:
    shops[shop_name]={"own":user,"ok":True,"lat":-1.3956,"lng":36.7562,"area":area if area!="" else "Rongai","till":till if till!="" else "0000"}
    chats[shop_name]=[]
   return redirect("/")
 h="<style>"+s+"</style><div class=top><b style=color:white>Register Shop</b></div>"
 h+="<div class=card><b style=font-size:28px>➕ Register Your Shop</b><p style=font-size:20px>Shop will appear instantly - no hardcoded shops</p><form method=post>"
 h+="<input name=user placeholder='Your username e.g. admin' required style=width:100%;padding:18px;font-size:22px;margin-top:10px;border-radius:12px;border:2px solid #ddd>"
 h+="<input name=shop placeholder='Shop name e.g. Rongai Shoe Center' required style=width:100%;padding:18px;font-size:22px;margin-top:10px;border-radius:12px;border:2px solid #ddd>"
 h+="<input name=area placeholder='Area e.g. Rongai Town' required style=width:100%;padding:18px;font-size:22px;margin-top:10px;border-radius:12px;border:2px solid #ddd>"
 h+="<input name=till placeholder='Till / Phone e.g. 0116782556' style=width:100%;padding:18px;font-size:22px;margin-top:10px;border-radius:12px;border:2px solid #ddd>"
 h+="<button class='btn btn-o' style=border:none;width:100%;margin-top:14px>Register Shop</button></form></div>"
 h+="<div class=card><b>Current shops: "+str(len(shops))+"</b><br>All dynamic - not hardcoded</div>"+nav()
 return h

@app.route("/chat/<own>",methods=["GET","POST"])
def chat(own):
 s=css()
 sn=""
 for n in shops:
  if shops[n]["own"]==own:
   sn=n
 if sn=="":
  return redirect("/")
 if sn not in chats:
  chats[sn]=[]
 if request.method=="POST":
  m=request.form.get("msg","")
  if m!="":
   chats[sn].append(m)
 h="<style>"+s+"</style><div class=top><b style=color:white>💬 Chat "+sn+"</b></div><div class=card><form method=post style=display:flex;gap:8px><input name=msg placeholder='Ask size price' style=flex:1;padding:18px;font-size:22px;border-radius:12px;border:2px solid #ddd><button style=padding:18px;background:#f68b1e;color:white;border:none;border-radius:12px;font-size:22px>Send</button></form></div><div class=card>"
 for mm in chats[sn][-10:]:
  h+="<div style=background:#f5f5f5;padding:12px;border-radius:10px;margin:6px 0>"+mm+"</div>"
 h+="</div><a href='/shop/"+own+"' class='btn btn-b' style=margin:14px>Back to Shop</a>"+nav()
 return h

@app.route("/ai",methods=["GET","POST"])
def ai():
 s=css()
 ans=""
 if request.method=="POST":
  q=request.form.get("q","").lower()
  if len
