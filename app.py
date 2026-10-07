from flask import Flask, render_template_string, request, redirect, session
import os, datetime, json

app = Flask(__name__)
app.secret_key = "eazymade-v11-logo-all"
TILL_MAIN = "0116782556"
OFFICE_PASS = "0116782556"

users = {
    "admin": {"name":"John Thuo","phone":"0116782556","role":"admin","till":"0116782556","password":"0116782556","shop":"Rongai Shoe Center","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=365),"lat":-1.3956,"lng":36.7562,"area":"Rongai Town, Magadi Road"}
}

products = [
    {"id":1,"name":"Jordan 1 Rongai","price":4500,"image":"https://images.unsplash.com/photo-1600269452121-4f2416e55c28?w=500","seller":"admin","shop":"Rongai Shoe Center","size":"42","stock":10,"sold":3,"lat":-1.3956,"lng":36.7562},
    {"id":2,"name":"Air Max 90","price":3800,"image":"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500","seller":"admin","shop":"Rongai Shoe Center","size":"41","stock":5,"sold":7,"lat":-1.3956,"lng":36.7562},
]

shops = {
    "Rongai Shoe Center": {"owner":"admin","till":"0116782556","approved":True,"expiry":datetime.datetime.now()+datetime.timedelta(days=30),"lat":-1.3956,"lng":36.7562,"area":"Rongai Town, Magadi Road, Opp Naivas"}
}

carts = {}

def is_ok(uname):
    u = users.get(uname)
    if not u:
        return False
    return u.get("approved") and datetime.datetime.now() < u.get("expiry")

HEADER = """
<div style="background:#000;color:#0f0;padding:4px;text-align:center;font-size:10px">ARTIFICIAL MARKET - Till 0116782556 - Whole Shop + Real GPS + Own Till</div>
<div style="background:#f68b1e;padding:10px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:1000">
<div style="display:flex;align-items:center;gap:8px">
<div style="background:white;color:#f68b1e;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:20px">E</div>
<div><b style="color:white;font-size:18px">EAZYMADE</b><br><span style="color:white;font-size:10px">ARTIFICIAL MARKET - Rongai</span></div>
</div>
<div style="color:white;font-size:12px"><a href="/map" style="color:white;text-decoration:none">Map</a> | <a href="/" style="color:white;text-decoration:none">Market</a> | <a href="/office" style="color:white;text-decoration:none">Office</a></div>
</div>
"""

FOOTER_STYLE = """
<style>body{font-family:Arial;margin:0;background:#f0f2f5}.card{background:white;border-radius:12px;padding:12px;margin:8px;box-shadow:0 2px 8px #ddd}.btn{border:none;padding:11px;border-radius:8px;width:100%;margin-top:6px;font-weight:bold;cursor:pointer}.btn-o{background:#f68b1e;color:white}.btn-b{background:#000;color:white}.btn-g{background:green;color:white}.small{font-size:11px;color:#666}#map{height:380px;border-radius:12px}.logo-text{font-weight:bold;color:#f68b1e}input,select{width:100%;padding:11px;margin:5px 0;border:1px solid #ddd;border-radius:8px}</style>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
"""

@app.route("/")
def home():
    html = FOOTER_STYLE + HEADER
    html += "<div style='background:linear-gradient(135deg,#f68b1e,#000);color:white;padding:18px;border-radius:12px;margin:8px;text-align:center'><div style='background:white;color:#f68b1e;width:60px;height:60px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:bold;margin:0 auto'>E</div><h2 style='margin:8px 0'>EAZYMADE ARTIFICIAL MARKET</h2><p>Walk in online - See whole shop stock BEFORE you go - Real Kenya GPS</p><a href='/map'><button class='btn' style='background:white;color:#f68b1e'>VIEW MARKET MAP - Real GPS</button></a><a href='/register'><button class='btn btn-b'>Everyone Register - Buyer or Seller</button></a></div>"
    html += "<div class='card'><h3>Shops Inside Market - Enter to See Whole Stock (Your Aim)</h3>"
    for sname, sinfo in shops.items():
        if not is_ok(sinfo["owner"]):
            continue
        cnt = len([p for p in products if p["shop"] == sname])
        tot = sum([p["stock"] for p in products if p["shop"] == sname])
        html += "<div class='card' style='border-left:5px solid #f68b1e'><b>" + sname + "</b> - " + str(cnt) + " types | " + str(tot) + " pairs in stock<br><span class='small'>" + sinfo["area"] + " | GPS " + str(sinfo["lat"]) + "," + str(sinfo["lng"]) + " | Pay to Till " + sinfo["till"] + "</span><br><span class='small'>Customer views ALL before coming</span><br><a href='/shop/" + sinfo["owner"] + "'><button class='btn btn-o'>Enter Whole Shop</button></a><a href='https://www.google.com/maps?q=" + str(sinfo["lat"]) + "," + str(sinfo["lng"]) + "' target='_blank'><button class='btn btn-b'>GPS Navigate - Real</button></a></div>"
    html += "</div><div class='card'><h3>All Stock</h3></div><div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:8px'>"
    for p in products:
        if not is_ok(p["seller"]):
            continue
        html += "<div class='card'><img src='" + p["image"] + "' style='width:100%;height:110px;object-fit:cover;border-radius:8px'><b>" + p["name"] + "</b><br><span class='small'>Stock " + str(p["stock"]) + " | " + p["shop"] + "</span><br><b>KSh " + str(p["price"]) +
