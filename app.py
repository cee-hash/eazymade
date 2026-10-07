from flask import Flask,request,redirect,session
import os
app=Flask(__name__)
app.secret_key="v33"

shops={"Rongai":{"own":"admin","ok":True},"Kit":{"own":"kiten","ok":True}}
prods=[{"id":1,"name":"Jordan 1","price":4500,"shop":"Rongai"},{"id":2,"name":"Air Max","price":3800,"shop":"Kit"}]

def css():
 a="body{margin:0;background:#f5f5f5;padding-bottom:120px;font-size:28px}"
 b=".top{background:#f68b1e;padding:16px}"
 c=".card{background:white;border-radius:18px;padding:20px;margin:12px}"
 d=".btn{display:block;padding:20px;background:#f68b1e;color:white;text-align:center;border-radius:14px;text-decoration:none;margin-top:10px;font-weight:bold}"
 e=".bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:12px;border-top:4px solid #f68b1e}"
 return a+b+c+d+e

def nav():
 c=len(session.get("cart",[]))
 t="("+str(c)+")" if c>0 else ""
 return "<div class=bottom><a href=/>Market</a><a href=/cart>Cart "+t+"</a><a href=/ai>AI</a></div>"

@app.route("/")
def home():
 s=css()
 h="<style>"+s+"</style>"
 h+="<div class=top><b style=color:white;font-size:32px>EAZYMADE 28px</b></div>"
 h+="<div class=card><b style=font-size:32px>All Shops BIG FONT</b><p>Micro code - phone safe</p></div>"
 for n in shops:
  h+="<div class=card><b style=font-size:30px>"+n+"</b><a href=/shop/"+shops[n]["own"]+" class=btn>Enter Shop WORKS</a></div>"
 for p in prods:
  h+="<div class=card>"+p["name"]+" KSh "+str(p["price"])+"<a href=/add/"+str(p["id"])+" class=btn>Add to Cart WORKS</a></div>"
 h+=nav()
 return h

@app.route("/add/<int:pid>")
def add(pid):
 c=session.get("cart",[])
 c.append(pid)
 session["cart"]=c
 return redirect("/cart")

@app.route("/cart")
def cart():
 s=css()
 c=session.get("cart",[])
 h="<style>"+s+"</style><div class=top><b style=color:white>CART 28px</b></div>"
 tot=0
 cnt=0
 for pid in c:
  for p in prods:
   if p["id"]==pid:
    h+="<div class=card>"+p["name"]+" KSh "+str(p["price"])+"</div>"
    tot+=p["price"]
    cnt+=1
 h+="<div class=card style=background:#111;color:white><b>TOTAL "+str(cnt)+" pairs KSh "+str(tot)+"</b></div>"
 h+="<div class=card><a href=/ class=btn style=background:#111>Continue Shopping WORKS</a></div>"
 h+=nav()
 return h

@app.route("/shop/<own>")
def shop(own):
 s=css()
 sn="Rongai"
 for n in shops:
  if shops[n]["own"]==own:
   sn=n
 h="<style>"+s+"</style><div class=top><b style=color:white>"+sn+"</b></div>"
 h+="<div class=card><b>"+sn+" Whole Shop</b></div>"
 for p in prods:
  if p["shop"]==sn:
   h+="<div class=card>"+p["name"]+"<a href=/add/"+str(p["id"])+" class=btn>Add to Cart</a></div>"
 h+=nav()
 return h

@app.route("/ai",methods=["GET","POST"])
def ai():
 s=css()
 ans=""
 if request.method=="POST":
  q=request.form.get("q","").lower()
  if "jordan" in q:
   ans="Jordan 1 KSh 4500 Rongai"
  else:
   ans="Air Max KSh 3800 Kitengela"
 h="<style>"+s+"</style><div class=top><b style=color:white>AI 28px</b></div>"
 h+="<div class=card><form method=post><input name=q placeholder=jordan style=width:100%;padding:18px;font-size:24px><button class=btn style=border:none;width:100%>Ask AI WORKS</button></form></div>"
 if ans!="":
  h+="<div class=card><b style=font-size:28px>"+ans+"</b></div>"
 h+=nav()
 return h

@app.route("/office",methods=["GET","POST"])
def office():
 s=css()
 if request.method=="POST":
  if request.form.get("password")=="0116782556":
   session["off"]=True
 if not session.get("off"):
  return "<style>"+s+"</style><div class=card><form method=post><input name=password type=password placeholder=0116782556 style=width:100%;padding:18px><button class=btn style=border:none;background:#111>Enter</button></form></div>"+nav()
 return "<style>"+s+"</style><div class=card><b>Office OK</b></div>"+nav()

if __name__=="__main__":
 app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
