from flask import Flask, request, redirect, session
import os, base64
app = Flask(__name__)
app.secret_key = 'v25friendly'

shops = {
    'Rongai Shoe Center': {'own': 'admin', 'till': '0116782556', 'ok': True, 'lat': -1.3956, 'lng': 36.7562, 'area': 'Rongai Town'},
    'Kitengela Sneakers': {'own': 'kiten', 'till': '0712345678', 'ok': True, 'lat': -1.38, 'lng': 36.78, 'area': 'Kitengela'},
    'Kware Market': {'own': 'kware', 'till': '0722000000', 'ok': True, 'lat': -1.40, 'lng': 36.74, 'area': 'Kware'}
}
prods = [
    {'id': 1, 'name': 'Jordan 1', 'price': 4500, 'img': 'https://via.placeholder.com/400', 'shop': 'Rongai Shoe Center', 'stock': 10},
    {'id': 2, 'name': 'Air Max 90', 'price': 3800, 'img': 'https://via.placeholder.com/400', 'shop': 'Kitengela Sneakers', 'stock': 15}
]

STYLE = """
body{margin:0;background:#f5f5f5;padding-bottom:100px;font-family:Arial}
.top{background:#f68b1e;padding:12px;display:flex;align-items:center;gap:10px}
.logo{background:white;color:#f68b1e;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:22px}
.card{background:white;border-radius:16px;padding:16px;margin:10px;box-shadow:0 2px 8px #0001}
.btn{padding:18px;border-radius:12px;width:100%;border:none;font-weight:bold;font-size:18px;margin-top:8px}
.btn-o{background:#f68b1e;color:white}
.btn-b{background:#111;color:white}
.btn-g{background:#0a8a0a;color:white}
.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:10px 0;border-top:3px solid #f68b1e;z-index:999}
.nav{text-align:center;text-decoration:none;color:#333;font-size:14px;font-weight:bold}
#map{height:65vh;width:100%;border-radius:12px}
.badge{background:red;color:white;border-radius:50%;padding:2px 7px;font-size:12px;margin-left:4px}
"""

def bottom():
    c = len(session.get('cart', []))
    b = '<span class=badge>' + str(c) + '</span>' if c > 0 else ''
    return """
    <div class=bottom>
    
