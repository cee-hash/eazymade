from flask import Flask,request,redirect,session
import os,base64,urllib.parse
app=Flask(__name__)
app.secret_key="v39social"

shops={}
prods=[]
chats={}

def auto_samples(shop_name):
 samples=[
  ["Jordan 1 Retro High","5500","12"],
  ["Air Force 1 White","4800","15"],
  ["Yeezy Boost 350","5200","8"],
  ["Jordan 4 Black","6000","10"],
  ["Nike Dunk Low","4700","20"],
 ]
 for nm,pr,st in samples:
  prods.append({"id":len(prods)+1,"name":nm,"price":pr,"img":"https://via.placeholder.com/400?text="+nm.replace(" ","+"),"shop":shop_name,"stock":st})

def css():
 a="body{margin:0;background:#f0f2f5;padding-bottom:140px;font-family:Arial;font-size:32px}"
 b=".top{background:linear-gradient(90deg,#f68b1e,#ff9a3d);padding:20px;position:sticky;top:0;z-index:100}"
 c=".card{background:white;border-radius:22px;padding:26px;margin:16px;box-shadow:0 6px 18px #0001;border-left:10px solid #f68b1e;font-size:30px}"
 d=".btn{display:block;padding:26px;border-radius:18px;width:100%;text-align:center;text-decoration:none!important;font-weight:bold;font-size:26px;margin-top:14px;color:white!important}"
 e=".btn-o{background:linear-gradient(90deg,#f68b1e,#ff6a00)}"
 f=".btn-b{background:#111}"
 g=".btn-w{background:white;color:#f68b1e!important;border:3px solid #f68b1e}"
 h=".bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:16px 0;border-top:5px solid #f68b1e;z-index:999}"
 i=".nav{text-align:center;text-decoration:none;color:#222;font-size:20px;font-weight:bold}"
 j="#map{height:65vh;width:100%;border-radius:20px}"
 k=".chat-msg{background:#f0f2f5;padding:18px;border-radius:16px;margin:10px 0;font-size:28px;border-left:6px solid #f68b1e}"
 l=".share-wa{background:#25D366}"
 m=".share-fb{background:#1877F2}"
 n=".share-tt{background:#000}"
 return a+b+c+d+e+f+g+h+i+j+k+l+m+n

def nav():
 c=session.get("cart",[])
 t=""
 if c:
  t="("+str(len(c))+")"
 return "<div class=bottom><a href='/' class='nav'>Market<br>🏪</a><a href='/register' class='nav'>Register<br>➕</a><a href='/post' class='nav'>Post<br>📸</a><a href='/cart' class='nav'>Cart "+t+"<br>🛒</a><a href='/ai' class='nav'>AI<br>🤖</a></div>"

@app.route("/")
def home():
 s=css()
 h="<style>"+s+"</style><div class=top><b style=color:white;font-size:36px>EAZYMADE AUTO SOCIAL</b><div style=color:white;font-size:20px>Auto Post TikTok WhatsApp Facebook</div></div>"
 h+="<div class='card' style='background:linear-gradient(135deg,#f68b1e,#000);color:white;border-left:none;text-align:center'><b style=font-size:36px>🛍️ Market Auto Social</b><p>"+str(len(shops))+" shops - "+str(len(prods))+" products</p></div>"
 if not shops:
  h+="<div class=card><b>No shops yet</b><a href='/register' class='btn btn-o'>Register + Auto Social Post</a></div>"
 for name in shops:
  sh=shops[name]
  tot=0
  stock_tot=0
  for p in prods:
   if p["shop"]==name:
    tot+=1
    stock_tot+=int(p["stock"])
  msg="🔥 NEW SHOP on EAZYMADE MARKET! 🏬 "+name+" - "+sh["area"]+" - "+str(tot)+" types "+str(stock_tot)+" pairs! 📍 GPS: https://www.google.com/maps?q="+str(sh["lat"])+","+str(sh["lng"])+" - Shop now on EazyMade!"
  enc=urllib.parse.quote(msg)
  h+="<div class=card><b style=font-size:32px>🏬 "+name+"</b><br>"+sh["area"]+" - "+str(tot)+" types "+str(stock_tot)+" pairs<a href='/shop/"+sh["own"]+"' class='btn btn-o'>Enter Shop "+str(stock_tot)+" pairs</a>"
  h+="<div style=display:flex;gap:8px;margin-top:12px><a href='https://wa.me/?text="+enc+"' target=_blank class='btn share-wa' style=flex:1;font-size:20px>WhatsApp</a><a href='https://www.facebook.com/sharer/sharer.php?u=https://eazymade-market.com&quote="+enc+"' target=_blank class='btn share-fb' style=flex:1;font-size:20px>Facebook</a><a href='/share/"+sh["own"]+"' class='btn share-tt' style=flex:1;font-size:20px>TikTok</a></div>"
  h+="<a href='/chat/"+sh["own"]+"' class='btn btn-b'>💬 Chat Big Font</a></div>"
 for p in prods:
  h+="<div class=card><img src='"+p["img"]+"' style='width:100%;height:260px;object-fit:cover;border-radius:18px'><br><b style=font-size:32px>"+p["name"]+"</b><br>KSh "+str(p["price"])+" - "+p["shop"]+"</div>"
 h+="<div class=card><b>📍 Map 65vh</b><div id='map'></div></div><link rel=stylesheet href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'><script src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'></script><script>var m=L.map('map').setView([-1.3956,36.7562],12);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(m);"
 for n in shops:
  sh=shops[n]
  h+="L.marker(["+str(sh["lat"])+","+str(sh["lng"])+"]).addTo(m).bindPopup('"+n+"');"
 h+="</script>"+nav()
 return h

@app.route("/share/<own>")
def share(own):
 s=css()
 sn=""
 for n in shops:
  if shops[n]["own"]==own:
   sn=n
 if not sn:
  return redirect("/")
 sh=shops[sn]
 tot=0
 stock_tot=0
 for p in prods:
  if p["shop"]==sn:
   tot+=1
   stock_tot+=int(p["stock"])
 msg="🔥 NEW SHOP ALERT on EAZYMADE MARKET! 🏪\n\n🏬 "+sn+"\n📍 "+sh["area"]+"\n👟 "+str(tot)+" types - "+str(stock_tot)+" pairs WHOLE SHOP\n\n💬 Chat before visit\n📍 GPS Navigate available\n🛒 Add to Cart + WhatsApp Order\n\n👉 Visit EazyMade Market now!\n\n#Rongai #Shoes #Kenya #EazyMade"
 msg2="🔥 NEW SHOP "+sn+" "+str(stock_tot)+" pairs! EAZYMADE MARKET Rongai - Check it now! https://www.google.com/maps?q="+str(sh["lat"])+","+str(sh["lng"])
 enc=urllib.parse.quote(msg)
 enc2=urllib.parse.quote(msg2)
 enc_url=urllib.parse.quote("https://eazymade-market.com/shop/"+own)
 h="<style>"+s+"</style><div class=top><b style=color:white;font-size:32px>Auto Social Post - "+sn+"</b></div>"
 h+="<div class=card style='background:linear-gradient(135deg,#25D366,#128C7E);color:white;border-left:none;text-align:center'><b style=font-size:34px>✅ Shop Registered + Auto Posted 5 Shoes!</b><p style=font-size:26px>Now Auto Post on TikTok WhatsApp Facebook - 1 Click Viral</p></div>"
 h+="<div class=card><b style=font-size:32px>📱 Your Viral Post Text - Big Font - Auto Generated</b><div style=background:#f0f2f5;padding:18px;border-radius:14px;font-size:22px;white-space:pre-wrap;margin-top:12px;border-left:6px solid #f68b1e>"+msg+"</div>"
 h+="<a href='https://wa.me/?text="+enc+"' target=_blank class='btn share-wa' style=font-size:30px;margin-top:14px>📱 AUTO POST WhatsApp Status + Groups</a>"
 h+="<a href='https://wa.me/254116782556?text="+enc+"' target=_blank class='btn' style=background:#111;color:white;font-size:24px;margin-top:10px>💬 Share to WhatsApp Direct</a>"
 h+="<a href='https://www.facebook.com/sharer/sharer.php?u="+enc_url+"&quote="+enc+"' target=_blank class='btn share-fb' style=font-size:30px;margin-top:10px>📘 AUTO POST Facebook Page + Groups</a>"
 h+="<a href='https://www.tiktok.com/upload?caption="+enc2+"' target=_blank class='btn share-tt' style=font-size:28px;margin-top:10px>🎵 AUTO POST TikTok - Open TikTok Upload</a>"
 h+="<div class=card style=background:#fff3e0;border-left:10px solid #000><b>TikTok Instructions Big Font:</b><br><span style=font-size:24px>1. Click TikTok button above<br>2. TikTok app opens with caption ready<br>3. Add video of your shoes (10 sec)<br>4. Post - your shop goes viral!<br><br>Caption auto copied: "+msg2+"</span><br><button onclick=\"navigator.clipboard.writeText(`"+msg2+"`)\" class='btn btn-o' style=border:none;width:100%;margin-top:10px>📋 Copy TikTok Caption</button></div>"
 h+="<div class=card><a href='/' class='btn btn-o' style=font-size:30px>✅ Done - Go to Market Big Font</a></div>"
 h+=nav()
 return h

@app.route("/autopost/<own>")
def autopost(own):
 sn=""
 for n in shops:
  if shops[n]["own"]==own:
   sn=n
 if sn:
  auto_samples(sn)
 return redirect("/share/"+own)

@app.route("/add/<int:pid>")
def add(pid):
 c=session.get("cart",[])
 c.append(pid)
 session["cart"]=c
 return redirect("/cart")

@app.route("/cart")
def cart():
 s=css()
 h="<style>"+s+"</style><div class=top><b style=color:white>CART</b></div>"
 for pid in session.get("cart",[]):
  for p in prods:
   if p["id"]==pid:
    h+="<div class=card><b>"+p["name"]+"</b></div>"
 h+="<div class=card><a href='/' class='btn btn-b'>Continue</a><a href='/clear' class='btn btn-w'>Clear</a></div>"+nav()
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
 tot=0
 stock_tot=0
 for p in prods:
  if p["shop"]==sn:
   tot+=1
   stock_tot+=int(p["stock"])
 h="<style>"+s+"</style><div class=top><b style=color:white>"+sn+"</b></div><div class=card style='background:linear-gradient(135deg,#f68b1e,#ff9a3d);color:white'><b style=font-size:34px>"+sn+"</b><br>"+str(tot)+" types "+str(stock_tot)+" pairs</div>"
 for p in prods:
  if p["shop"]==sn:
   h+="<div class=card><b>"+p["name"]+"</b><br>KSh "+str(p["price"])+"<a href='/add/"+str(p["id"])+"' class='btn btn-o'>Add</a></div>"
 h+="<div class=card><a href='/share/"+own+"' class='btn share-wa' style=font-size:26px>📱 Share Shop WhatsApp Facebook TikTok</a><a href='/chat/"+own+"' class='btn btn-b'>Chat</a></div>"+nav()
 return h

@app.route("/register",methods=["GET","POST"])
def register():
 s=css()
 if request.method=="POST":
  shop_name=request.form.get("shop","").strip()
  user=request.form.get("user","").strip().lower()
  area
