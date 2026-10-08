from flask import Flask,request,redirect,session
import os,base64,urllib.parse
from datetime import datetime,timedelta
app=Flask(__name__)
app.secret_key="v54copyright"
shops={}
prods=[]
chats={}
DELIVERY=300
SUB_FEE=500
OFFICE_PASS="EazyOffice2026!"

def auto_samples(shop_name):
    a=[["Jordan 1","5500","12"],["Air Force","4800","15"],["Yeezy","5200","8"],["Jordan 4","6000","10"],["Nike Dunk","4700","20"]]
    for nm,pr,st in a:
        prods.append({"id":len(prods)+1,"name":nm,"price":pr,"img":"https://via.placeholder.com/400","shop":shop_name,"stock":st})

def is_active(sh):
    if not sh:
        return False
    if sh.get("sub"):
        return True
    try:
        e=sh.get("trial_end")
        if e:
            if isinstance(e,str):
                e=datetime.fromisoformat(e)
            if datetime.now()<=e:
                return True
    except:
        return True
    return False

def days_left(sh):
    try:
        e=sh.get("trial_end")
        if e:
            if isinstance(e,str):
                e=datetime.fromisoformat(e)
            d=e-datetime.now()
            if d.days>=0:
                return d.days+1
    except:
        pass
    return 0

def base_html(body,show_nav=True):
    style="<style>body{margin:0;background:#f0f2f5;padding-bottom:140px;font-family:Arial;font-size:22px}.top{background:#f68b1e;padding:16px;color:white}.card{background:white;margin:12px;padding:16px;border-radius:16px;border-left:6px solid #f68b1e}.btn{display:block;padding:14px;background:#f68b1e;color:white;text-align:center;margin-top:8px;text-decoration:none;font-weight:bold;border-radius:10px}.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:12px 0;border-top:3px solid #f68b1e}.nav{color:#222;text-decoration:none;font-weight:bold}.foot{text-align:center;padding:30px 10px;color:#666;font-size:14px;background:white;margin-top:20px;border-top:2px solid #f68b1e}</style>"
    nav=""
    if show_nav:
        cart=session.get("cart",[])
        t=""
        if cart:
            t=str(len(cart))
        nav="<div class=bottom><a href=/ class=nav>Market</a><a href=/register class=nav>Reg</a><a href=/post class=nav>Post</a><a href=/cart class=nav>Cart "+t+"</a></div>"
    foot="<div class=foot>© 2026 EazyMade Market - All Rights Reserved<br>Langata Rongai | Kitengela | Kware | Nairobi<br>Owner: EazyMade | Phone: 0116782556 | Till: 0116782556<br>Office Private - Only Owner Access via /office<br>Designed and Built by EazyMade Team</div>"
    return style+body+foot+nav

@app.errorhandler(404)
def nf(e):
    return redirect("/")

@app.route("/")
def home():
    body="<div class=top><b>EAZYMADE MARKET</b><br>Rongai Kitengela Kware</div>"
    body+="<div class=card><b>Welcome to EazyMade</b><br>"+str(len(shops))+" Shops - "+str(len(prods))+" Shoes<br><a href=/register class=btn>Register Your Shop - 1 Week Free</a></div>"
    if not shops:
        body+="<div class=card><b>No shops yet - Be first to register</b><br><a href=/register class=btn>Register Now - Free Trial</a></div>"
    for name in shops:
        sh=shops[name]
        if not is_active(sh):
            continue
        tot=0
        stk=0
        for p in prods:
            if p["shop"]==name:
                tot+=1
                stk+=int(p["stock"])
        enc=urllib.parse.quote("Shop "+name+" on EAZYMADE MARKET")
        sp="/shop/"+sh["own"]
        sr="/share/"+sh["own"]
        cp="/chat/"+sh["own"]
        body+="<div class=card><b>"+name+"</b><br>"+sh["area"]+" - "+str(tot)+" Types - "+str(stk)+" Pairs<br><a href="+sp+" class=btn>Enter Shop - "+str(stk)+" Pairs</a><a href="+sr+" class=btn>Share Shop</a><a href=https://wa.me/?text="+enc+" target=_blank class=btn>WhatsApp</a><a href="+cp+" class=btn>Chat with Owner</a></div>"
    for p in prods:
        if p["shop"] not in shops:
            continue
        if not is_active(shops[p["shop"]]):
            continue
        ap="/add/"+str(p["id"])
        body+="<div class=card><img src="+p["img"]+" style=width:100%;height:200px;object-fit:cover;border-radius:12px><br><b>"+p["name"]+"</b><br>KSh "+p["price"]+" - Stock "+p["stock"]+"<br><a href="+ap+" class=btn>Add to Cart</a></div>"
    body+="<div class=card><b>Shops Location - Rongai Area</b><br>"
    for n in shops:
        if not is_active(shops[n]):
            continue
        sh=shops[n]
        body+=n+" - "+sh["area"]+"<br>Lat "+str(sh["lat"])+" Lng "+str(sh["lng"])+"<br><br>"
    body+="</div>"
    return base_html(body)

@app.route("/map")
def mp():
    return home()

@app.route("/share/<own>")
def share(own):
    sn=""
    for n in shops:
        if shops[n]["own"]==own:
            sn=n
    if not
