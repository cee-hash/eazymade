from flask import Flask,request,redirect,session
import os,base64,urllib.parse
from datetime import datetime,timedelta
app=Flask(__name__)
app.secret_key="v43fixtrialgreen"

shops={}
prods=[]
chats={}

DELIVERY=300
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
   delta=end-datetime.now()
   if delta.days>=0:
    return delta.days+1
 except:
  pass
 return 0

def css():
 return "body{margin:0;background:#f0f2f5;padding-bottom:140px;font-family:Arial;font-size:30px}.top{background:linear-gradient(90deg,#f68b1e,#ff9a3d);padding:20px;position:sticky;top:0;z-index:100}.card{background:white;border-radius:22px;padding:26px;margin:16px;box-shadow:0 6px 18px #0001;border-left:10px solid #f68b1e}.btn{display:block;padding:26px;border-radius:18px;width:100%;text-align:center;text-decoration:none!important;font-weight:bold;font-size:26px;margin-top:14px;color:white!important}.btn-o{background:linear-gradient(90deg,#f68b1e,#ff6a00)}.btn-b{background:#111}.btn-w{background:white;color:#f68b1e!important;border:3px solid #f68b1e}.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:16px 0;border-top:5px solid #f68b1e;z-index:999}.nav{text-align:center;text-decoration:none;color:#222;font-size:20px;font-weight:bold}#map{height:65vh;width:100%;border-radius:20px}.chat-msg{background:#f0f2f5;padding:18px;border-radius:16px;margin:10px 0;font-size:26px;border-left:6px solid #f68b1e}"

def nav():
 cart=session.get("cart",[])
 txt=""
 if cart:
  txt="("+str(len(cart))+")"
 return "<div class=bottom><a href='/' class='nav'>Market<br>🏪</a><a href='/register' class='nav'>Register<br>➕</a><a href='/post' class='nav'>Post<br>📸</a><a href='/cart' class='nav'>
