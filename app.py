from flask import Flask, render_template_string, request, redirect, session
import os, datetime, json, urllib.parse

app = Flask(__name__)
app.secret_key = "eazymade-v10-all-features"
TILL_MAIN = "0116782556"
OFFICE_PASS = "0116782556"
MY_FEE = 0.05

users = {
    "admin": {"name":"John Thuo","phone":"0116782556","role":"admin","till":"0116782556","password":"0116782556","shop":"Rongai Shoe Center","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=365),"lat":-1.3956,"lng":36.7562,"area":"Rongai Town, Magadi Road"}
}

products = [
    {"id":1,"name":"Jordan 1 Rongai","price":4500,"image":"https://images.unsplash.com/photo-1600269452121-4f2416e55c28?w=500","seller":"admin","shop":"Rongai Shoe Center","size":"42","stock":10,"sold":3,"lat":-1.3956,"lng":36.7562},
    {"id":2,"name":"Air Max 90","price":3800,"image":"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500","seller":"admin","shop":"Rongai Shoe Center","size":"41","stock":5,"sold":7,"lat":-1.3956,"lng":36.7562},
]

shops = {"Rongai Shoe Center":{"owner":"admin","till":"0116782556","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=30),"lat":-1.3956,"lng":36.7562,"area":"Rongai Town, Magadi Road, Opp Naivas"}}
carts = {}
chats = {}

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
.small{font-size:11px;color:#666}input,select{width:100%;padding:11px;margin:5px 0;border:1px solid #ddd;border-radius:8px}
#map{height:350px;border-radius:12px;margin:8px}.market{background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:15px;border-radius:12px;margin:8px;text-align:center}
.badge{background:#e8f5e9;color:green;padding:3px 8px;border-radius:10px;font-size:10px}
</style></head><body>
<div style="background:#000;color:#0f0;padding:5px;text-align:center;font-size:10px">ARTIFICIAL MARKET - Whole Shop + Real GPS + Own Till - Admin Till 0116782556</div>
<div class="header"><div>🏪 EazyMade</div><div><a href="/map" style="color:white">🗺️Map</a> | <a href="/" style="color:white">Market</a> | USER_LINKS</div></div>
CONTENT_HERE</body></html>
"""

def is_approved(uname):
    u = users.get(uname)
    if not u: return False
    return u.get('approved',False) and datetime.datetime.now() < u.get('expiry', datetime.datetime.now())

def user_links():
    u = session.get('user')
    if u:
        role = users.get(u,{}).get('role','')
        return u + " (" + role + ") | <a href='/seller/dashboard' style='color:white'>Dashboard</a> | <a href='/logout' style='color:white'>Logout</a> | <a href='/cart' style='color:white'>Cart</a>"
    else:
        return "<a href='/login' style='color:white'>Login</a> | <a href='/register' style='color:white'>Register</a>"

@app.route('/')
def home():
    html = "<div class='market'><h2>🏪 EAZYMADE ARTIFICIAL MARKET</h2><p>Walk in online - See whole shop stock BEFORE you go - Real GPS Navigation</p><p style='font-size:11px'>Rongai | Kware | Ongata - All shops in one building</p><a href='/map'><button class='btn' style='background:white;color:#f68b1e'>🗺️ VIEW MARKET MAP - Real Kenya GPS</button></a><a href='/register'><button class='btn btn-b'>👤 Everyone Register - Buyer or Seller</button></a></div>"
    html += "<div class='card'><h3>🏬 Shops Inside Market - Enter to See Whole Stock (Your Aim)</h3>"
    for sname, sinfo in shops.items():
        owner = sinfo['owner']
        if not is_approved(owner): continue
        cnt = len([p for p in products if p['shop']==sname])
        tot = sum([p['stock'] for p in products if p['shop']==sname])
        html += "<div class='card' style
