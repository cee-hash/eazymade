from flask import Flask,request,redirect,session
import os,base64,urllib.parse
from datetime import datetime,timedelta
app=Flask(__name__)
app.secret_key="v60finalnomorefail"
shops={}
prods=[]
chats={}
DELIVERY=300
SUB_FEE=500
OFFICE_PASS="EazyOffice2026!"

def auto_samples(sn):
    a=[["Jordan 1","5500","12"],["Air Force","4800","15"],["Yeezy","5200","8"]]
    for x in a:
        prods.append({"id":len(prods)+1,"name":x[0],"price":x[1],"img":"https://via.placeholder.com/400","shop":sn,"stock":x[2]})

def is_active(sh):
    if sh is None:
        return False
    if sh.get("sub") is True:
        return True
    try:
        e=sh.get("trial_end")
        if e is not None:
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
        if e is not None:
            if isinstance(e,str):
                e=datetime.fromisoformat(e)
            d=e-datetime.now()
            if d.days>=0:
                return d.days+1
    except:
        pass
    return 0

def base_html(body,show_nav=True):
    s="<style>body{margin:0;background:#f0f2f5;padding-bottom:140px;font-family:Arial;font-size:20px}.top{background:#f68b1e;padding:16px;color:white}.card{background:white;margin:12px;padding:14px;border-radius:14px;border-left:6px solid #f68b1e}.btn{display:block;padding:12px;background:#f68b1e;color:white;text-align:center;margin-top:8px;text-decoration:none;font-weight:bold;border-radius:10px}.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:12px 0;border-top:3px solid #f68b1e}.nav{color:#222;text-decoration:none;font-weight:bold}.foot{text-align:center;padding:20px;color:#666;font-size:12px;background:white;margin-top:20px}</style>"
    nav=""
    if show_nav is True:
        c=session.get("cart",[])
        t=str(len(c)) if len(c)>0 else ""
        nav="<div class=bottom><a href=/ class=nav>Market</a><a href=/register class=nav>Reg</a><a href=/post class=nav>Post</a><a href=/cart class=nav>Cart "+t+"</a></div>"
    foot="<div class=foot>© 2026 EazyMade Market - All Rights Reserved<br>Rongai | Kitengela | Kware<br>Phone 0116782556<br>Office Private via /office</div>"
    return s+body+foot+nav

@app.errorhandler(404)
def nf(e):
    return redirect("/")

@app.route("/")
def home():
    body="<div class=top><b>EAZYMADE MARKET</b></div>"
    body+="<div class=card><b>Welcome</b><br>"+str(len(shops))+" Shops<br><a href=/register class=btn>Register 1 Week Free</a></div>"
    if len(shops)==0:
        body+="<div class=card><b>No shops yet</b></div>"
    for n in shops:
        sh=shops[n]
        if is_active(sh) is False:
            continue
        tot=0
        stk=0
        for p in prods:
            if p["shop"]==n:
                tot+=1
                stk+=int(p["stock"])
        enc=urllib.parse.quote("Shop "+n)
        sp="/shop/"+sh["own"]
        sr="/share/"+sh["own"]
        cp="/chat/"+sh["own"]
        body+="<div class=card><b>"+n+"</b><br>"+sh["area"]+"<br><a href="+sp+" class=btn>Enter</a><a href="+sr+" class=btn>Share</a><a href="+cp+" class=btn>Chat</a></div>"
    for p in prods:
        if p["shop"] in shops:
            if is_active(shops[p["shop"]]) is True:
                ap="/add/"+str(p["id"])
                body+="<div class=card><b>"+p["name"]+"</b><br>KSh "+p["price"]+"<br><a href="+ap+" class=btn>Add</a></div>"
    body+="<div class=card><b>Location</b><br>"
    for n in shops:
        if is_active(shops[n]) is True:
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
    for n in shops:
        if shops[n]["own"]==own:
            sn=n
    if sn=="":
        return redirect("/")
    dl=days_left(shops[sn])
    enc=urllib.parse.quote("Shop "+sn)
    body="<div class=top><b>Share "+sn+"</b></div>"
    body+="<div class=card><b>"+str(dl)+" Days Free</b></div>"
    body+="<div class=card><a href=https://wa.me/?text="+enc+" target=_blank class=btn>WhatsApp</a></div>"
    body+="<div class=card><a href=/ class=btn>Market</a></div>"
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
    body="<div class=top><b>Cart</b></div>"
    if len(items)==0:
        body+="<div class=card><b>Empty</b></div>"
    for p in items:
        body+="<div class=card><b>"+p["name"]+"</b><br>KSh "+p["price"]+"</div>"
    body+="<div class=card><b>Total KSh "+str(tot)+"</b></div>"
    body+="<div class=card><a href=https://wa.me/254116782556?text=Order KSh "+str(tot)+" target=_blank class=btn>Order</a><a href=/ class=btn>Continue</a><a href=/clear class=btn>Clear</a></div>"
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
    if sn=="":
        return redirect("/")
    body="<div class=top><b>"+sn+"</b></div>"
    for p in prods:
        if p["shop"]==sn:
            ap="/add/"+str(p["id"])
            body+="<div class=card><b>"+p["name"]+"</b><br>KSh "+p["price"]+"<br><a href="+ap+" class=btn>Add</a></div>"
    sr="/share/"+own
    cp="/chat/"+own
    body+="<div class=card><a href="+sr+" class=btn>Share</a><a href="+cp+" class=btn>Chat</a></div>"
    return base_html(body)

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        sname=request.form.get("shop","").strip()
        user=request.form.get("user","").strip().lower()
        area=request.form.get("area","").strip()
        till=request.form.get("till","").strip()
        if sname!="" and user!="":
            if sname not in shops:
                now=datetime.now()
                tend=now+timedelta(days=7)
                shops[sname]={"own":user,"lat":-1.3956,"lng":36.7562,"area":area,"till":till,"sub":False,"sub_start":now.isoformat(),"trial_end":tend.isoformat()}
                chats[sname]=[]
                auto_samples(sname)
            return redirect("/share/"+user)
    body="<div class=top><b>Register - © EazyMade</b></div><div class=card><b>Register Free</b><form method=post><input name=user placeholder=Username required style=width:100%;padding:10px><input name=shop placeholder=Shop name required style=width:100%;padding:10px><input name=area placeholder=Area required style=width:100%;padding:10px><input name=till placeholder=Phone style=width:100%;padding:10px><button class=btn style=border:none;width:100%>Register</button></form></div>"
    return base_html(body)

@app.route("/chat/<own>",methods=["GET","POST"])
def chat(own):
    sn=""
    for n in shops:
        if shops[n]["own"]==own:
            sn=n
    if sn=="":
        return redirect("/")
    if sn not in chats:
        chats[sn]=[]
    if request.method=="POST":
        m=request.form.get("msg","")
        if m!="":
            chats[sn].append(m)
    sp="/shop/"+own
    body="<div class=top><b>Chat "+sn+"</b></div><div class=card><form method=post style=display:flex><input name=msg placeholder=Message required style=flex:1;padding:10px><button style=padding:10px;background:#f68b1e;color:white;border:none>Send</button></form></div><div class=card><b>Messages</b><br>"
    if len(chats[sn])==0:
        body+="No messages<br>"
    for mm in chats[sn][-20:]:
        body+=mm+"<br><hr>"
    body+="</div><div class=card><a href="+sp+" class=btn>Back</a></div>"
    return base_html(body)

@app.route("/subscribe/<own>")
def subscribe(own):
    sn=""
    for n in shops:
        if shops[n]["own"]==own:
            sn=n
    if sn=="":
        return redirect("/")
    shops[sn]["sub"]=True
    shops[sn]["sub_start"]=datetime.now().isoformat()
    body="<div class=card><b>Activated 30 days</b><br>"+sn+"</div><div class=card><a href=/ class=btn>Market</a></div>"
    return base_html(body,show_nav=False)

@app.route("/office",methods=["GET","POST"])
def office():
    if request.method=="POST":
        pw=request.form.get("password","")
        if pw==OFFICE_PASS:
            session["off"]=True
    if session.get("off") is not True:
        body="<div class=top><b>Office Private</b></div><div class=card><b>Only Owner</b><form method=post><input name=password type=password placeholder=Password required style=width:100%;padding:10px><button class=btn style=border:none;width:100%>Enter</button></form></div>"
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
        if is_active(shops[n]) is True:
            act+=1
            if shops[n].get("sub") is True:
                sub+=SUB_FEE
            else:
                tri+=1
        else:
            exp+=1
    body="<div class=top><b>Office Private © 2026</b></div><div class=card style=background:#111;color:white><b>Business</b><br>Shops: "+str(len(shops))+" Active: "+str(act)+" Trial: "+str(tri)+" Exp: "+str(exp)+"<br>Products: "+str(len(prods))+"<br>5 percent KSh "+str(osale)+"<br>Delivery KSh "+str(odel)+"<br>Sub Hidden KSh "+str(sub)+"<br><b>Total KSh "+str(osale+odel+sub)+"</b></div>"
    for n in shops:
        sh=shops[n]
        dl=days_left(sh)
        if sh.get("sub") is True:
            st="Paid"
        elif is_active(sh) is True:
            st="Trial "+str(dl)+" days"
        else:
            st="Expired Need 500"
        sp="/subscribe/"+sh["own"]
        cp="/chat/"+sh["own"]
        body+="<div class=card><b>"+n+"</b><br>Owner: "+sh["own"]+"<br>Status: "+st+"<br><a href="+sp+" class=btn>Activate 500</a><a href="+cp+" class=btn>Chats</a></div>"
    body+="<div class=card><a href=/ class=btn>Market</a><a href=/office/logout class=btn>Logout</a></div>"
    return base_html(body,show_nav=False)

@app.route("/office/logout")
def office_logout():
    session.pop("off",None)
    return redirect("/")

@app.route("/post",methods=["GET","POST"])
def post():
    if request.method=="POST":
        bulk=request.form.get("bulk","").strip()
        if bulk!="":
            sn=request.form.get("shop_select","")
            if sn=="" and len(shops)>0:
                sn=list(shops.keys())[0]
            for line in bulk.split("\n"):
                if line.strip()=="":
                    continue
                parts=line.strip().split()
                if len(parts)>=3:
                    nm=" ".join(parts[:-2])
                    pr=parts[-2]
                    st=parts[-1]
                    prods.append({"id":len(prods)+1,"name":nm,"price":pr,"img":"https://via.placeholder.com/400","shop":sn,"stock":st})
            return redirect("/")
        f=request.files.get("pic")
        img="https://via.placeholder.com/400"
        if f is not None and f.filename!="":
            img="data:image/jpeg;base64,"+base64.b64encode(f.read()).decode()
        sn=request.form.get("shop_select","")
        if sn=="" and len(shops)>0:
            sn=list(shops.keys())[0]
        prods.append({"id":len(prods)+1,"name":request.form["name"],"price":request.form["price"],"img":img,"shop":sn,"stock":request.form["stock"]})
        return redirect("/")
    if len(shops)==0:
        return base_html("<div class=card><b>No shops</b><br><a href=/register class=btn>Register</a></div>")
    opts=""
    for n in shops:
        opts+="<option value="+n+">"+n+"</option>"
    body="<div class=top><b>Post</b></div><div class=card><b>Bulk</b><form method=post><select name=shop_select>"+opts+"</select><textarea name=bulk placeholder=Name Price Stock></textarea><button class=btn>Post Many</button></form></div><div class=card><form method=post enctype=multipart/form-data><select name=shop_select>"+opts+"</select><input name=name placeholder=Name required><input name=price placeholder=Price required><input name=stock placeholder=Stock required><input type=file name=pic accept=image/*><button class=btn>Post</button></form></div>"
    return base_html(body)

if True:
    app.run(host='0.0.0.0',port=10000)
