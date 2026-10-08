from flask import Flask,request,redirect,session
import os,base64,urllib.parse
from datetime import datetime,timedelta
app=Flask(__name__)
app.secret_key="v57finalgreen5times"
shops={}
prods=[]
chats={}
DELIVERY=300
SUB_FEE=500
OFFICE_PASS="EazyOffice2026!"

def auto_samples(sn):
    a=[["Jordan 1","5500","12"],["Air Force","4800","15"],["Yeezy","5200","8"],["Jordan 4","6000","10"],["Nike Dunk","4700","20"]]
    for nm,pr,st in a:
        prods.append({"id":len(prods)+1,"name":nm,"price":pr,"img":"https://via.placeholder.com/400","shop":sn,"stock":st})

def is_active(sh):
    if sh==None:
        return False
    if sh.get("sub")==True:
        return True
    try:
        e=sh.get("trial_end")
        if e!=None:
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
        if e!=None:
            if isinstance(e,str):
                e=datetime.fromisoformat(e)
            d=e-datetime.now()
            if d.days>=0:
                return d.days+1
    except:
        pass
    return 0

def base_html(body,show_nav=True):
    s="<style>body{margin:0;background:#f0f2f5;padding-bottom:140px;font-family:Arial;font-size:22px}.top{background:#f68b1e;padding:16px;color:white}.card{background:white;margin:12px;padding:16px;border-radius:16px;border-left:6px solid #f68b1e}.btn{display:block;padding:14px;background:#f68b1e;color:white;text-align:center;margin-top:8px;text-decoration:none;font-weight:bold;border-radius:10px}.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:12px 0;border-top:3px solid #f68b1e}.nav{color:#222;text-decoration:none;font-weight:bold}.foot{text-align:center;padding:20px;color:#666;font-size:14px;background:white;margin-top:20px}</style>"
    nav=""
    if show_nav==True:
        cart=session.get("cart",[])
        t=""
        if len(cart)>0:
            t=str(len(cart))
        nav="<div class=bottom><a href=/ class=nav>Market</a><a href=/register class=nav>Reg</a><a href=/post class=nav>Post</a><a href=/cart class=nav>Cart "+t+"</a></div>"
    foot="<div class=foot>© 2026 EazyMade Market - All Rights Reserved<br>Langata Rongai | Kitengela | Kware<br>Phone 0116782556 | Till 0116782556<br>Office Private Only Owner via /office</div>"
    return s+body+foot+nav

@app.errorhandler(404)
def nf(e):
    return redirect("/")

@app.route("/")
def home():
    body="<div class=top><b>EAZYMADE MARKET</b><br>Rongai Kitengela Kware</div>"
    body+="<div class=card><b>Welcome</b><br>"+str(len(shops))+" Shops - "+str(len(prods))+" Shoes<br><a href=/register class=btn>Register 1 Week Free</a></div>"
    if len(shops)==0:
        body+="<div class=card><b>No shops yet</b><br><a href=/register class=btn>Register Now</a></div>"
    for name in list(shops.keys()):
        sh=shops[name]
        if is_active(sh)==False:
            continue
        tot=0
        stk=0
        for p in prods:
            if p["shop"]==name:
                tot+=1
                stk+=int(p["stock"])
        enc=urllib.parse.quote("Shop "+name)
        sp="/shop/"+sh["own"]
        sr="/share/"+sh["own"]
        cp="/chat/"+sh["own"]
        body+="<div class=card><b>"+name+"</b><br>"+sh["area"]+" - "+str(tot)+" Types - "+str(stk)+" Pairs<br><a href="+sp+" class=btn>Enter Shop</a><a href="+sr+" class=btn>Share</a><a href=https://wa.me/?text="+enc+" target=_blank class=btn>WhatsApp</a><a href="+cp+" class=btn>Chat</a></div>"
    for p in prods:
        if p["shop"] in shops and is_active(shops[p["shop"]])==True:
            ap="/add/"+str(p["id"])
            body+="<div class=card><img src="+p["img"]+" style=width:100%><br><b>"+p["name"]+"</b><br>KSh "+p["price"]+"<br><a href="+ap+" class=btn>Add to Cart</a></div>"
    body+="<div class=card><b>Shops Location</b><br>"
    for n in list(shops.keys()):
        if is_active(shops[n])==True:
            sh=shops[n]
            body+=n+" - "+sh["area"]+"<br>"
    body+="</div>"
    return base_html(body)

@app.route("/map")
def mp():
    return home()

@app.route("/share/<own>")
def share(own):
    sn=""
    for n in list(shops.keys()):
        if shops[n]["own"]==own:
            sn=n
    if sn=="":
        return redirect("/")
    dl=days_left(shops[sn])
    msg="Shop "+sn+" on EAZYMADE © 2026"
    enc=urllib.parse.quote(msg)
    body="<div class=top><b>Share "+sn+"</b></div>"
    body+="<div class=card><b>Ready - "+str(dl)+" Days Free</b></div>"
    body+="<div class=card><a href=https://wa.me/?text="+enc+" target=_blank class=btn>WhatsApp</a><a href=https://www.facebook.com/sharer/sharer.php target=_blank class=btn>Facebook</a><a href=https://www.tiktok.com/upload target=_blank class=btn>TikTok</a></div>"
    body+="<div class=card><a href=/ class=btn>Market</a></div>"
    return base_html(body)

@app.route("/add/<int:pid>")
def add(pid):
    c=session.get("cart",[])
    c.append(pid)
    session["cart"]=c
    return redirect("/cart")

@app.route("/
