from flask import Flask,request,redirect,session
import os,base64
app=Flask(__name__)
app.secret_key='tiny32'

shops={
'Rongai':{'own':'admin','ok':True,'lat':-1.3956,'lng':36.7562},
'Kitengela':{'own':'kiten','ok':True,'lat':-1.38,'lng':36.78}
}
prods=[
{'id':1,'name':'Jordan 1','price':4500,'img':'https://via.placeholder.com/400','shop':'Rongai','stock':10},
{'id':2,'name':'Air Max','price':3800,'img':'https://via.placeholder.com/400','shop':'Kitengela','stock':15}
]
chats={}

def css():
 a='body{margin:0;background:#f5f5f5;'
 b='padding-bottom:120px;font-size:28px;font-family:Arial}'
 c='.top{background:#f68b1e;padding:16px;display:flex}'
 d='.card{background:white;border-radius:18px;'
 e='padding:20px;margin:12px;box-shadow:0 4px 10px #0001}'
 f='.btn{display:block;padding:20px;background:#f68b1e;'
 g='color:white;text-align:center;border-radius:14px;'
 h='text-decoration:none;font-weight:bold;margin-top:10px}'
 i='.bottom{position:fixed;bottom:0;left:0;right:0;'
 j='background:white;display:flex;justify-content:space-around;'
 k='padding:12px 0;border-top:4px solid #f68b1e}'
 l='.nav{text-align:center;text-decoration:none;color:#222;font-size:20px}'
 return a+b+c+d+e+f+g+h+i+j+k+l

def nav():
 c=len(session.get('cart',[]))
 b='('+str(c)+')' if c>0 else ''
 return '<div class=bottom><a href=/ class=nav>Market</a><a href=/cart class=nav>Cart '+b+'</a><a href=/ai class=nav>AI</a><a href=/office class=nav>Office</a></div>'

@app.route('/')
def home():
 s=css()
 h='<style>'+s+'</style><div class=top><b style=color:white;font-size:30px>EAZYMADE</b></div>'
 h+='<div class=card><b style=font-size:32px>All Shops 28px</b><p>Buttons fixed - Tiny code</p></div>'
 for name in shops:
  tot=0
  for p in prods:
   if p['shop']==name:
    tot+=int(p['stock'])
  h+='<div class=card><b style=font-size:28px>'+name+'</b> '+str(tot)+' pairs<a href=/shop/'+shops[name]['own']+' class=btn>Enter Shop</a><a href=/chat/'+shops[name]['own']+' class=btn style=background:#111>Chat</a></div>'
 for p in prods:
  h+='<div class=card><img src='+p['img']+' style=width:100%;height:200px;object-fit:cover;border-radius:12px><br><b>'+p['name']+'</b> KSh '+str(p['price'])+'<a href=/add/'+str(p['id'])+' class=btn>Add to Cart</a></div>'
 h+='<div class=card><div id=map style=height:50vh></div></div>'
 h+='<link rel=stylesheet href=https://unpkg.com/leaflet@1.9.4/dist/leaflet.css><script src=https://unpkg.com/leaflet@1.9.4/dist/leaflet.js></script><script>var m=L.map("map").setView([-1.3956,36.7562],12);L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(m);L.marker([-1.3956,36.7562]).addTo(m);L.marker([-1.38,36.78]).addTo(m);</script>'
 h+=nav()
 return h

@app.route('/add/<int:pid>')
def add(pid):
 c=session.get('cart',[])
 c.append(pid)
 session['cart']=c
 return redirect('/cart')

@app.route('/cart')
def cart():
 s=css()
 c=session.get('cart',[])
 h='<style>'+s+'</style><div class=top><b style=color:white>CART 28px</b></div>'
 tot=0
 cnt=0
 for pid in c:
  for p in prods:
   if p['id']==pid:
    h+='<div class=card>'+p['name']+' KSh '+str(p['price'])+'</div>'
    tot+=int(p['price'])
    cnt+=1
 h+='<div class=card style=background:#111;color:white><b>TOTAL '+str(cnt)+' pairs KSh '+str(tot)+'</b></div>'
 h+='<div class=card><a href=/ class=btn style=background:#111>Continue</a><a href=/clear class=btn style=background:#ddd;color:#111>Clear</a></div>'+nav()
 return h

@app.route('/clear')
def clear():
 session['cart']=[]
 return redirect('/')

@app.route('/shop/<own>')
def shop(own):
 s=css()
 sn='Rongai'
 for n in shops:
  if shops[n]['own']==own:
   sn=n
 h='
