from flask import Flask, render_template_string, request, redirect, session
import os, datetime, json

app = Flask(__name__)
app.secret_key = "eazymade-v9-gps-market"
TILL_MAIN = "0116782556"
OFFICE_PASS = "0116782556"
MY_FEE = 0.05

# Real Rongai GPS coordinates
KENYA_GPS = {
    "Rongai Shoe Center": {"lat": -1.3956, "lng": 36.7562, "area": "Rongai Town, Magadi Road"},
    "Mike Kicks Rongai": {"lat": -1.3980, "lng": 36.7600, "area": "Kware, Rongai"},
    "Ongata Market": {"lat": -1.3920, "lng": 36.7500, "area": "Ongata Rongai"},
}

users = {
    "admin": {"name":"John Thuo","phone":"0116782556","role":"admin","till":"0116782556","password":"0116782556","shop":"Rongai Shoe Center","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=365), "lat":-1.3956, "lng":36.7562},
}

products = [
    {"id":1, "name":"Jordan 1 Rongai","price":4500,"image":"https://images.unsplash.com/photo-1600269452121-4f2416e55c28?w=500","seller":"admin","shop":"Rongai Shoe Center","size":"42","sold":3,"stock":10,"lat":-1.3956,"lng":36.7562},
    {"id":2, "name":"Air Max 90","price":3800,"image":"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500","seller":"admin","shop":"Rongai Shoe Center","size":"41","sold":7,"stock":5,"lat":-1.3956,"lng":36.7562},
]

shops = {"Rongai Shoe Center":{"owner":"admin","till":"0116782556","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=30),"lat":-1.3956,"lng":36.7562,"area":"Rongai Town, Magadi Road - Opp Naivas"}}
chats = {}
carts = {}

BASE = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
body{font-family:Arial;margin:0;background:#f0f2f5}
.header{background:#f68b1e;padding:10px;color:white;display:flex;justify-content:space-between;position:sticky;top:0;z-index:1000}
.card{background:white;border-radius:12px;padding:12px;margin:8px;box-shadow:0 2px 8px #ddd}
.btn{border:none;padding:11px;border-radius:8px;width:100%;margin-top:6px;font-weight:bold;cursor:pointer}
.btn-o{background:#f68b1e;color:white}.btn-g{background:green;color:white}.btn-b{background:#000;color:white}.btn-w{background:#25D366;color:white}
.small{font-size:11px;color:#666}
.market-building{background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:15px;border-radius:12px;margin:8px;text-align:center}
.stock-badge{background:#e8f5e9;color:green;padding:3px 8px;border-radius:10px;font-size:10px}
input,select{width:100%;padding:11px;margin:5px 0;border:1px solid #ddd;border-radius:8px}
#map{height:350px;border-radius:12px;margin:8px}
</style></head><body>
<div style="background:#000;color:#0f0;padding:5px;text-align:center;font-size:10px">🏪 ARTIFICIAL MARKET - Rongai GPS Live | Till {{till}}</div>
<div class="header"><div>🏪 EazyMade Market</div><div><a href="/map" style="color:white">🗺️ Map</a> | <a href="/" style="color:white">Market</a> | <a href="/register" style="color:white">Join</a> | <a href="/office" style="color:white">🏢</a></div></div>
{{content}}</body></html>
"""

def is_approved(uname):
    u=users.get(uname)
    if not u: return False
    return u.get('approved',False) and datetime.datetime.now() < u.get('expiry', datetime.datetime.now())

@app.route('/')
def home():
    content = """
    <div class="market-building">
    <h2>🏪 EAZYMADE ARTIFICIAL MARKET</h2>
    <p>Walk in online - See whole shop stock before you go - Real GPS</p>
    <p style="font-size:11px">Rongai | Kware | Maasai Lodge | Ongata - All shops in one market</p>
    <a href="/map"><button class="btn btn-b" style="background:white;color:#f68b1e">🗺️ VIEW MARKET MAP - Real Kenya GPS</button></a>
    </div>
    """
    content += "<div class='card'><h3>🏪 Shops Inside Artificial Market - Click to Enter Whole Shop</h3>"
    for shop, info in shops.items():
        if not is_approved(info['owner']): continue
        cnt = len([p for p in products if p['shop']==shop])
        stock_total = sum([p['stock'] for p in products if p['shop']==shop])
        content+=f"""
        <div class="card" style="border-left:5px solid #f68b1e">
        <b style="font-size:18px">🏬 {shop}</b> <span class="stock-badge">{cnt} types | {stock_total} pairs in stock</span><br>
        <span class="small">📍 {info.get('area','Rongai')} | GPS: {info['lat']},{info['lng']} | Owner: {info['owner']} | Till: {info['till']}</span><br>
        <span class="small">Whole shop stock available - View BEFORE you go</span><br>
        <div style="display:flex;gap:5px">
        <a href="/shop/{info['owner']}" style="flex:1"><button class="btn btn-o">Enter Shop - See All Stock</button></a>
        <a href="https://www.google.com/maps?q={info['lat']},{info['lng']}" target="_blank" style="flex:1"><button class="btn btn-b">📍 GPS Navigate to Shop</button></a>
        </div>
        <a href="/chat/{info['owner']}"><button class="btn btn-w">💬 Chat with Shop Before Visiting</button></a>
        </div>
        """
    content+="</div>"

    content+="<div class='card'><h3>👟 All Stock in Market - Artificial Market View</h3><p class='small'>Like you are inside market - every shop's stock visible</p></div><div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:8px'>"
    for p in products:
        if not is_approved(p['seller']): continue
        seller = users.get(p['seller'],{})
        content+=f"""<div class="card"><img src="{p['image']}" style="width:100%;height:110px;object-fit:cover;border-radius:8px"><b>{p['name']}</b><br><span class="small">{p['shop']} | Stock: {p['stock']} left | Size {p['size']}</span><br><b style="color:#f68b1e">KSh {p['price']}</b><br><span class="small">📍 GPS {p['lat']},{p['lng']} | Till {seller.get('till')}</span><a href="/shop/{p['seller']}"><button class="btn btn-b" style="padding:5px">See Whole Shop Stock</button></a></div>"""
    content+="</div>"
    return render_template_string(BASE.replace("{{content}}",content), till=TILL_MAIN)

@app.route('/map')
def map_view():
    shops_json = json.dumps([{"shop":k,"lat":v['lat'],"lng":v['lng'],"owner":v['owner'],"area":v.get('area',''),"till":v['till'],"count":len([p for p in products if p['shop']==k])} for k,v in shops.items() if is_approved(v['owner'])])
    content = f"""
    <div class="card"><h2>🗺️ Artificial Market - Real Kenya GPS Map</h2><p class="small">Rongai shops with real GPS - Tap shop to see stock & navigate</p>
    <div id="map"></div>
    <p class="small">Map shows real location - Customers can navigate using Google Maps - GPS from your shop</p>
    </div>
    <div class="card"><h3>📍 Shops on Map</h3><div id="shoplist"></div></div>
    <script>
    var map = L.map('map').setView([-1.3956, 36.7562], 14);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
    var shops = {shops_json};
    var list = document.getElementById('shoplist');
    shops.forEach(s=>{{
        L.marker([s.lat, s.lng]).addTo(map).bindPopup(`<b>${{s.shop}}</b><br>${{s.area}}<br>${{s.count}} items in stock<br><a href='/shop/${{s.owner}}'>Enter Shop - See All Stock</a><br><a href='https://www.google.com/maps?q=${{s.lat}},${{s.lng}}' target='_blank'>Navigate</a>`);
        list.innerHTML += `<div class="card"><b>${{s.shop}}</b> - ${{s.count}} items<br><span class="small">${{s.area}} | GPS ${{s.lat}},${{s.lng}}</span><br><a href="/shop/${{s.owner}}"><button class="btn btn-o" style="padding:5px">Enter Whole Shop</button></a> <a href="https://www.google.com/maps?q=${{s.lat}},${{s.lng}}" target="_blank"><button class="btn btn-b" style="padding:5px">📍 Navigate</button></a></div>`;
    }});
    </script>
    """
    return render_template_string(BASE.replace("{{content}}",content), till=TILL_MAIN)

@app.route('/shop/<seller>')
def shop_page(seller):
    seller_info = users.get(seller,{})
    shop_name = seller_info.get('shop','Shop')
    info = shops.get(shop_name,{})
    s_prods = [p for p in products if p['seller']==seller]
    stock_total = sum(p['stock'] for p in s_prods)
    content = f"""
    <div class="market-building"><h2>🏬 {shop_name} - WHOLE SHOP</h2><p>Artificial Market - You are inside {shop_name}</p><p style="font-size:11px">📍 {info.get('area','Rongai')} | GPS {info.get('lat')},{info.get('lng')} | {stock_total} pairs total in stock | Till {seller_info.get('till')}</p></div>
    <div class="card"><h3>📦 Whole Shop Stock - {len(s_prods)} types, {stock_total} pairs available</h3><p class="small">Customer sees ALL available stock BEFORE coming - Your aim!</p><a href="https://www.google.com/maps?q={info.get('lat',-1.3956)},{info.get('lng',36.7562)}" target="_blank"><button class="btn btn-b">📍 Get Real GPS Directions to Shop</button></a><a href="/chat/{seller}"><button class="btn btn-w">💬 Chat Seller Before You Come</button></a></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:8px">
    """
    for p in s_prods:
        content+=f"""<div class="card" style="border:2px solid #f68b1e"><img src="{p['image']}" style="width:100%;height:120px;object-fit:cover;border-radius:8px"><b>{p['name']}</b><br><span class="stock-badge">In Stock: {p['stock']} left</span> <span class="small">Size {p['size']} | Sold {p['sold']} today 🔥</span><br><b style="color:#f68b1e">KSh {p['price']}</b><br><span class="small">📍 Shop GPS {p['lat']},{p['lng']}</span><a href="/add/{p['id']}"><button class="btn btn-o">Add to Cart - Pay to Till {seller_info.get('till')}</button></a></div>"""
    content+="</div><div class='card'><h3>🗺️ Shop Location - Real Kenya GPS</h3><p class='small'>Latitude: {lat} Longitude: {lng} - Real GPS for delivery boda</p><a href='https://www.google.com/maps?q={lat},{lng}' target='_blank'><button class='btn btn-b'>📍 Open in Google Maps - Navigate Real</button></a></div>".replace("{lat}",str(info.get('lat',-1.3956))).replace("{lng}",str(info.get('lng',36.7562)))
    return render_template_string(BASE.replace("{{content}}",content), till=TILL_MAIN)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        uname=request.form['username'].lower()
        if uname in users: return "Exists <a href='/register'>Back</a>"
        lat=float(request.form['lat'] or -1.3956)
        lng=float(request.form['lng'] or 36.7562)
        role=request.form['role']
        users[uname]={"name":request.form['fullname'],"phone":request.form['phone'],"role":role,"till":request.form['till'],"password":request.form['password'],"shop":request.form['shop'],"approved":False if role=='seller' else True,"expiry":datetime.datetime.now()+datetime.timedelta(days=3) if role=='seller' else datetime.datetime.now()+datetime.timedelta(days=365),"lat":lat,"lng":lng}
        if role=='seller':
            shops[request.form['shop']]={"owner":uname,"till":request.form['till'],"approved":False,"expiry":datetime.datetime.now()+datetime.timedelta(days=3),"lat":lat,"lng":lng,"area":request.form['area']}
        session['user']=uname
        return redirect('/seller/dashboard')
    content="""
    <div class="card" style="max-width:500px;margin:20px auto">
    <h2>👤 Register - Join Artificial Market</h2>
    <form method="post">
    Full Name: <input name="fullname" required>
    Phone: <input name="phone" required>
    Username: <input name="username" required>
    Password: <input name="password" type="password" required>
    Role: <select name="role"><option value="buyer">Buyer</option><option value="seller">Seller - Host whole shop</option></select>
    <div style="background:#e8f5e9;padding:10px;border-radius:8px">
    <b>IF SELLER - Whole Shop + Real GPS:</b><br>
    Shop Name: <input name="shop" placeholder="Rongai Shoe Center" required>
    Your M-Pesa Till: <input name="till" placeholder="0116782556" required>
    Shop Area: <input name="area" placeholder="Rongai Town, Magadi Road, Opp Naivas">
    <b>Real Kenya GPS (for map & delivery):</b><br>
    Latitude: <input name="lat" id="lat" placeholder="-1.3956 - Get from Google Maps" required>
    Longitude: <input name="lng" id="lng" placeholder="36.7562" required>
    <button type="button" class="btn btn-b" onclick="getGPS()" style="padding:5px">📍 Get My Current GPS Location</button>
    <p class="small">Open Google Maps, long press your shop location, copy GPS</p>
    </div>
    <button class="btn btn-g">Register Shop with Real GPS</button>
    </form>
    </div>
    <script>
    function getGPS(){
      if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(p=>{
          document.getElementById('lat').value = p.coords.latitude;
          document.getElementById('lng').value = p.coords.longitude;
          alert('GPS captured: '+p.coords.latitude+','+p.coords.longitude);
        });
      } else { alert('GPS not supported'); }
    }
    </script>
    """
    return render_template_string(BASE.replace("{{content}}",content), till=TILL_MAIN)

@app.route('/seller/dashboard')
def seller_dash():
    user=session.get('user')
    if not user: return redirect('/login')
    u=users.get(user)
    approved=is_approved(user)
    content=f"<div class='card'><h2>🏪 Seller Dashboard - Whole Shop Hosting</h2><p>Shop: {u['shop']}<br>Till: {u['till']} (customers pay you)<br>GPS: {u['lat']},{u['lng']} - Real Kenya GPS<br>Status: {'✅ Approved' if approved else '❌ Pending - Pay KSh 500 to Till 0116782556'}<br><a href='/shop/{user}'><button class='btn btn-o'>🏬 View My Whole Shop - {len([p for p in products if p['seller']==user])} types hosted</button></a><a href='https://www.google.com/maps?q={u['lat']},{u['lng']}' target='_blank'><button class='btn btn-b'>📍 View My Shop GPS on Map</button></a></div>"
    if approved: content+=f"<div class='card'><a href='/admin'><button class='btn btn-o'>📸 Post New Stock - Add to Whole Shop</button></a><p class='small'>Your shop shows ALL available stock - Customer sees before coming</p></div>"
    content+=f"<div class='card'><h3>Your Whole Shop Stock - Total {sum(p['stock'] for p in products if p['seller']==user)} pairs</h3>"
    for p in [x for x in products if x['seller']==user]:
        content+=f"<div class='card'><img src='{p['image']}' style='width:50px;height:40px'> {p['name']} - Stock {p['stock']} - KSh {p['price']}</div>"
    content+="</div>"
    return render_template_string(BASE.replace("{{content}}",content), till=TILL_MAIN)

# Keep other routes minimal for V9 GPS
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        u=users.get(request.form['username'].lower())
        if u and u['password']==request.form['password']:
            session['user']=request.form['username'].lower()
            return redirect('/')
        return "Wrong <a href='/login'>Back</a>"
    content="<div class='card' style='max-width:400px;margin:30px auto'><h2>Login</h2><form method='post'><input name='username' placeholder='Username'><input name='password' type='password'><button class='btn btn-b'>Login</button></form></div>"
    return render_template_string(BASE.replace("{{content}}",content), till=TILL_MAIN)

@app.route('/add/<int:pid>')
def add(pid):
    user=session.get('user')
    if not user: return redirect('/login')
    p=next((x for x in products if x['id']==pid),None)
    if not is_approved(p['seller']): return "Expired <a href='/'>Back</a>"
    if user not in carts: carts[user]=[]
    carts[user].append(pid); return redirect('/shop/'+p['seller'])

@app.route('/admin', methods=['GET','POST'])
def admin_add():
    user=session.get('user')
    if not user or not is_approved(user): return "Not approved - Pay sub <a href='/seller/dashboard'>Dashboard</a>"
    if request.method=='POST':
        nid=max([p['id'] for p in products])+1
        u=users[user]
        products.append({"id":nid,"name":request.form['name'],"price":int(request.form['price']),"image":request.form['image'],"seller":user,"shop":u['shop'],"size":request.form['size'],"sold":0,"stock":int(request.form['stock']),"lat":u['lat'],"lng":u['lng']})
        return redirect(f"/shop/{user}")
    content="""<div class="card"><h2>📸 Add to Whole Shop Stock</h2><form method="post"><input name="name" placeholder="Name" required><input name="price" type="number" placeholder="Price" required><input name="size" placeholder="Size"><input name="stock" type="number" placeholder="How many pairs in stock? e.g 15" required><input name="image" placeholder="Image URL imgbb.com" value="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500" required><button class="btn btn-o">Add to Whole Shop - Host Real Stock</button></form></div>"""
    return render_template_string(BASE.replace("{{content}}",content), till=TILL_MAIN)

@app.route('/office', methods=['GET','POST'])
def office():
    if request.method=='POST':
        if request.form.get('password')!=OFFICE_PASS: return "Wrong <a href='/office'>Back</a>"
        session['office']=True
    if not session.get('office'):
        return render_template_string(BASE.replace("{{content}}","<div class='card' style='max-width:400px;margin:50px auto;text-align:center'><h2>🏢 Office</h2><form method='post'><input name='password' type='password' placeholder='0116782556'><button class='btn btn-b'>Enter</button></form></div>"), till=TILL_MAIN)
    if request.args.get('approve'):
        uname=request.args.get('approve')
        if uname in users:
            users[uname]['approved']=True
            users[uname]['expiry']=datetime.datetime.now()+datetime.timedelta(days=30)
            shops[users[uname]['shop']]['approved']=True
            shops[users[uname]['shop']]['expiry']=users[uname]['expiry']
    content="<div class='card'><h2>🏢 Office - Approve + GPS</h2><table style='width:100%;font-size:11px'><tr><th>Shop</th><th>Till</th><th>GPS</th><th>Stock Hosted</th><th>Action</th></tr>"
    for shop, info in shops.items():
        cnt=len([p for p in products if p['shop']==shop])
        approved=is_approved(info['owner'])
        content+=f"<tr><td>{shop}<br>{info['owner']}</td><td>{info['till']}</td><td>{info['lat']:.4f},{info['lng']:.4f}<br><a href='https://www.google.com/maps?q={info['lat']},{info['lng']}' target='_blank'>Map</a></td><td>{cnt} types</td><td>{'✅' if approved else f'<a href=/office?approve={info[\"owner\"]}><button class=btn btn-g style=padding:3px>Approve</button></a>'}</td></tr>"
    content+="</table></div>"
    return render_template_string(BASE.replace("{{content}}",content), till=TILL_MAIN)

@app.route('/cart')
def cart():
    user=session.get('user')
    if not user: return redirect('/login')
    ids=carts.get(user,[])
    items=[p for p in products if p['id'] in ids]
    content="<div class='card'><h2>Cart</h2>"
    for p in items:
        content+=f"{p['name']} - KSh {p['price']} - Till {users[p['seller']]['till']}<br>"
    content+=f"<p>Pay each seller Till directly - GPS delivery to your location</p><a href='/'><button class='btn btn-g'>Continue Shopping Market</button></a></div>"
    return render_template_string(BASE.replace("{{content}}",content), till=TILL_MAIN)

@app.route('/chat/<seller>', methods=['GET','POST'])
def chat(seller):
    return render_template_string(BASE.replace("{{content}}",f"<div class='card'><h3>Chat with {seller} - Till {users.get(seller,{{}}).get('till')}</h3><p>Chat feature - Seller GPS {users.get(seller,{{}}).get('lat')},{users.get(seller,{{}}).get('lng')}</p><a href='/shop/{seller}'><button class='btn btn-o'>Back to Whole Shop</button></a></div>"), till=TILL_MAIN)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',10000)))
