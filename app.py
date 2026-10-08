from flask import Flask,request,redirect,session
import os,base64
app=Flask(__name__)
app.secret_key="v36slow"

shops={}
prods=[]
chats={}

def css():
 a="body{margin:0;background:#f0f2f5;padding-bottom:130px;font-family:Arial;font-size:28px}"
 b=".top{background:linear-gradient(90deg,#f68b1e,#ff9a3d);padding:16px;position:sticky;top:0;z-index:100}"
 c=".card{background:white;border-radius:20px;padding:22px;margin:14px;box-shadow:0 5px 15px #0001;border-left:8px solid #f68b1e}"
 d=".btn{display:block;padding:22px;border-radius:16px;width:100%;text-align:center;text-decoration:none!important;font-weight:bold;font-size:24px;margin-top:12px;color:white!important}"
 e=".btn-o{background:#f68b1e}"
 f=".btn-b{background:#111}"
 g=".btn-w{background:white;color:#f68b1e!important;border:3px solid #f68b1e}"
 h=".bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:14px 0;border-top:4px solid #f68b1e;z-index:999}"
 i=".nav{text-align:center;text-decoration:none;color:#222;font-size:18px;font-weight:bold}"
 j="#map{height:65vh;width:100%;border-radius:18px}"
 return a+b+c+d+e+f+g+h+i+j

def nav():
 c=session.get("cart",[])
 t=""
 if c:
  t="("+str(len(c))+")"
 return "<div class=bottom><a href='/' class='nav'>Market<br>🏪</a><a href='/register' class='nav'>Register<br>➕</a><a href='/post' class='nav'>Post<br>📸</a><a href='/cart' class='nav'>Cart "+t+"<br>🛒</a><a href='/ai' class='nav'>AI<br>🤖</a></div>"

@app.route("/")
def home():
 s=css()
 h="<style>"+s+"</style>"
 h+="<div class=top><b style=color:white;font-size:32px>EAZYMADE</b></div>"
 h+="<div class='card' style='background:linear-gradient(135deg,#f68b1e,#000);color:white;border-left:none;text-align:center'><b>🛍️ All Shops</b><p>"+str(len(shops))+" shops - dynamic</p><a href='/register' class='btn' style='background:#0a8a0a;color:white'>➕ REGISTER YOUR SHOP</a></div>"
 if not shops:
  h+="<div class=card><b>No shops yet</b><br>Be first!<br><a href='/register' class='btn btn-o'>Register Now</a></div>"
 for name in shops:
  sh=shops[name]
  tot=0
  for p in prods:
   if p["shop"]==name:
    tot+=1
  h+="<div class=card><b>🏬 "+name+"</b><br>"+sh["area"]+" - "+str(tot)+" types<a href='/shop/"+sh["own"]+"' class='btn btn-o'>Enter Shop - "+str(tot)+" types</a><a href='/chat/"+sh["own"]+"' class='btn btn-b'>Chat</a><a href='https://www.google.com/maps?q="+str(sh["lat"])+","+str(sh["lng"])+"' target=_blank class='btn btn-w'>GPS Navigate</a></div>"
 for p in prods:
  h+="<div class=card><img src='"+p["img"]+"' style='width:100%;height:200px;object-fit:cover;border-radius:16px'><br><b>"+p["name"]+"</b><br>KSh "+str(p["price"])+"<a href='/add/"+str(p["id"])+"' class='btn btn-o'>Add to Cart</a></div>"
 h+="<div class=card><b>📍 Map 65vh</b><div id='map'></div></div>"
 h+="<link rel=stylesheet href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'><script src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'></script><script>var m=L.map('map').setView([-1.3956,36.7562],12);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(m);"
 for n in shops:
  sh=shops[n]
  h+="L.marker(["+str(sh["lat"])+","+str(sh["lng"])+"]).addTo(m).bindPopup('"+n+"');"
 h+="</script>"+nav()
 return h

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
 h="<style>"+s+"</style><div class=top><b style=color:white>CART</b></div>"
 tot=0
 cnt=0
 for pid in c:
  for p in prods:
   if p["id"]==pid:
    h+="<div class=card>"+p["name"]+"</div>"
    tot+=1
 h+="<div class=card><b>TOTAL "+str(tot)+" pairs</b></div><div class=card><a href='/' class='btn btn-b'>Continue Shopping</a><a href='/clear' class='btn btn-w'>Clear</a></div>"+nav()
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
 if not sn:
  return redirect("/")
 h="<style>"+s+"</style><div class=top><b style=color:white>"+sn+"</b></div>"
 for p in prods:
  if p["shop"]==sn:
   h+="<div class=card><b>"+p["name"]+"</b><a href='/add/"+str(p["id"])+"' class='btn btn-o'>Add to Cart</a></div>"
 h+=nav()
 return h

@app.route("/register",methods=["GET","POST"])
def register():
 s=css()
 if request.method=="POST":
  shop_name=request.form.get("shop","")
  user=request.form.get("user","")
  area=request.form.get("area","")
  till=request.form.get("till","")
  shop_name=shop_name.strip()
  user=user.strip().lower()
  if shop_name:
   if user:
    if shop_name not in shops:
     shops[shop_name]={"own":user,"lat":-1.3956,"lng":36.7562,"area":area,"till":till}
     chats[shop_name]=[]
    return redirect("/")
 h="<style>"+s+"</style><div class=top><b style=color:white>Register</b></div><div class=card><b>Register Shop</b><form method=post><input name=user placeholder='username e.g admin' required style=width:100%;padding:18px;margin-top:10px><input name=shop placeholder='Shop name' required style=width:100%;padding:18px;margin-top:10px><input name=area placeholder='Area Rongai' required style=width:100%;padding:18px;margin-top:10px><input name=till placeholder='Till 0116782556' style=width:100%;padding:18px;margin-top:10px><button class='btn btn-o' style=border:none;width:100%;margin-top:12px>Register Shop</button></form></div>"+nav()
 return h

@app.route("/chat/<own>",methods=["GET","POST"])
def chat(own):
 s=css()
 sn=""
 for n in shops:
  if shops[n]["own"]==own:
   sn=n
 if not sn:
  return redirect("/")
 if sn not in chats:
  chats[sn]=[]
 if request.method=="POST":
  m=request.form.get("msg","")
  if m:
   chats[sn].append(m)
 h="<style>"+s+"</style><div class=top><b style=color:white>Chat "+sn+"</b></div><div class=card><form method=post style=display:flex;gap:8px><input name=msg placeholder='Ask' style=flex:1;padding:18px><button style=padding:18px;background:#f68b1e;color:white;border:none;border-radius:12px>Send</button></form></div><div class=card>"
 for mm in chats[sn]:
  h+="<div style=background:#f5f5f5;padding:10px;margin:6px 0>"+mm+"</div>"
 h+="</div>"+nav()
 return h

@app.route("/ai",methods=["GET","POST"])
def ai():
 s=css()
 ans=""
 if request.method=="POST":
  ans="Found "+str(len(prods))+" products"
 h="<style>"+s+"</style><div class=top><b style=color:white>AI</b></div><div class=card><form method=post><input name=q placeholder='search' style=width:100%;padding:20px><button class='btn btn-o' style=border:none;width:100%>Ask AI</button></form></div>"
 if ans:
  h+="<div class=card><b>"+ans+"</b></div>"
 h+=nav()
 return h

@app.route("/post",methods=["GET","POST"])
def post():
 s=css()
 if request.method=="POST":
  img="https://via.placeholder.com/400"
  f=request.files.get("pic")
  if f:
   if f.filename!="":
    img="data:image/jpeg;base64,"+base64.b64encode(f.read()).decode()
  shop_name=request.form.get("shop_select","")
  if not shop_name:
   if shops:
    shop_name=list(shops.keys())[0]
  prods.append({"id":len(prods)+1,"name":request.form["name"],"price":request.form["price"],"img":img,"shop":shop_name,"stock":request.form["stock"]})
  return redirect("/")
 if not shops:
  return "<style>"+s+"</style><div class=card><b>No shops yet</b><br><a href='/register' class='btn btn-o'>Register Shop</a></div>"+nav()
 opts=""
 for n in shops:
  opts+="<option value='"+n+"'>"+n+"</option>"
 return "<style>"+s+"</style><div class=top><b style=color:white>Post</b></div><div class=card><form method=post enctype=multipart/form-data><select name=shop_select style=width:100%;padding:18px>"+opts+"</select><input name=name placeholder='Name' required style=width:100%;padding:18px;margin-top:10px><input name=price placeholder='Price' required style=width:100%;padding:18px;margin-top:10px><input name=stock placeholder='Stock' required style=width:100%;padding:18px;margin-top:10px><input type=file name=pic accept='image/*' capture='environment' style=width:100%;padding:18px;margin-top:10px><button class='btn btn-o' style=border:none;width:100%;margin-top:10px>Post</button></form></div>"+nav()

@app.route("/office",methods=["GET","POST"])
def office():
 s=css()
 if request.method=="POST":
  pw=request.form.get("password","")
  if pw=="0116782556":
   session["off"]=True
 if not session.get("off"):
  return "<style>"+s+"</style><div class=card><b>Office</b><form method=post><input name=password type=password placeholder='0116782556' style=width:100%;padding:18px><button class='btn btn-b' style=border:none;width:100%>Enter</button></form></div>"+nav()
 h="<style>"+s+"</style><div class=card><b>Office "+str(len(shops))+" shops</b></div>"
 for n in shops:
  h+="<div class=card>"+n+" - "+shops[n]["area"]+"</div>"
 h+=nav()
 return h

if __name__=="__main__":
 app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
