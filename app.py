from flask import Flask, request, redirect, session
import os, base64
app = Flask(__name__)
app.secret_key = 'v26green'

shops = {
    'Rongai Shoe Center': {'own': 'admin', 'till': '0116782556', 'ok': True, 'lat': -1.3956, 'lng': 36.7562, 'area': 'Rongai Town'},
    'Kitengela Sneakers': {'own': 'kiten', 'till': '0712345678', 'ok': True, 'lat': -1.38, 'lng': 36.78, 'area': 'Kitengela'},
    'Kware Market': {'own': 'kware', 'till': '0722000000', 'ok': True, 'lat': -1.40, 'lng': 36.74, 'area': 'Kware'}
}
prods = [
    {'id': 1, 'name': 'Jordan 1', 'price': 4500, 'img': 'https://via.placeholder.com/400', 'shop': 'Rongai Shoe Center', 'stock': 10},
    {'id': 2, 'name': 'Air Max 90', 'price': 3800, 'img': 'https://via.placeholder.com/400', 'shop': 'Kitengela Sneakers', 'stock': 15}
]

def style():
    return 'body{margin:0;background:#f5f5f5;padding-bottom:100px;font-family:Arial} .top{background:#f68b1e;padding:12px;display:flex;align-items:center;gap:10px} .logo{background:white;color:#f68b1e;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:22px} .card{background:white;border-radius:16px;padding:16px;margin:10px;box-shadow:0 2px 8px #0001} .btn{padding:18px;border-radius:12px;width:100%;border:none;font-weight:bold;font-size:18px;margin-top:8px} .btn-o{background
