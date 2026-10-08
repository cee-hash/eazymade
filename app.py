from flask import Flask,request,redirect,session
import os,base64,urllib.parse
from datetime import datetime,timedelta
app=Flask(__name__)
app.secret_key="v45finalclean"

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
 return "body{margin:0;background:#f0f2f5;padding-bottom:140px;font-family:Arial;font-size:28px}.top{background:#f68b1e;padding:18px;position:sticky;top:0;z-index:100}.card{background:white;border-radius:18px;padding:22px;margin:14px;border-left:8px solid #f68b1e}.btn{display:block;padding:20px;border-radius:14px;width:100%;text-align:center;text-decoration:none;font-weight:bold;font-size:24px;margin-top:12px;color:white}.btn-o{background:#f68b1e}.btn-b{background:#111}.btn-w{background:white;color:#f68b1e;border:2px solid #f68b1e}.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:14px 0;border-top:4px solid #f68b1e;z-index:999}.nav{text-align:center;text-decoration:none;color:#222;font-size:18px;font-weight:bold}#map{height:60vh;width:100%}.chat-msg{background:#f0f2f5;padding:14px;border-radius:12px;margin:8px 0;font-size:24px;border-left:5px solid #f68b1e}"

def nav():
 cart=session.get("cart",[])
 txt=""
 if cart:
  txt=str(len(cart))
 return "<div class=bottom><a href='/' class=nav>Market</a><a href='/register' class=nav>Register</a><a href='/post' class=nav>Post</a><a href='/cart' class=nav>Cart "+txt+"</a><a href='/office' class=nav>Office</a></div>"

@app.errorhandler(404)
def nf(e):
 return redirect("/")

@app.route("/")
def home():
 s=css()
 h="<style>"+s+"</style>"
 h+="<div class=top><b style=color:white>EAZYMADE MARKET</b></div>"
 h+="<div class=card style='background:linear-gradient(135deg,#f68b1e,#000);color:white;border-left:none;text-align:center'><b>Welcome</b><p>"+str(len(shops))+" Shops - "+str(len(prods))+" Shoes</p><a href='/register' class='btn' style='background:#0a8a0a'>Register - 1 Week Free</a><a href='/map' class='btn' style='background:white;color:#f68b1e'>View Map</a></div>"
 if not shops:
  h+="<div class=card><b>No shops yet</b><br>Be first - 1 week free<br><a href='/register' class='btn btn-o'>Register Now</a></div>"
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
  if dl>0 and not sh.get("sub"):
   trial_txt=" - "+str(dl)+" days free left"
  msg="Shop "+name+" "+str(stock_tot)+" pairs"
  enc=urllib.parse.quote(msg)
  h+="<div class=card><b>"+name+"</b><br>"+sh["area"]+" - "+str(tot)+" Types - "+str(stock_tot)+" Pairs"+trial_txt+"<br><a href='/shop/"+sh["own"]+"' class='btn btn-o'>Enter Shop</a><a
