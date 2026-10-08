from flask import Flask,request,redirect,session
import os,base64,urllib.parse
from datetime import datetime,timedelta
app=Flask(__name__)
app.secret_key='v47fullkeepall'

shops={}
prods=[]
chats={}

DELIVERY=300
SUB_FEE=500

def auto_samples(shop_name):
    samples=[["Jordan 1 Retro High","5500","12"],["Air Force 1 White","4800","15"],["Yeezy Boost 350","5200","8"],["Jordan 4 Black","6000","10"],["Nike Dunk Low","4700","20"]]
    for nm,pr,st in samples:
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
    style='body{margin:0;background:#f0f2f5;padding-bottom:130px;font-family:Arial;font-size:26px}.top{background:#f68b1e;padding:16px;position:sticky;top:0;z-index:100}.card{background:white;border-radius:16px;padding:20px;margin:12px;border-left:6px solid #f68b1e;box-shadow:0 4px 10px #0001}.btn{display:block;padding:18px;border-radius:12px;text-align:center;text-decoration:none;font-weight:bold;margin-top:10px;color:white;background:#f68b1e}.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:10px 0;border-top:4px solid #f68b1e;z-index:999}.nav{text-align:center;text-decoration:none;color:#222;font-size:16px;font-weight:bold}#map{height:60vh;width:100%;border-radius:12px}.chat-msg{background:#f0f2f5;padding:14px;border-radius:12px;margin:8px 0;border-left:5px solid #f68b1e}'
    cart=session.get('cart',[])
    txt=''
    if cart:
        txt=str(len(cart))
    nav='<div class="bottom"><a href="/" class="nav">Market</a><a href="/register" class="nav">Register</a><a href="/post" class="nav">Post</a><a href="/cart" class="nav">Cart '+txt+'</a><a href="/office" class="nav">Office</a></div>'
    return '<style>'+style+'</style>'+body+nav

@app.errorhandler(404)
def nf(e):
    return redirect('/')

@app.route('/')
def home():
    body='<div class="top"><b style="color:white">EAZYMADE MARKET</b><div style="color:white;font-size:18px">Shops Near You - Rongai Kitengela Kware</div></div>'
    body+='<div class="card" style="background:linear-gradient(135deg,#f68b1e,#000);color:white;border-left:none;text-align:center"><b>Welcome to EazyMade</b><br>'+str(len(shops))+' Shops - '+str(len(prods))+' Shoes Available<br><a href="/register" class="btn" style="background:#0a8a0a">Register Your Shop - 1 Week Free Trial</a><a href="/map" class="btn" style="background:white;color:#f68b1e;border:2px solid #f68b1e">View Map</a></div>'
    if not shops:
        body+='<div class="card"><b>No shops yet</b><br>Be first to register - 1 week free trial included<br><a href="/register" class="btn">Register Now</a></div>'
    for name in shops:
        sh=shops[name]
        if not is_active(sh):
            continue
        tot=0
        stock=0
        for p in prods:
            if p["shop"]==name:
                tot+=1
                stock+=int(p["stock"])
        dl=days_left(sh)
        tr=''
        if dl>0 and not sh.get('sub'):
            tr=' - '+str(dl)+' days free trial left'
        enc=urllib.parse.quote('New shop '+name+' '+str(stock)+' pairs on EAZYMADE')
        body+='<div class="card"><b>'+name+'</b><br>'+sh["area"]+' - '+str(tot)+' Types - '+str(stock)+' Pairs'+tr+'<br>Owner: '+sh["own"]+'<br>Till: '+sh["till"]+'<br><a href="/shop/'+sh["own"]+'" class="btn">Enter Shop - '+str(stock)+' Pairs</a><a href="/share/'+sh["own"]+'" class="btn" style="background:#0a8a0a">Share Shop to Social</a><div style="display:flex;gap:6px;margin-top:8px"><a href="https://wa.me/?text='+enc+'" target="_blank" class="btn" style="flex:1;background:#25D366">WhatsApp</a><a href="/chat/'+sh["own"]+'" class="btn" style="flex:1;background:#111">Chat</a><a href="https://www.google.com/maps?q='+str(sh["lat"])+','+str(sh["lng"])+'" target="_blank" class="btn" style="flex:1;background:white;color:#f68b1e;border:2px solid #f68b1e">GPS Directions</a></div></div>'
    for p in prods:
        if p["shop"] not in shops:
            continue
        if not is_active(shops[p["shop"]]):
            continue
        body+='<div class="card"><img src="'+p["img"]+'" style="width:100%;height:220px;object-fit:cover;border-radius:12px"><br><b>'+p["name"]+'</b><br><span style="color:#f68b1e;font-weight:bold">KSh '+p["price"]+'</span><br>'+p["shop"]+' - Stock '+p["stock"]+' Pairs<br><a href="/add/'+str(p["id"])+'" class="btn">Add to Cart</a></div>'
    body+='<div class="card"><b>Shops on Map</b><div id="map"></div></div><link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script><script>var m=L.map("map").setView([-1.3956,36.7562],12);L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(m);'
    for n in shops:
        if not is_active(shops[n]):
            continue
        sh=shops[n]
        body+='L.marker(['+str(sh["lat"])+','+str(sh["lng"])+']).addTo(m).bindPopup("'+n+'");'
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
    tot=0
    stock=0
    for p in prods:
        if p['shop']==sn:
            tot+=1
            stock+=int(p['stock'])
    dl=days_left(sh)
    msg='New shop '+sn+' '+str(stock)+' pairs on EAZYMADE MARKET - '+str(dl)+' days free trial - Visit now'
    enc=urllib.parse.quote(msg)
    body='<div class="top"><b>Share - '+sn+'</b></div><div class="card" style="background:#25D366;color:white;border-left:none;text-align:center"><b>Shop Ready - '+str(dl)+' Days Free Trial</b><br>'+str(tot)+' Types - '+str(stock)+' Pairs Auto Posted</div><div class="card"><b>Share Your Shop to Get Customers</b><div style="background:#f0f2f5;padding:14px;border-radius:12px;margin-top:10px">'+msg+'</div><a href="https://wa.me/?text='+enc+'" target="_blank" class="btn" style="background:#25D366;margin-top:12px">Share to WhatsApp</a><a href="https://www.facebook.com/sharer/sharer.php?u=https://eazymade-market.com" target="_blank" class="btn" style="background:#1877F2;margin-top:8px">Share to Facebook</a><a href="https://www.tiktok.com/upload" target="_blank" class="btn" style="background:#000;margin-top:8px">Share to TikTok</a></div><div class="card"><a href="/" class="btn">Continue to Market</a></div>'
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
    body='<div class="top"><b>Your Cart - Business Model</b></div>'
    if not items:
        body+='<div class="card"><b>Cart is empty</b><br><a href="/" class="btn">Browse Shops</a></div>'
    for p in items:
        body+='<div class="card"><b>'+p['name']+'</b><br>KSh '+p['price']+' - '+p['shop']+'</div>'
    body+='<div class="card" style="background:#111;color:white"><b>Order Summary - Office Earnings</b><br><br>Subtotal: KSh '+str(subtotal)+'<br><span style="color:#ccc">Office 5 percent of sales: KSh '+str(sale)+'</span><br><span style="color:#ccc">Delivery KSh '+str(DELIVERY)+' - Office 50 percent KSh '+str(off_del)+' + Shop 50 percent KSh '+str(shop_del)+'</span><hr><b style="font-size:30px">Total to Pay: KSh '+str(total)+'</b></div><div class="card"><a href="https://wa.me/254116782556?text=Order%20'+str(len(items))+'%20pairs%20Total%20KSh%20'+str(total)+'" target="_blank" class="btn" style="background:#25D366">Order on WhatsApp</a><a href="/" class="btn" style="background:#111">Continue Shopping</a><a href="/clear" class="btn" style="background:white;color:#f68b1e;border:2px solid #f68b1e">Clear Cart</a></div>'
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
    tot=0
    stock=0
    for p in prods:
        if p['shop']==sn:
            tot+=1
            stock+=int(p['stock'])
    body='<div class="top"><b>'+sn+' - '+str(stock)+' Pairs Available</b></div><div class="card" style="background:linear-gradient(135deg,#f68b1e,#ff9a3d);color:white"><b>'+sn+'</b><br>'+shops[sn]["area"]+' - '+str(tot)+' Types - '+str(stock)+' Pairs</div>'
    for p in prods:
        if p['shop']==sn:
            body+='<div class="card"><img src="'+p['img']+'" style="width:100%;height:200px;object-fit:cover;border-radius:12px"><br><b>'+p['name']+'</b><br><span style="color:#f68b1e;font-weight:bold">KSh '+p['price']+'</span><br>Stock '+p['stock']+'<br><a href="/add/'+str(p['id'])+'" class="btn">Add to Cart</a></div>'
    body+='<div class="card"><a href="/share/'+own+'" class="btn" style="background:#0a8a0a">Share Shop</a><a href="/chat/'+own+'" class="btn" style="background:#111">Chat with Shop Owner</a><a href="https://www.google.com/maps?q='+str(shops[sn]['lat'])+','+str(shops[sn]['lng'])+'" target="_blank" class="btn" style="background:white;color:#f68b1e;border:2px solid #f68b1e">Get GPS Directions</a></div>'
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
    body='<div class="top"><b>Register Your Shop - Business</b></div><div class="card"><b>Register Your Shoe Shop</b><p>1 Week Free Trial - Then KSh 500 per month to stay visible</p><div style="background:#e8f5e9;padding:14px;border-radius:12px;border-left:6px solid #0a8a0a"><b>Free Trial Offer - 7 Days FREE</b><br>5 Shoes auto posted free on registration<br>Shop visible on market and map for 7 days<br>After trial: KSh 500 per month subscription<br><br><b>Business Model - Office Earnings:</b><br>Office takes 5 percent of every sale<br>Delivery KSh 300 - Office takes 50 percent (KSh 150) + Shop takes 50 percent<br>Chat with customers included<br>Auto post to TikTok WhatsApp Facebook</div><form method="post"><input name="user" placeholder="Username e.g. admin" required style="width:100%;padding:16px;margin-top:8px"><input name="shop" placeholder="Shop name e.g. Rongai Shoe Center" required style="width:100%;padding:16px;margin-top:8px"><input name="area" placeholder="Area e.g. Rongai Town" required style="width:100%;padding:16px;margin-top:8px"><input name="till" placeholder="Till or Phone e.g. 0116782556" style="width:100%;padding:16px;margin-top:8px"><button class="btn" style="border:none;width:100%;margin-top:12px">Register - Start 1 Week Free Trial</button></form></div>'
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
    body='<div class="top"><b>Chat - '+sn+' - Big Font</b></div><div class="card"><b>Chat with Shop Owner</b><br>Ask about size, price, stock before you visit - Big font for easy reading<br><form method="post" style="display:flex;gap:6px;margin-top:12px"><input name="msg" placeholder="Ask e.g. Size 43 available?" required style="flex:1;padding:16px"><button style="padding:16px;background:#f68b1e;color:white;border:none;border-radius:12px">Send</button></form></div><div class="card"><b>Messages - '+str(len(chats[sn]))+' chats</b><br>'
    if not chats[sn]:
        body+='<div class="chat-msg">No messages yet - Say hello to shop owner</div>'
    for mm in chats[sn][-20:]:
        body+='<div class="chat-msg">'+mm+'</div>'
    body+='</div><div class="card"><a href="/shop/'+own+'" class="btn" style="background:#111">Back to Shop</a><a href="https://www.google.com/maps?q='+str(shops[sn]['lat'])+','+str(shops[sn]['lng'])+'" target="_blank" class="btn" style="background:white;color:#f68b1e;border:2px solid #f68b1e">Get Directions</a></div>'
    return base_html(body)

@app.route('/subscribe/<own>')
def subscribe(own):
    sn=''
    for n in shops:
        if shops[n]['own']==own:
            sn=n
    if not sn:
        return redirect('/')
    shops[sn]['sub']=True
    shops[sn]['sub_start']=datetime.now().isoformat()
    body='<div class="card" style="background:#0a8a0a;color:white;text-align:center"><b>Subscribed Successfully</b><br>'+sn+' active for 30 days - KSh 500 paid<br>1 week free trial converted to paid subscription</div><div class="card"><a href="/" class="btn">Go to Market</a></div>'
    return base_html(body)

@app.route('/office',methods=['GET','POST'])
def office():
    if request.method=='POST':
        pw=request.form.get('password','')
        if pw=='0116782556':
            session['off']=True
    if not session.get('off'):
        body='<div class="top"><b>Office Login - Business Dashboard</b></div><div class="card"><b>Office Access - Enter Password</b><form method="post"><input name="password" type="password" placeholder="Password 0116782556" required style="width:100%;padding:16px"><button class="btn" style="border:none;width:100%;background:#111;margin-top:10px">Enter Office Dashboard</button></form></div>'
        return base_html(body)
    total_sales=0
    for p in prods:
        total_sales+=int(p['price'])
    office_sale=int(total_sales*0.05)
    delivery_orders=len(prods)
    office_delivery=int(delivery_orders*DELIVERY*0.5)
    sub_income=0
    active=0
    trial=0
    expired=0
    for n in shops:
        if is_active(shops[n]):
            active+=1
            if shops[n].get('sub'):
                sub_income+=SUB_FEE
            else:
                trial+=1
        else:
            expired+=1
    body='<div class="top"><b>Office Dashboard - Business Earnings</b></div><div class="card" style="background:#111;color:white"><b>Business Summary - Keep All Features</b><br><br>Shops Total: '+str(len(shops))+'<br>Active Shops: '+str(active)+' (Paid: '+str(active-trial)+' + Trial: '+str(trial)+')<br>Expired Shops: '+str(expired)+'<br>Products Total: '+str(len(prods))+'<br>Total Sales Value: KSh '+str(total_sales)+'<hr>Office 5 percent Sales Cut: KSh '+str(office_sale)+'<br>Office 50 percent Delivery Cut: KSh '+str(office_delivery)+' ('+str(delivery_orders)+' deliveries x KSh 150)<br>Subscription Income: KSh '+str(sub_income)+' ('+str(active-trial)+' paid shops x KSh 500)<br><br><b style="color:#f68b1e;font-size:28px">Total Office Income: KSh '+str(office_sale+office_delivery+sub_income)+'</b><br><br>Business: 5 percent sales + 50 percent delivery + 500 subscription + 1 week free trial + chat + auto social</div>'
    for n in shops:
        sh=shops[n]
        dl=days_left(sh)
        if sh.get('sub'):
            status='Active Paid - Subscribed'
        elif is_active(sh):
            status='Free Trial - '+str(dl)+' days left - Will expire'
        else:
            status='Expired - Needs KSh 500 subscription'
        body+='<div class="card"><b>Shop: '+n+'</b><br>Owner Username: '+sh['own']+'<br>Area: '+sh['area']+'<br>Till: '+sh['till']+'<br>Status: '+status+'<br>Lat: '+str(sh['lat'])+' Lng: '+str(sh['lng'])+'<br>Products: '+str(len([p for p in prods if p["shop"]==n]))+'<br>Chats: '+str(len(chats.get(n,[])))+'<br><a href="/subscribe/'+sh['own']+'" class="btn" style="background:#0a8a0a">Activate Subscription KSh 500 - Extend 30 Days</a><a href="/share/'+sh['own']+'" class="btn" style="background:#25D366">Share Shop Social</a><a href="/chat/'+sh['own']+'" class="btn" style="background:#111">View Chats ('+str(len(chats.get(n,[])))+')</a><a href="/shop/'+sh['own']+'" class="btn" style="background:white;color:#f68b1e;border:2px solid #f68b1e">Enter Shop View</a></div>'
    return base_html(body)

@app.route('/post',methods=['GET','POST'])
def post():
    if request.method=='POST':
        bulk=request.form.get('bulk','').strip()
        if bulk:
            shop_name=request.form.get('shop_select','')
            if not shop_name and shops:
                shop_name=list(shops.keys())[0]
            for line in bulk.split('\n'):
                if not line.strip():
                    continue
                parts=line.strip().split()
                if len(parts)>=3:
                    nm=' '.join(parts[:-2])
                    pr=parts[-2]
                    st=parts[-1]
                    prods.append({'id':len(prods)+1,'name':nm,'price':pr,'img':'https://via.placeholder.com/400','shop':shop_name,'stock':st})
            return redirect('/')
        f=request.files.get('pic')
        img='https://via.placeholder.com/400'
        if f and f.filename!='':
            img='data:image/jpeg;base64,'+base64.b64encode(f.read()).decode()
        shop_name=request.form.get('shop_select','')
        if not shop_name and shops:
            shop_name=list(shops.keys())[0]
        prods.append({'id':len(prods)+1,'name':request.form['name'],'price':request.form['price'],'img':img,'shop':shop_name,'stock':request.form['stock']})
        return redirect('/')
    if not shops:
        return base_html('<div class="card"><b>No shops registered yet</b><br>Register first to post products<br><a href="/register" class="btn">Register Shop - 1 Week Free</a></div>')
    opts=''
    for n in shops:
        opts+='<option value="'+n+'">'+n+'</option>'
    body='<div class="top"><b>Post Products - Bulk and Single</b></div><div class="card"><b>Bulk Post - Many Shoes at Once</b><br>Format per line: Name Price Stock<br>Example: Jordan 1 Retro 5500 12<br><form method="post"><select name="shop_select" style="width:100%;padding:12px">'+opts+'</select><textarea name="bulk" placeholder="Jordan 1 Retro 5500 12\nAir Force 1 White 4800 15" style="width:100%;height:120px;padding:14px;margin-top:10px"></textarea><button class="btn" style="background:#0a8a0a;border:none;width:100%;margin-top:10px">Post Many Shoes at Once - Auto</button></form></div><div class="card"><b>Single Post with Camera</b><br>Take photo with phone camera<br><form method="post" enctype="multipart/form-data"><select name="shop_select" style="width:100%;padding:12px">'+opts+'</select><input name="name" placeholder="Shoe name e.g. Jordan 1 Retro High" required style="width:100%;padding:12px;margin-top:6px"><input name="price" placeholder="Price e.g. 5500" required style="width:100%;padding:12px;margin-top:6px"><input name="stock" placeholder="Stock pairs e.g. 12" required style="width:100%;padding:12px;margin-top:6px"><input type="file" name="pic" accept="image/*" capture="environment" style="width:100%;padding:10px;margin-top:8px"><button class="btn" style="border:none;width:100%;margin-top:8px">Post Single Shoe with Photo</button></form></div>'
    return base_html(body)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
