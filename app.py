from flask import Flask,request,redirect,session
import os,base64,urllib.parse
from datetime import datetime,timedelta

app=Flask(__name__)
app.secret_key="v49onlyyou"

shops={}
prods=[]
chats={}

DELIVERY=300
SUB_FEE=500
OFFICE_PASS="EazyOffice2026!"

def auto_samples(shop_name):
    samples=[
        ["Jordan 1 Retro High","5500","12"],
        ["Air Force 1 White","4800","15"],
        ["Yeezy Boost 350","5200","8"],
        ["Jordan 4 Black","6000","10"],
        ["Nike Dunk Low","4700","20"]
    ]
    for nm,pr,st in samples:
        prods.append({"id":len(prods)+1,"name":nm,"price":pr,"img":"https://via.placeholder.com/400","shop":shop_name,"stock":st})

def is_active(sh):
    if not sh:
        return False
    if sh.get("sub"):
        return True
    try:
        end=sh.get("trial_end")
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
        end=sh.get("trial_end")
        if end:
            if isinstance(end,str):
                end=datetime.fromisoformat(end)
            d=end-datetime.now()
            if d.days>=0:
                return d.days+1
    except:
        pass
    return 0

def base_html(body,show_nav=True):
    css="body{margin:0;background:#f0f2f5;padding-bottom:130px;font-family:Arial;font-size:26px}"
    css+=".top{background:#f68b1e;padding:16px;position:sticky;top:0;z-index:100}"
    css+=".card{background:white;border-radius:16px;padding
