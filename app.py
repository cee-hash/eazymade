from flask import Flask, request, redirect, session
import os, base64, urllib.parse
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "eazymade_v58_nice_final"

# DATA
shops = {}
prods = []
chats = {}
DELIVERY = 300
SUB_FEE = 500
OFFICE_PASS = "EazyOffice2026!"

# HELPERS
def auto_samples(shop_name):
    samples = [
        ["Jordan 1 Retro", "5500", "12"],
        ["Air Force 1", "4800", "15"],
        ["Yeezy Boost", "5200", "8"],
        ["Jordan 4", "6000", "10"],
        ["Nike Dunk Low", "4700", "20"]
    ]
    for nm, pr, st in samples:
        prods.append({
            "id": len(prods) + 1,
            "name": nm,
            "price": pr,
            "img": "https://via.placeholder.com/400",
            "shop": shop_name,
            "stock": st
        })

def is_active(sh):
    if sh is None:
        return False
    if sh.get("sub") is True:
        return True
    try:
        e = sh.get("trial_end")
        if e is not None:
            if isinstance(e, str):
                e = datetime.fromisoformat(e)
            if datetime.now() <= e:
                return True
    except:
        return True
    return False

def days_left(sh):
    try:
        e = sh.get("trial_end")
        if e is not None:
            if isinstance(e, str):
                e = datetime.fromisoformat(e)
            d = e - datetime.now()
            if d.days >= 0:
                return d.days + 1
    except:
        pass
    return 0

def base_html(body, show_nav=True):
    css = """
    <style>
    body{margin:0;background:#f0f2f5;padding-bottom:160px;font-family:Arial,sans-serif;font-size:20px}
    .top{background:#f68b1e;padding:16px;color:white;font-weight:bold}
    .card{background:white;margin:12px;padding:16px;border-radius:16px;border-left:6px solid #f68b1e;box-shadow:0 2px 6px rgba(0,0,0,0.1)}
    .btn{display:block;padding:14px;background:#f68b1e;color:white;text-align:center;margin-top:10px;text-decoration:none;font-weight:bold;border-radius:10px}
    .btn-dark{background:#111}
    .btn-green{background:#0a8a0a}
    .bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:14px 0;border-top:3px solid #f68b1e;z-index:999}
    .nav{color:#222;text-decoration:none;font-weight:bold}
    .foot{text-align:center;padding:30px 15px;color:#666;font-size:13px;background:white;margin-top:30px;border-top:2px solid #eee;line-height:1.6}
    </style>
    """
    nav = ""
    if show_nav is True:
        cart = session.get("cart", [])
        count = str(len(cart)) if len(cart) > 0 else ""
        nav = f"<div class=bottom><a href=/ class=nav>Market</a><a href=/register class=nav>Reg</a><a href=/post class=nav>Post</a><a href=/cart class=nav>Cart {count}</a></div>"
    
    foot = """
    <div class=foot>
    © 2026 EazyMade Market - All Rights Reserved<br>
    Langata Rongai | Kitengela | Kware | Nairobi<br>
    Owner: EazyMade | Phone: 0116782556 | Till: 0116782556<br>
    Office Private - Only Owner Access via /office<br>
    Designed & Built by EazyMade Team - Nairobi, Kenya<br>
    </div>
    """
    return css + body + foot + nav

@app.errorhandler(404)
def not_found(e):
    return redirect("/")

# ROUTES
@app.route("/")
def home():
    body = "<div class=top>EAZYMADE MARKET - Rongai | Kitengela | Kware</div>"
    body += f"<div class=card><b>Welcome to EazyMade © 2026</b><br>{len(shops)} Shops - {len(prods)} Shoes Available<br><a href=/register class=btn>Register Your Shop - 1 Week Free</a></div>"
    
    if len(shops) == 0:
        body += "<div class=card><b>No shops yet - Be first!</b><br><a href=/register class=btn>Register Now - Free</a></div>"

    for shop_name in list(shops.keys()):
        sh = shops[shop_name]
        if is_active(sh) is False:
            continue
        total_types = 0
        total_stock = 0
        for p in prods:
            if p["shop"] == shop_name:
                total_types += 1
                total_stock += int(p["stock"])
        enc = urllib.parse.quote(f"Shop {shop_name} on EAZYMADE MARKET - {total_stock} pairs!")
        sp = "/shop/" + sh["own"]
        sr = "/share/" + sh["own"]
        cp = "/chat/" + sh["own"]
        body += f"<div class=card><b>{shop_name}</b><br>{sh['area']} - {total_types} Types - {total_stock} Pairs<br><a href={sp} class=btn>Enter Shop - {total_stock} Pairs</a><a href={sr} class=btn>Share Shop</a><a href=https://wa.me/?text={enc} target=_blank class=btn>WhatsApp Share</a><a href={cp} class=btn>Chat with Owner</a></div>"

    for p in prods:
        if p["shop"] in shops and is_active(shops[p["shop"]]) is True:
            ap = "/add/" + str(p["id"])
            body += f"<div class=card><img src={p['img']} style=width:100%;height:200px;object-fit:cover;border-radius:12px><br><b>{p['name']}</b><br>KSh {p['price']} - Stock {p['stock']}<br>Shop: {p['shop']}<br><a href={ap} class=btn>Add to Cart</a></div>"

    body += "<div class=card><b>Shops Location - Rongai Area</b><br>"
    for shop_name in list
