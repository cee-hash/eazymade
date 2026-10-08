from flask import Flask,request,redirect,session
import os,base64,urllib.parse
from datetime import datetime
app=Flask(__name__)
app.secret_key="v41business"

shops={}
prods=[]
chats={}

DELIVERY=300
SALE_CUT=0.05
DELIVERY_CUT=0.5
SUB_FEE=500

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
 a="body{margin:0;background:#f0f2f5;padding-bottom:140px;font-family:Arial;font-size:30px}"
 b=".top{background:linear-gradient(90deg,#f68b1e,#ff9a3d);padding:20px;position:sticky;top:0;z-index:100}"
 c=".card{background:white;border-radius:22px;padding:26px;margin:16px;box-shadow:0 6px 18px #0001;border-left:10px solid #f68b1e}"
 d=".btn{display:block;padding:26px;border-radius:18px;width:100%;text-align:center;text-decoration:none!important;font-weight:bold;font-size:26px;margin-top:14px;color:white!important}"
 e=".btn-o{background:linear-gradient(90deg,#f68b1e,#ff6a00)}"
 f=".btn-b{background:#111}"
 g=".btn-w{background:white;color:#f68b1e!important;border:3px solid #f68b1e}"
 h=".bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:16px 0;border-top:5px solid #f68b1e;z-index:999}"
 i=".nav{text-align:center;text-decoration:none;color:#222;font-size:20px;font-weight:bold}"
 j="#map{height:65vh;width:100%;border-radius:20px}"
 k=".chat-msg{background:#f0f2f5;padding:18px;border-radius:16px;margin:10px 0;font-size:26px;border-left:6px solid #f68b1e}"
 return a+b+c+d+e+f+g+h+i+j+k

def nav():
 c=session.get("cart",[])
 t=""
 if c:
  t="("+str(len(c))+")"
 return "<div class=bottom><a href='/' class='nav'>Market<br>🏪</a><a href='/register' class='nav'>Register<br>➕</a><a href='/post' class='nav'>Post<br>📸</a><a href='/cart' class='nav'>Cart "+t+"<br>🛒</a><a href='/office' class='nav'>Office<br>💼</a></div>"

@app.errorhandler(404)
def nf(e):
 return redirect("/")

@app.route("/")
def home():
 s=css()
 h="<style>"+s+"</style><div class=top><b style=color:white;font-size:34px>EAZYMADE MARKET</b><div style=color:white;font-size:20px>Shops Near You - Rongai Kitengela Kware</div></div>"
 h+="<div class='card' style='background:linear-gradient(135deg,#f68b1e,#000);color:white;border-left:none;text-align:center'><b style=font-size:34px>🛍️ Welcome</b><p style=font-size:24px>"+str(len(shops))+" Shops - "+str(len(prods))+" Shoes Available</p><a href='/register' class='btn' style='background:#0a8a0a'>➕ Register Your Shop</a><a href='/map' class='btn' style='background:white;color:#f68b1e!important'>📍 View Map</a></div>"
 if not shops:
  h+="<div class=card><b>🏬 No shops yet</b><br><span style=font-size:24px>Be the first to register your shoe shop in Rongai</span><br><a href='/register' class='btn btn-o'>Register Shop Now</a></div>"
 for name in shops:
  sh=shops[name]
  if not sh.get("sub",True):
   continue
  tot=0
  stock_tot=0
  for p in prods:
   if p["shop"]==name:
    tot+=1
    stock_tot+=int(p["stock"])
  msg="🔥 "+name+" - "+sh["area"]+" - "+str(stock_tot)+" pairs available! Visit EAZYMADE MARKET"
  enc=urllib.parse.quote(msg)
  h+="<div class=card><b style=font-size:32px>🏬 "+name+"</b><br><span style=font-size:24px>📍 "+sh["area"]+" - "+str(tot)+" Types - "+str(stock_tot)+" Pairs Available</span><a href='/shop/"+sh["own"]+"' class='btn btn-o'>Enter Shop - "+str(stock_tot)+" Pairs</a><a href='/share/"+sh["own"]+"' class='btn' style='background:#0a8a0a'>📱 Share Shop</a><div style=display:flex;gap:8px;margin-top:10px><a href='https://wa.me/?text="+enc+"' target=_blank class='btn' style='flex:1;background:#25D366;font-size:20px'>WhatsApp</a><a href='/chat/"+sh["own"]+"' class='btn btn-b' style='flex:1;font-size:20px'>💬 Chat</a><a href='https://www.google.com/maps?q="+str(sh["lat"])+","+str(sh["lng"])+"' target=_blank class='btn btn-w' style='flex:1;font-size:20px'>GPS</a></div></div>"
 for p in prods:
  # only show if shop sub active
  if p["shop"] in shops:
   if not shops[p["shop"]].get("sub",True):
    continue
  h+="<div class=card><img src='"+p["img"]+"' style='width:100%;height:260px;object-fit:cover;border-radius:18px'><br><b style=font-size:30px>"+p["name"]+"</b><br><span style=color:#f68b1e;font-weight:bold;font-size:32px>KSh "+str(p["price"])+"</span><br><span style=font-size:22px>"+p["shop"]+" - Stock "+str(p["stock"])+" Pairs</span><a href='/add/"+str(p["id"])+"' class='btn btn-o'>🛒 Add to Cart</a></div>"
 h+="<div class=card><b style=font-size:30px>📍 Shops on Map</b><div id='map'></div></div><link rel=stylesheet href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'><script src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'></script><script>var m=L.map('map').setView([-1.3956,36.7562],12);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(m);"
 for n in shops:
  if not shops[n].get("sub",True):
   continue
  sh=shops[n]
  h+="L.marker(["+str(sh["lat"])+","+str(sh["lng"])+"]).addTo(m).bindPopup('"+n+"');"
 h+="</script>"+nav()
 return h

@app.route("/map")
def mp():
 return home()

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
 msg="🔥 "+sn+" - "+sh["area"]+" - "+str(stock_tot)+" pairs available on EAZYMADE MARKET! Visit now!"
 enc=urllib.parse.quote(msg)
 h="<style>"+s+"</style><div class=top><b style=color:white>Share - "+sn+"</b></div>"
 h+="<div class=card style='background:linear-gradient(135deg,#25D366,#128C7E);color:white;border-left:none;text-align:center'><b style=font-size:32px>✅ Shop Ready!</b><p style=font-size:24px>"+str(tot)+" Types - "+str(stock_tot)+" Pairs - Share to get customers</p></div>"
 h+="<div class=card><b>Share Your Shop</b><div style=background:#f0f2f5;padding:18px;border-radius:14px;font-size:22px;margin-top:12px>"+msg+"</div>"
 h+="<a href='https://wa.me/?text="+enc+"' target=_blank class='btn' style='background:#25D366;font-size:28px;margin-top:14px'>📱 Share to WhatsApp</a>"
 h+="<a href='https://www.facebook.com/sharer/sharer.php?u=https://eazymade-market.com' target=_blank class='btn' style='background:#1877F2;font-size:28px;margin-top:10px'>📘 Share to Facebook</a>"
 h+="<a href='https://www.tiktok.com/upload' target=_blank class='btn' style='background:#000;font-size:28px;margin-top:10px'>🎵 Share to TikTok</a></div>"
 h+="<div class=card><a href='/' class='btn btn-o'>Continue to Market</a></div>"+nav()
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
 cart_ids=session.get("cart",[])
 subtotal=0
 items=[]
 for pid in cart_ids:
  for p in prods:
   if p["id"]==pid:
    subtotal+=int(p["price"])
    items.append(p)
 sale_cut=int(subtotal*SALE_CUT)
 delivery_office=int(DELIVERY*DELIVERY_CUT)
 delivery_shop=DELIVERY-delivery_office
 total=subtotal+DELIVERY
 h="<style>"+s+"</style><div class=top><b style=color:white;font-size:32px>🛒 Your Cart</b></div>"
 if not items:
  h+="<div class=card><b>Cart is empty</b><br><a href='/' class='btn btn-o'>Browse Shops</a></div>"
 for p in items:
  h+="<div class=card><b>"+p["name"]+"</b><br>KSh "+str(p["price"])+" - "+p["shop"]+"</div>"
 h+="<div class=card style=background:#111;color:white><b style=font-size:30px>Order Summary</b><br><br>"
 h+="<div style=display:flex;justify-content:space-between;font-size:24px><span>Shoes Subtotal:</span><span>KSh "+
