from flask import Flask,request,redirect,session
import os,base64,urllib.parse
from datetime import datetime,timedelta

app=Flask(__name__)
app.secret_key="v50keepallfinal"

shops={}
prods=[]
chats={}
DELIVERY=300
SUB_FEE=500
OFFICE_PASS="EazyOffice2026!"

def auto_samples(shop_name):
    a=[["Jordan 1 High","5500","12"],["Air Force 1","4800","15"],["Yeezy 350","5200","8"],["Jordan 4","6000","10"],["Nike Dunk","4700","20"]]
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
    c1="body{margin:0;background:#f0f2f5}"
    c2=".top{background:#f68b1e;padding:16px}"
    c3=".card{background:white;margin:12px}"
    c4=".card{padding:20px;border-radius:16px}"
    c5=".card{border-left:6px solid #f68b1e}"
    c6=".btn{display:block;padding:18px}"
    c7=".btn{border-radius:12px;text-align:center}"
    c8=".btn{color:white;background:#f68b1e}"
    c9=".bottom{position:fixed;bottom:0;left:0;right:0}"
    c10=".bottom{background:white;display:flex}"
    c11=".nav{color:#222;font-size:16px}"
    style="<style>"+c1+c2+c3+c4+c5+c6+c7+c8+c9+c10+c11+"</style>"
    nav=""
    if show_nav:
        cart=session.get("cart",[])
        t=""
        if cart:
            t=str(len(cart))
        nav="<div class='bottom'>"
        nav+="<a href='/' class='nav'>Market</a>"
        nav+="<a href='/register' class='nav'>Reg</a>"
        nav+="<a href='/post' class='nav'>Post</a>"
        nav+="<a href='/cart' class='nav'>Cart "+t+"</a>"
        nav+="</div>"
    return style+body+nav

@app.errorhandler(404)
def nf(e):
    return redirect("/")

@app.route("/")
def home():
    body="<div class='top'><b>EAZYMADE MARKET</b></div>"
    body+="<div class='card'><b>Welcome</b><br>"+str(len(shops))+" Shops<br>"
    body+="<a href='/register' class='btn'>Register 1 Week Free</a>"
    body+="<a href='/map' class='btn'>View Map</a></div>"
    if not shops:
        body+="<div class='card'><b>No shops yet</b></div>"
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
        enc=urllib.parse.quote("Shop "+name)
        body+="<div class='card'><b>"+name+"</b><br>"
        body+=sh["area"]+" - "+str(tot)+" Types - "+str(stk)+" Pairs<br>"
        body+="<a href='/shop/"+sh["own"]+"' class='btn'>Enter Shop</a>"
        body+="<a href='/share/"+sh["own"]+"' class='btn'>Share</a>"
        body+="<a href='https://wa.me/?text="+enc+"' target='_blank' class='btn'>WhatsApp</a>"
        body+="<a href='/chat/"+sh["own"]+"' class='btn'>Chat</a></div>"
    for p in prods:
        if p["shop"] not in shops:
            continue
        if not is_active(shops[p["shop"]]):
            continue
        body+="<div class='card'><img src='"+p["img"]+"' style='width:100%'>"
        body+="<br><b>"+p["name"]+"</b><br>KSh "+p["price"]+"<br>"
        body+="<a href='/add/"+str(p["id"])+"' class='btn'>Add to Cart</a></div>"
    body+="<div class='card'><b>Map</b><div id='map' style='height:50vh'></div></div>"
    body+="<link rel='stylesheet' href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'>"
    body+="<script src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'></script>"
    body+="<script>var m=L.map('map').setView([-1.3956,36.7562],12);"
    body+="L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(m);"
    for n in shops:
        if not is_active(shops[n]):
            continue
        sh=shops[n]
        body+="L.marker(["+str(sh["lat"])+","+str(sh["lng"])+"]).addTo(m).bindPopup('"+n+"');"
    body+="</script>"
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
    if not sn:
        return redirect("/")
    sh=shops[sn]
    tot=0
    stk=0
    for p in prods:
        if p["shop"]==sn:
            tot+=1
            stk+=int(p["stock"])
    dl=days_left(sh)
    msg="Shop "+sn+" "+str(stk)+" pairs"
    enc=urllib.parse.quote(msg)
    body="<div class='top'><b>Share "+sn+"</b></div>"
    body+="<div class='card'><b>Ready "+str(dl)+" Days Free</b></div>"
    body+="<div class='card'><a href='https://wa.me/?text="+enc+"' target='_blank' class='btn'>WhatsApp</a>"
    body+="<a href='https://www.facebook.com/sharer/sharer.php' target='_blank' class='btn'>Facebook</a>"
    body+="<a href='https://www.tiktok.com/upload' target='_blank' class='btn'>TikTok</a></div>"
    body+="<div class='card'><a href='/' class='btn'>Continue</a></div>"
    return base_html(body)

@app.route("/add/<int:pid>")
def add(pid):
    c=session.get("cart",[])
    c.append(pid)
    session["cart"]=c
    return redirect("/cart")

@app.route("/cart")
def cart():
    ids=session.get("cart",[])
    sub=0
    items=[]
    for pid in ids:
        for p in prods:
            if p["id"]==pid:
                sub+=int(p["price"])
                items.append(p)
    tot=sub+DELIVERY
    body="<div class='top'><b>Cart</b></div>"
    if not items:
        body+="<div class='card'><b>Cart empty</b></div>"
    for p in items:
        body+="<div class='card'><b>"+p["name"]+"</b><br>KSh "+p["price"]+"</div>"
    body+="<div class='card'><b>Subtotal KSh "+str(sub)+"</b><br>Delivery KSh "+str(DELIVERY)+"<br><b>Total KSh "+str(tot)+"</b></div>"
    body+="<div class='card'><a href='https://wa.me/254116782556?text=Order KSh "+str(tot)+"' target='_blank' class='btn'>Order WhatsApp</a>"
    body+="<a href='/' class='btn'>Continue</a><a href='/clear' class='btn'>Clear</a></div>"
    return base_html(body)

@app.route("/clear")
def clear():
    session["cart"]=[]
    return redirect("/")

@app.route("/shop/<own>")
def shop(own):
    sn=""
    for n in shops:
        if shops[n]["own"]==own:
            sn=n
    if not sn:
        return redirect("/")
    body="<div class='top'><b>"+sn+"</b></div>"
    for p in prods:
        if p["shop"]==sn:
            body+="<div class='card'><b>"+p["name"]+"</b><br>KSh "+p["price"]+"<br>"
            body+="<a href='/add/"+str(p["id"])+"' class='btn'>Add to Cart</a></div>"
    body+="<div class='card'><a href='/share/"+own+"' class='btn'>Share</a>"
    body+="<a href='/chat/"+own+"' class='btn'>Chat</a></div>"
    return base_html(body)

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        sname=request.form.get("shop","").strip()
        user=request.form.get("user","").strip().lower()
        area=request.form.get("area","").strip()
        till=request.form.get("till","").strip()
        if sname and user:
            if sname not in shops:
                now=datetime.now()
                tend=now+timedelta(days=7)
                shops[sname]={"own":user,"lat":-1.3956,"lng":36.7562,"area":area,"till":till,"sub":False,"sub_start":now.isoformat(),"trial_end":tend.isoformat()}
                chats[sname]=[]
                auto_samples(sname)
            return redirect("/share/"+user)
    body="<div class='top'><b>Register Shop</b></div>"
    body+="<div class='card'><b>Register Free</b><br>5 Shoes auto posted<br>Visible on market<br>"
    body+="<form method='post'><input name='user' placeholder='Username' required style='width:100%;padding:12px'>"
    body+="<input name='shop' placeholder='Shop name' required style='width:100%;padding:12px'>"
    body+="<input name='area' placeholder='Area' required style='width:100%;padding:12px'>"
    body+="<input name='till' placeholder='Phone' style='width:100%;padding:12px'>"
    body+="<button class='btn' style='border:none;width:100%'>Register</button></form></div>"
    return base_html(body)

@app.route("/chat/<own>",methods=["GET","POST"])
def chat(own):
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
    body="<div class='top'><b>Chat "+sn+"</b></div>"
    body+="<div class='card'><form method='post' style='display:flex'>"
    body+="<input name='msg' placeholder='Message' required style='flex:1;padding:12px'>"
    body+="<button style='padding:12px;background:#f68b1e;color:white;border:none'>Send</button></form></div>"
    body+="<div class='card'><b>Messages</b><br>"
    if not chats[sn]:
        body+="No messages<br>"
    for mm in chats[sn][-20:]:
        body+=mm+"<br><hr>"
    body+="</div><div class='card'><a href='/shop/"+own+"' class='btn'>Back</a></div>"
    return base_html(body)

@app.route("/subscribe/<own>")
def subscribe(own):
    sn=""
    for n in shops:
        if shops[n]["own"]==own:
            sn=n
    if not sn:
        return redirect("/")
    shops[sn]["sub"]=True
    shops[sn]["sub_start"]=datetime.now().isoformat()
    body="<div class='card'><b>Activated</b><br>"+sn+" 30 days</div>"
    body+="<div class='card'><a href='/' class='btn'>Market</a></div>"
    return base_html(body,show_nav=False)

@app.route("/office",methods=["GET","POST"])
def office():
    if request.method=="POST":
        pw=request.form.get("password","")
        if pw==OFFICE_PASS:
            session["off"]=True
    if not session.get("off"):
        body="<div class='top'><b>Office Private</b></div>"
        body+="<div class='card'><b>Only Owner</b><form method='post'>"
        body+="<input name='password' type='password' placeholder='Password' required style='width:100%;padding:12px'>"
        body+="<button class='btn' style='border:none;width:100%'>Enter</button></form></div>"
        return base_html(body,show_nav=False)
    ts=0
    for p in prods:
        ts+=int(p["price"])
    osale=int(ts*0.05)
    odel=int(len(prods)*DELIVERY*0.5)
    sub=0
    act=0
    tri=0
    exp=0
    for n in shops:
        if is_active(shops[n]):
            act+=1
            if shops[n].get("sub"):
                sub+=SUB_FEE
            else:
                tri+=1
        else:
            exp+=1
    body="<div class='top'><b>Office Private - Only You</b></div>"
    body+="<div class='card'><b>Business</b><br>Shops: "+str(len(shops))+" Active: "+str(act)+" Trial: "+str(tri)+" Exp: "+str(exp)+"<br>"
    body+="Products: "+str(len(prods))+"<br>Sales: KSh "+str(ts)+"<br>"
    body+="5 percent: KSh "+str(osale)+"<br>Delivery 50 percent: KSh "+str(odel)+"<br>"
    body+="Subscription: KSh "+str(sub)+"<br><b>Total: KSh "+str(osale+odel+sub)+"</b></div>"
    for n in shops:
        sh=shops[n]
        dl=days_left(sh)
        if sh.get("sub"):
            st="Paid"
        elif is_active(sh):
            st="Trial "+str(dl)+" days"
        else:
            st="Expired Need 500"
        body+="<div class='card'><b>"+n+"</b><br>Owner: "+sh["own"]+" Status: "+st+"<br>"
        body+="<a href='/subscribe/"+
