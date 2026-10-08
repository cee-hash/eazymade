from flask import Flask,request,redirect,session
import os,base64,urllib.parse
from datetime import datetime,timedelta
app=Flask(__name__)
app.secret_key="v44safe"

shops={}
prods=[]
chats={}

DELIVERY=300
SUB_FEE=500

def auto_samples(shop_name):
 samples=[
  ["Jordan 1 Retro","5500","12"],
  ["Air Force 1","4800","15"],
  ["Yeezy Boost","5200","8"],
  ["Jordan 4","6000","10"],
  ["Nike Dunk","4700","20"],
 ]
 for nm,pr,st in samples:
  prods.append({"id":len(prods)+1,"name":nm,"price":pr,"img":"https://via.placeholder.com/400","shop":shop_name,"stock":st})

def is_active(sh):
 if not sh:
  return False
 if sh.get("sub"):
  return True
 try:
  end=sh.get("trial_end")
  if end:
   if isinstance(end,str):
    end=datetime.fromisoformat(end)
   if datetime.now()<=end:
    return True
 except:
  return True
 return False

def days_left(sh):
 try:
  end=sh.get("trial_end")
  if end:
   if isinstance(end,str):
    end=datetime.fromisoformat(end)
   d=end-datetime.now()
   if d.days>=0:
    return d.days+1
 except:
  pass
 return 0

def css():
 return "body{margin:0;background:#f0f2f5;padding-bottom:140px;font-family:Arial;font-size:28px}.top{background:#f68b1e;padding:18px;position:sticky;top:0;z-index:100}.card{background:white;border-radius:18px;padding:22px;margin:14px;box-shadow:0 4px 12px #0001;border-left:8px solid #f68b1e}.btn{display:block;padding:20px;border-radius:14px;width:100%;text-align:center;text-decoration:none;font-weight:bold;font-size:24px;margin-top:12px;color:white!important}.btn-o{background:#f68b1e}.btn-b{background:#111}.btn-w{background:white;color:#f68b1e!important;border:2px solid #f68b1e}.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:14px 0;border-top:4px solid #f68b1e;z-index:999}.nav{text-align:center;text-decoration:none;color:#222;font-size:18px;font-weight:bold}#map{height:60vh;width:100%;border-radius:16px}.chat-msg{background:#f0f2f5;padding:14px;border-radius:12px;margin:8px 0;font-size:24px;border-left:5px solid #f68b1e}"

def nav():
 cart=session.get("cart",[])
 txt=""
 if cart:
  txt=str(len(cart))
 return "<div class=bottom><a href='/' class='nav'>Market</a><a href='/register' class='nav'>Register</a><a href='/post' class='nav'>Post</a><a href='/cart' class='nav'>Cart "+txt+"</a><a href='/office' class='nav'>Office</a></div>"

@app.errorhandler(404)
def nf(e):
 return redirect("/")

@app.route("/")
def home():
 s=css()
 h="<style>"+s+"</style>"
 h+="<div class=top><b style=color:white>EAZYMADE MARKET</b><div style=color:white;font-size:18px>Shops Near You</div></div>"
 h+="<div class='card' style='background:linear-gradient(135deg,#f68b1e,#000);color:white;border-left:none;text-align:center'><b>Welcome</b><p style=font-size:22px>"+str(len(shops))+" Shops - "+str(len(prods))+" Shoes</p><a href='/register' class='btn' style='background:#0a8a0a'>Register - 1 Week Free</a><a href='/map' class='btn' style='background:white;color:#f68b1e!important'>View Map</a></div>"
 if not shops:
  h+="<div class=card><b>No shops yet</b><br>Be first - 1 week free trial<br><a href='/register' class='btn btn-o'>Register Now</a></div>"
 for name in shops:
  sh=shops[name]
  if not is_active(sh):
   continue
  tot=0
  stock_tot=0
  for p in prods:
   if p["shop"]==name:
    tot+=1
    stock_tot+=int(p["stock"])
  dl=days_left(sh)
  trial_txt=""
  if dl>0:
   if not sh.get("sub"):
    trial_txt=" - "+str(dl)+" days free left"
  msg="Shop "+name+" "+str(stock_tot)+" pairs"
  enc=urllib.parse.quote(msg)
  h+="<div class=card><b>"+name+"</b><br>"+sh["area"]+" - "+str(tot)+" Types - "+str(stock_tot)+" Pairs"+trial_txt+"<br><a href='/shop/"+sh["own"]+"' class='btn btn-o'>Enter Shop</a><a href='/share/"+sh["own"]+"' class='btn' style='background:#0a8a0a'>Share Shop</a><div style=display:flex;gap:6px;margin-top:8px><a href='https://wa.me/?text="+enc+"' target=_blank class='btn' style='flex:1;background:#25D366;font-size:18px'>WhatsApp</a><a href='/chat/"+sh["own"]+"' class='btn btn-b' style='flex:1;font-size:18px'>Chat</a><a href='https://www.google.com/maps?q="+str(sh["lat"])+","+str(sh["lng"])+"' target=_blank class='btn btn-w' style='flex:1;font-size:18px'>GPS</a></div></div>"
 for p in prods:
  if p["shop"] not in shops:
   continue
  if not is_active(shops[p["shop"]]):
   continue
  h+="<div class=card><img src='"+p["img"]+"' style='width:100%;height:240px;object-fit:cover;border-radius:14px'><br><b>"+p["name"]+"</b><br><span style=color:#f68b1e;font-weight:bold>KSh "+str(p["price"])+"</span><br>"+p["shop"]+" Stock "+str(p["stock"])+"<br><a href='/add/"+str(p["id"])+"' class='btn btn-o'>Add to Cart</a></div>"
 h+="<div class=card><b>Shops on Map</b><div id='map'></div></div><link rel=stylesheet href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'><script src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'></script><script>var m=L.map('map').setView([-1.3956,36.7562],12);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(m);"
 for n in shops:
  if not is_active(shops[n]):
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
 dl=days_left(sh)
 msg="Shop "+sn+" "+str(stock_tot)+" pairs on EAZYMADE free trial "+str(dl)+" days"
 enc=urllib.parse.quote(msg)
 h="<style>"+s+"</style><div class=top><b style=color:white>Share - "+sn+"</b></div>"
 h+="<div class='card' style='background:#25D366;color:white;border-left:none;text-align:center'><b>Shop Ready - "+str(dl)+" Days Free</b><p>"+str(tot)+" Types - "+str(stock_tot)+" Pairs</p></div>"
 h+="<div class=card><b>Share Your Shop</b><div style=background:#f0f2f5;padding:14px;border-radius:12px;font-size:20px;margin-top:10px>"+msg+"</div>"
 h+="<a href='https://wa.me/?text="+enc+"' target=_blank
