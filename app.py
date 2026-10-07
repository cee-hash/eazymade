from flask import Flask, render_template_string, request, redirect, session
import os, datetime, json

app = Flask(__name__)
app.secret_key = "eazymade-fixed-2026"
TILL_MAIN = "0116782556"
OFFICE_PASS = "0116782556"

users = {
    "admin": {"name":"John Thuo","phone":"0116782556","role":"admin","till":"0116782556","password":"0116782556","shop":"Rongai Shoe Center","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=365), "lat":-1.3956, "lng":36.7562, "area":"Rongai Town"},
}

products = [
    {"id":1, "name":"Jordan 1 Rongai","price":4500,"image":"https://images.unsplash.com/photo-1600269452121-4f2416e55c28?w=500","seller":"admin","shop":"Rongai Shoe Center","size":"42","sold":3,"stock":10,"lat":-1.3956,"lng":36.7562},
]

shops = {"Rongai Shoe Center":{"owner":"admin","till":"0116782556","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=30),"lat":-1.3956,"lng":36.7562,"area":"Rongai Town, Magadi Road"}}

carts = {}

BASE = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
body{font-family:Arial;margin:0;background:#f0f2f5}.header{background:#f68b1e;padding:10px;color:white;display:flex;justify-content:space-between;position:sticky;top:0;z-index:1000}.card{background:white;border-radius:12px;padding:12px;margin:8px;box-shadow:0 2px 8px #ddd}.btn{border:none;padding:11px;border-radius:8px;width:100%;margin-top:6px;font-weight:bold}.btn-o{background:#f68b1e;color:white}.btn-b{background:#000;color:white}.btn-w{background:#25D366;color:white}.small{font-size:11px;color:#666}#map{height:350px;border-radius:12px}input,select{width:100%;padding:11px;margin:5px 0;border:1px solid #ddd;border-radius:8px}
</style></head><body>
<div style="background:#000;color:#0f0;padding:5px;text-align:center;font-size:10px">ARTIFICIAL MARKET - Rongai GPS Live - Till 0116782556</div>
<div class="header"><div>EazyMade Market</div><div><a href="/map" style="color:white">Map</a> | <a href="/" style="color:white">Market</a> | <a href="/office" style="color:white">Office</a></div></div>
{{content}}</body></html>
"""

def is_approved(uname):
    u=users.get(uname)
    if not u: return False
    return u.get('approved',False) and datetime.datetime.now() < u.get('expiry')

@app.route('/')
def home():
    content = "<div style='background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:15px;border-radius:12px;margin:8px;text-align:center'><h2>EAZYMADE ARTIFICIAL MARKET</h2><p>Walk in online - See whole shop stock before you go - Real GPS</p><a href='/map'><button class='btn' style='background:white;color:#f68b1e'>VIEW MARKET MAP - Real Kenya GPS</button></a></div>"
    content += "<div class='card'><h3>Shops Inside Market - Click to Enter Whole Shop</h3>"
    for shop, info in shops.items():
        if not is_approved(info['owner']): continue
        cnt = len([p for p in products if p['shop']==shop])
        total_stock = sum([p['stock'] for p in products if p['shop']==shop])
        content+=f"<div class='card' style='border-left:5px solid #f68b1e'><b>{shop}</b> - {cnt} types | {total_stock} pairs in stock<br><span class='small'>{info.get('area')} | GPS {info['lat']},{info['lng']} | Till {info['till']}</span><br><a href='/shop/{info['owner']}'><button class='btn btn-o'>Enter Shop - See All Stock</button></a><a href='https://www.google.com/maps?q={info['lat']},{info['lng']}' target='_blank'><button class='btn btn-b'>GPS Navigate to Shop</button></a></div>"
    content+="</div><div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:8px'>"
    for p in products:
        if not is_approved(p['seller']): continue
        content+=f"<div class='card'><img src='{p['image']}' style='width:100%;height:110px;object-fit:cover;border-radius:8px'><b>{p['name']}</b><br><span class='small'>Stock {p['stock']} left | {p['shop']}</span><br><b>KSh {p['price']}</b><br><span class='small'>GPS {p['lat']},{p['lng']}</span><a href='/shop/{p['seller']}'><button class='btn btn-b' style='padding:5px'>See Whole Shop</button></a></div>"
    content+="</div>"
    return render_template_string(BASE.replace("{{content}}",content))

@app.route('/map')
def map_view():
    shops_json = json.dumps([{"shop":k,"lat":v['lat'],"lng":v['lng'],"owner":v['owner'],"area":v.get('area',''),"till":v['till'],"count":len([p for p in products if p['shop']==k])} for k,v in shops.items() if is_approved(v['owner'])])
    content = f"""
    <div class="card"><h2>Artificial Market - Real Kenya GPS Map</h2><div id="map"></div></div>
    <div class="card"><h3>Shops on Map</h3><div id="shoplist"></div></div>
    <script>
    var map = L.map('map').setView([-1.3956, 36.7562], 14);
    L.tileLayer('https://'+'{{s}}.tile.openstreetmap.org/'+'{{z}}/{{x}}/{{y}}.png').addTo(map);
    var shops = {shops_json};
    var list = document.getElementById('shoplist');
    shops.forEach(s=>{{
        L.marker([s.lat, s.lng]).addTo(map).bindPopup('<b>'+s.shop+'</b><br>'+s.area+'<br>'+s.count+' items<br><a href=/shop/'+s.owner+'>Enter Shop</a>');
        list.innerHTML += '<div class=card><b>'+s.shop+'</b> - '+s.count+' items<br><span class=small>'+s.area+' | GPS '+s.lat+','+s.lng+'</span><br><a href=/shop/'+s.owner+'><button class=\"btn btn-o\" style=\"padding:5px\">Enter Whole Shop</button></a> <a href=https://www.google.com/maps?q='+s.lat+','+s.lng+' target=_blank><button class=\"btn btn-b\" style=\"padding:5px\">Navigate</button></a></div>';
    }});
    </script>
    """
    return render_template_string(BASE.replace("{{content}}",content))

@app.route('/shop/<seller>')
def shop_page(seller):
    seller_info = users.get(seller,{{}})
    shop_name = seller_info.get('shop','Shop')
    info = shops.get(shop_name,{{}})
    s_prods = [p for p in products if p['seller']==seller]
    total = sum(p['stock'] for p in s_prods)
    content = f"<div style='background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:15px;border-radius:12px;margin:8px'><h2>{shop_name} - WHOLE SHOP</h2><p>{len(s_prods)} types, {total} pairs total in stock - View BEFORE you go</p><p>GPS {info.get('lat',-1.3956)},{info.get('lng',36.7562)} | {info.get('area','Rongai')}</p></div>"
    content += f"<div class='card'><a href='https://www.google.com/maps?q={info.get('lat',-
