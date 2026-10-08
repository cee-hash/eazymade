from flask import Flask,request,redirect,session
import os,base64
app=Flask(__name__)
app.secret_key="v34perfect"

shops={
"Rongai Shoe Center":{"own":"admin","ok":True,"lat":-1.3956,"lng":36.7562,"area":"Rongai Town","till":"0116782556"},
"Kitengela Sneakers":{"own":"kiten","ok":True,"lat":-1.38,"lng":36.78,"area":"Kitengela","till":"0712345678"},
"Kware Market":{"own":"kware","ok":True,"lat":-1.40,"lng":36.74,"area":"Kware","till":"0722000000"}
}
prods=[
{"id":1,"name":"Jordan 1 Retro","price":4500,"img":"https://via.placeholder.com/400","shop":"Rongai Shoe Center","stock":10},
{"id":2,"name":"Air Max 90","price":3800,"img":"https://via.placeholder.com/400","shop":"Kitengela Sneakers","stock":15}
]
chats={}

def css():
 a="body{margin:0;background:#f0f2f5;padding-bottom:130px;font-family:Arial;font-size:28px;line-height:1.4}"
 b=".top{background:linear-gradient(90deg,#f68b1e,#ff9a3d);padding:16px;display:flex;gap:10px;position:sticky;top:0;z-index:100;box-shadow:0 3px 12px #0003}"
 c=".logo{background:white;color:#f68b1e;width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:30px}"
 d=".card{background:white;border-radius:20px;padding:22px;margin:14px;box-shadow:0 5px 15px #0001;border-left:8px solid #f68b1e}"
 e=".btn{display:block;padding:20px;border-radius:16px;width:100%;text-align:center;text-decoration:none;font-weight:bold;font-size:24px;margin-top:12px;box-sizing:border-box}"
 f=".btn-o{background:linear-gradient(90deg,#f68b1e,#ff6a00);color:white}"
 g=".btn-b{background:#111;color:white}"
 h=".btn-w{background:white;color:#f68b1e;border:3px solid #f68b1e}"
 i=".bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:14px 0;border-top:4px solid #f68b1e;z-index:999}"
 j=".nav{text-align:center;text-decoration:none;color:#222;font-size:18px;font-weight:bold}"
 k="#map{height:65vh;width:100%;border-radius:18px}"
 l=".price{color:#f68b1e;font-weight:bold;font-size:28px}"
 return a+b+c+d+e+f+g+h+i+j+k+l

def nav():
 c=len(session.get("cart",[]))
 t="("+str(c)+")" if c>0 else ""
 return "<div class=bottom><a href=/ class=nav>Market<br>🏪</a><a href=/map class=nav>GPS<br>📍</a><a href=/post class=nav>Post<br>📸</a><a href=/cart class=nav>Cart "+t+"<br>🛒</a><a href=/ai class=nav>AI<br>🤖</a></div>"

@app.route("/")
def home():
 s=css()
 h="<style>"+s+"</style>"
 h+="<div class=top><div class=logo>E</div><b style=color:white;font-size:30px>EAZYMADE MARKET</b></div>"
 h+="<div class=card style=background:linear-gradient(135deg,#f68b1e,#000);color:white;text-align:center><b style=font-size:32px>🛍️ All Shops Decorated</b><p>Big Font 28px - Map 65vh</p><a href=/map class=btn style=background:white;color:#f68b1e>📍 VIEW MAP FULL PAGE</a><a href=/ai class=btn style=background:#111;color:white>🤖 AI Find Shoes</a></div>"
 for name in shops:
  sh=shops[name]
  tot=0
  for p in prods:
   if p["shop"]==name:
    tot+=int(p["stock"])
  h+="<div class=card><b style=font-size:28px>🏬 "+name+"</b><br><span style=font-size:20px>"+sh["area"]+" - "+str(tot)+" pairs TOTAL Whole Shop</span><a href=/shop/"+sh["own"]+" class=btn btn-o>Enter Whole Shop - "+str(tot)+" pairs</a><a href=/chat/"+sh["own"]+" class=btn btn-b>💬 Chat Before Visit</a><a href=https://www.google.com/maps?q="+str(sh["lat"])+","+str(sh["lng"])+" target=_blank class=btn btn-w>📍 GPS Navigate WORKS</a></div>"
 for p in prods:
  h+="<div class=card><img src="+p["img"]+" style=width:100%;height:220px;object-fit:cover;border-radius:16px><br><b style=font-size:26px>"+p["name"]+"</b><br><span class=price>KSh "+str(p["price"])+"</span> Stock "+str(p["stock"])+" pairs<a href=/add/"+str(p["id"])+" class=btn btn-o>🛒 Add to Cart WORKS</a></div>"
 h+="<div class=card><b style=font-size:30px>📍 All Shops Map 65vh</b><div id=map></div></div>"
 h+="<link rel=stylesheet href=https://unpkg.com/leaflet@1.9.4/dist/leaflet.css><script src=https://unpkg.com/leaflet@1.9.4/dist/leaflet.js></script><script>var m=L.map('map').setView([-1.3956,36.7562],12);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(m);L.marker([-1.3956,36.7562]).addTo(m).bindPopup('Rongai Shoe Center');L.marker([-1.38,36.78]).addTo(m).bindPopup('Kitengela');L.marker([-1.40,36.74]).addTo(m).bindPopup('Kware');</script>"
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
 h="<style>"+s+"</style><div class=top><div class=logo>E</div><b style=color:white>CART 28px</b></div>"
 tot=0
 cnt=0
 for pid in c:
  for p in prods:
   if p["id"]==pid:
    h+="<div class=card>"+p["name"]+" KSh "+str(p["price"])+"</div>"
    tot+=int(p["price"])
    cnt+=1
 h+="<div class=card style=background:#111;color:white;text-align:center><b style=font-size:32px>TOTAL "+str(cnt)+" pairs KSh "+str(tot)+"</b></div>"
 h+="<div class=card><a href=https://wa.me/254116782556?text=Order "+str(cnt)+" pairs KSh "+str(tot)+" class=btn style=background:#0a8a0a;color:white>💬 WhatsApp Order - Private Till</a><a href=/ class=btn btn-b>Continue Shopping</a><a href=/clear class=btn btn-w>Clear Cart</a></div>"+nav()
 return h

@app.route("/clear")
def clear():
 session["cart"]=[]
 return redirect("/")

@app.route("/shop/<own>")
def shop(own):
 s=css()
 sn="Rongai Shoe Center"
 for n in shops:
  if shops[n]["own"]==own:
   sn=n
 tot=0
 for p in prods:
  if p["shop"]==sn:
   tot+=int(p["stock"])
 h="<style>"+s+"</style><div class=top><div class=logo>E</div><b style=color:white>"+sn+"</b></div><div class=card style=background:linear-gradient(135deg,#f68b1e,#ff9a3d);color:white><b style=font-size:30px>"+sn+"</b><br><b style=font-size:28px>"+str(tot)+" pairs TOTAL Whole Shop</b><br>"+shops[sn]["area"]+"<a href=/chat/"+own+" class=btn style=background:white;color:#f68b1e>💬 Chat Shop</a></div>"
 for p in prods:
  if p["shop"]==sn:
   h+="<div class=card><b>"+p["name"]+"</b> KSh "+str(p["price"])+"<a href=/add/"+str(p["id"])+" class=btn btn-o>Add to Cart WORKS</a></div>"
 h+=nav()
 return h

@app.route("/chat/<own>",methods=["GET","POST"])
def chat(own):
 s=css()
 sn="Rongai Shoe Center"
 for n in shops:
  if shops[n]["own"]==own:
   sn=n
 if sn not in chats:
  chats[sn]=[]
 if request.method=="POST":
  m=request.form.get("msg","")
  if m!="":
   chats[sn].append(m)
 h="<style>"+s+"</style><div class=top><div class=logo>E</div><b style=color:white>💬 Chat "+sn+"</b></div><div class=card><form method=post style=display:flex;gap:8px><input name=msg placeholder=Ask size price required style=flex:1;padding:18px;font-size:22px;border-radius:12px;border:2px solid #ddd><button style=padding:18px;background:#f68b1e;color:white;border:none;border-radius:12px;font-size:22px>Send WORKS</button></form></div><div class=card>"
 for mm in chats[sn][-10:]:
  h+="<div style=background:#f5f5f5;padding:12px;border-radius:10px;margin:6px 0>"+mm+"</div>"
 h+="</div><a href=/shop/"+own+" class=btn btn-b style=margin:14px>Back to Shop WORKS</a>"+nav()
 return h

@app.route("/ai",methods=["GET","POST"])
def ai():
 s=css()
 ans=""
 if request.method=="POST":
  q=request.form.get("q","").lower()
  if "jordan" in q:
   ans="AI: Jordan 1 Retro KSh 4500 - Rongai Shoe Center - 10 pairs - GPS -1.3956,36.7562"
  elif "cheap" in q:
   ans="AI: Cheapest Air Max 90 KSh 3800 - Kitengela - 15 pairs - Best deal"
  else:
   ans="AI: All shops "+str(len(prods))+" products - Total "+str(sum(int(p["stock"]) for p in prods))+" pairs - Try jordan cheap"
 h="<style>"+s+"</style><div class=top><div class=logo>🤖</div><b style=color:white;font-size:28px>AI Assistant Big Font</b></div><div class=card style=background:#111;color:white><form method=post><input name=q placeholder=cheap jordans size 43 style=width:100%;padding:20px;font-size:24px;border-radius:14px><button class=btn btn-o style=border:none>Ask AI WORKS 24px</button></form></div>"
 if ans!="":
  h+="<div class=card style=border-left:8px solid #0a8a0a><b style=font-size:26px>"+ans+"</b></div>"
 h+=nav()
 return h

@app.route("/post",methods=["GET","POST"])
def post():
 s=css()
 if request.method=="POST":
  img="https://via.placeholder.com/400"
  f=request.files.get("pic")
  if f and f.filename!="":
   img="data:image/jpeg;base64,"+base64.b64encode(f.read()).decode()
  prods.append({"id":len(prods)+1,"name":request.form["name"],"price":request.form["price"],"img":img,"shop":"Rongai Shoe Center","stock":request.form["stock"]})
  return redirect("/")
 return "<style>"+s+"</style><div class=top><div class=logo>E</div><b style=color:white>Post Upload 28px</b></div><div class=card><form method=post enctype=multipart/form-data><input name=name placeholder=Name required style=width:100%;padding:18px;font-size:22px><input name=price placeholder=Price required style=width:100%;padding:18px;font-size:22px><input name=stock placeholder=Stock pairs required style=width:100%;padding:18px;font-size:22px><input type=file name=pic accept=image/* capture=environment style=width:100%;padding:18px;border:3px dashed #f68b1e;background:#fff3e0;border-radius:14px><button class=btn btn-o style=border:none>POST BIG FONT WORKS</button></form></div>"+nav()

@app.route("/office",methods=["GET","POST"])
def office():
 s=css()
 if request.method=="POST":
  if request.form.get("password")=="0116782556":
   session["off"]=True
 if not session.get("off"):
  return "<style>"+s+"</style><div class=card style=max-width:400px;margin:60px auto><b>Office Login</b><form method=post><input name=password type=password placeholder=0116782556 style=width:100%;padding:18px;font-size:24px><button class=btn btn-b style=border:none>Enter WORKS</button></form></div>"+nav()
 h="<style>"+s+"</style><div class=card><b style=font-size:30px>Office - All Shops</b></div>"
 for n in shops:
  h+="<div class=card>"+n+" - Till "+shops[n]["till"]+" - Area "+shops[n]["area"]+"</div>"
 h+=nav()
 return h

if __name__=="__main__":
 app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
