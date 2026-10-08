from flask import Flask,request,redirect,session
import os,base64,urllib.parse
from datetime import datetime,timedelta
app=Flask(__name__)
app.secret_key='v46ultra'

shops={}
prods=[]
chats={}

DELIVERY=300
SUB_FEE=500

def auto_samples(shop_name):
    for nm,pr,st in [["Jordan 1","5500","12"],["Air Force","4800","15"],["Yeezy","5200","8"]]:
        prods.append({"id":len(prods)+1,"name":nm,"price":pr,"img":"https://via.placeholder.com/400","shop":shop_name,"stock":st})

def is_active(sh):
    if not sh:
        return False
    if sh.get('sub'):
        return True
    try:
        end=sh.get('trial_end')
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
        end=sh.get('trial_end')
        if end:
            if isinstance(end,str):
                end=datetime.fromisoformat(end)
            d=end-datetime.now()
            if d.days>=0:
                return d.days+1
    except:
        pass
    return 0

def base_html(body):
    style='body{margin:0;background:#f0f2f5;padding-bottom:120px;font-family:Arial;font-size:26px}.top{background:#f68b1e;padding:16px}.card{background:white;border-radius:16px;padding:20px;margin:12px;border-left:6px solid #f68b1e}.btn{display:block;padding:18px;border-radius:12px;text-align:center;text-decoration:none;font-weight:bold;margin-top:10px;color:white;background:#f68b1e}.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:10px 0;border-top:3px solid #f68b1e}.nav{text-align:center;text-decoration:none;color:#222;font-size:16px}'
    nav_cart=session.get('cart',[])
    txt=''
    if nav_cart:
        txt=str(len(nav_cart))
    nav='<div class=bottom><a href=/ class=nav>Market</a><a href=/register class=nav>Register</a><a href=/post class=nav>Post</a><a href=/cart class=nav>Cart '+txt+'</a><a href=/office class=nav>Office</a></div>'
    return '<style>'+style+'</style>'+body+nav

@app.errorhandler(404)
def nf(e):
    return redirect('/')

@app.route('/')
def home():
    body='<div class=top><b>EAZYMADE MARKET</b></div>'
    body+='<div class=card><b>Welcome</b><br>'+str(len(shops))+' Shops<br><a href=/register class=btn>Register 1 Week Free</a><a href=/map class=btn style=background:white;color:#f68b1e;border:2px solid #f68b1e>View Map</a></div>'
    if not shops:
        body+='<div class=card><b>No shops yet</b><br><a href=/register class=btn>Register Now</a></div>'
    for name in shops:
        sh=shops[name]
        if not is_active(sh):
            continue
        tot=0
        stock=0
        for p in prods:
            if p['shop']==name:
                tot+=1
                stock+=int(p['stock'])
        dl=days_left(sh)
        tr=''
        if dl>0 and not sh.get('sub'):
            tr=' - '+str(dl)+' days free'
        enc=urllib.parse.quote('Shop '+name)
        body+='<div class=card><b>'+name+'</b><br>'+sh['area']+' - '+str(tot)+' Types - '+str(stock)+' Pairs'+tr+'<br><a href=/shop/'+sh['own']+' class=btn>Enter Shop</a><a href=/share/'+sh['own']+' class=btn style=background:#0a8a0a>Share</a><br><a href=https://wa.me/?text='+enc+' target=_blank class=btn style=background:#25D366>WhatsApp</a><a href=/chat/'+sh['own']+' class=btn style=background:#111>Chat</a></div>'
    for p in prods:
        if p['shop'] not in shops:
            continue
        if not is_active(shops[p['shop']]):
            continue
        body+='<div class=card><img src='+p['img']+' style=width:100%;height:200px><br><b>'+p['name']+'</b><br>KSh '+p['price']+'<br><a href=/add/'+str(p['id'])+' class=btn>Add to Cart</a></div>'
    body+='<div class=card><b>Map</b><div id=map style=height:50vh></div></div><link rel=stylesheet href=https://unpkg.com/leaflet@1.9.4/dist/leaflet.css><script src=https://unpkg.com/leaflet@1.9.4/dist/leaflet.js></script><script>var m=L.map("map").setView([-1.3956,36.7562],12);L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(m);'
    for n in shops:
        if not is_active(shops[n]):
            continue
        sh=shops[n]
        body+='L.marker(['+str(sh['lat'])+','+str(sh['lng'])+']).addTo(m).bindPopup("'+n+'");'
    body+='</script>'
    return base_html(body)

@app.route('/map')
def mp():
    return home()

@app.route('/share/<own>')
def share(own):
    sn=''
    for n in shops:
        if shops[n]['own']==own:
            sn=n
    if not sn:
        return redirect('/')
    sh=shops[sn]
    dl=days_left(sh)
    msg='Shop '+sn+' free trial '+str(dl)+' days'
    enc=urllib.parse.quote(msg)
    body='<div class=top><b>Share '+sn+'</b></div><div class=card><b>Shop Ready - '+str(dl)+' Days Free</b></div><div class=card><a href=https://wa.me/?text='+enc+' target=_blank class=btn style=background:#25D366>WhatsApp</a><a href=https://www.facebook.com/sharer/sharer.php?u=https://eazymade-market.com target=_blank class=btn style=background:#1877F2>Facebook</a><a href=https://www.tiktok.com/upload target=_blank class=btn style=background:#000>TikTok</a></div><div class=card><a href=/ class=btn>Continue</a></div>'
    return base_html(body)

@app.route('/add/<int:pid>')
def add(pid):
    c=session.get('cart',[])
    c.append(pid)
    session['cart']=c
    return redirect('/cart')

@app.route('/cart')
def cart():
    cart_ids=session.get('cart',[])
    subtotal=0
    items=[]
    for pid in cart_ids:
        for p in prods:
            if p['id']==pid:
                subtotal+=int(p['price'])
                items.append(p)
    sale=int(subtotal*0.05)
    off_del=int(DELIVERY*0.5)
    shop_del=DELIVERY-off_del
    total=subtotal+DELIVERY
    body='<div class=top><b>Your Cart</b></div>'
    if not items:
        body+='<div class=card><b>Cart empty</b><br><a href=/ class=btn>Browse</a></div>'
    for p in items:
        body+='<div class=card><b>'+p['name']+'</b><br>KSh '+p['price']+'</div>'
    body+='<div class=card style=background:#111;color:white><b>Order Summary</b><br>Subtotal: KSh '+str(subtotal)+'<br>Office 5 percent: KSh '+str(sale)+'<br>Delivery: KSh '+str(DELIVERY)+' Office '+str(off_del)+' Shop '+str(shop_del)+'<br><b>Total: KSh '+str(total)+'</b></div>'
    body+='<div class=card><a href=https://wa.me/254116782556?text=Order%20'+str(len(items))+'%20pairs%20KSh%20'+str(total)+' target=_blank class=btn style=background:#25D366>Order WhatsApp</a><a href=/ class=btn style=background:#111>Continue</a><a href=/clear class=btn style=background:white;color:#f68b1e;border:2px solid #f68b1e>Clear</a></div>'
    return base_html(body)

@app.route('/clear')
def clear():
    session['cart']=[]
    return redirect('/')

@app.route('/shop/<own>')
def shop(own):
    sn=''
    for n in shops:
        if shops[n]['own']==own:
            sn=n
    if not sn:
        return redirect('/')
    body='<div class=top><b>'+sn+'</b></div>'
    for p in prods:
        if p['shop']==sn:
            body+='<div class=card><b>'+p['name']+'</b><br>KSh '+p['price']+'<br><a href=/add/'+str(p['id'])+' class=btn>Add to Cart</a></div>'
    body+='<div class=card><a href=/share/'+own+' class=btn style=background:#0a8a0a>Share</a><a href=/chat/'+own+' class=btn style=background:#111>Chat</a></div>'
    return base_html(body)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        shop_name=request.form.get('shop','').strip()
        user=request.form.get('user','').strip().lower()
        area=request.form.get('area','').strip()
        till=request.form.get('till','').strip()
        if shop_name and user:
            if shop_name not in shops:
                now=datetime.now()
                trial_end=now+timedelta(days=7)
                shops[shop_name]={'own':user,'lat':-1.3956,'lng':36.7562,'area':area,'till':till,'sub':False,'sub_start':now.isoformat(),'trial_end':trial_end.isoformat()}
                chats[shop_name]=[]
                auto_samples(shop_name)
            return redirect('/share/'+user)
    body='<div class=top><b>Register Shop</b></div><div class=card><b>Register Your Shop</b><br>1 Week Free Trial Then 500 per month<br><br>Business:<br>Office 5 percent sales<br>Delivery 300 Office 50 percent<br><br><form method=post><input name=user placeholder=Username required style=width:100%;padding:16px;margin-top:8px><input name=shop placeholder=ShopName required style=width:100%;padding:16px;margin-top:8px><input name=area placeholder=Area required style=width:100%;padding:16px;margin-top:8px><input name=till placeholder=Till style=width:100%;padding:16px;margin-top:8px><button class=btn style=border:none;width:100%>Register Free Trial</button></form></div>'
    return base_html(body)

@app.route('/chat/<own>',methods=['GET','POST'])
def chat(own):
    sn=''
    for n in shops:
        if shops[n]['own']==own:
            sn=n
    if not sn:
        return redirect('/')
    if sn not in chats:
        chats[sn]=[]
    if request.method=='POST':
        m=request.form.get('msg','')
        if m:
            chats[sn].append(m)
    body='<div class=top><b>Chat '+sn+'</b></div><div class=card><form method=post style=display:flex;gap:6px><input name=msg placeholder=Message required style=flex:1;padding:16px><button style=padding:16px;background:#f68b1e;color:white;border:none>Send</button></form></div><div class=card><b>Messages</b><br>'
