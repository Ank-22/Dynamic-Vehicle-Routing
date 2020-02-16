from flask import Flask,render_template, redirect, url_for, request
from Barcode_Genrator import GenrateBarcode_ID as GBI
import pandas as pd
import jinja2
app = Flask(__name__, static_url_path="/static")
import Main_Backend as DP 

global var1
global var2

@app.route("/")
def loading():

    return redirect(url_for('hello'))

@app.route("/VRP")
def VRP():

    return render_template("VRP.html")

@app.route('/processvrp', methods=['POST'])
def process():
   global var1
   global var2
   if request.method == 'POST':
      var1,var2=DP.Call_Depopackage()
      data=pd.read_csv('./data_3.csv',dtype={'Address':'str','lng': 'str','lat': 'str'})
      data=data.filter(["Address",'lat','lng'])
      data=data.dropna(axis=0)
      return render_template("Display.HTMl",data=var1,data2=data )
        
@app.route('/processap', methods=['POST'])
def processap():
   global var1
   global var2
   if request.method == 'POST':
      Depo = request.form['depo']
      var3,var4=DP.Call_Addpackage(Depo,var1,var2)
      data=pd.read_csv('./data_3.csv',dtype={'Address':'str','lng': 'str','lat': 'str'})
      data=data.filter(["Address",'lat','lng'])
      data=data.dropna(axis=0)
      return render_template("AddPackage.HTMl",data=var4,AgentNo=var3,data2=data)        

@app.route("/home-page")
def hello():
    return render_template("Home-page.html")

@app.route('/process',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      Name = request.form['Name']
      Address=request.form['Full Address']
      GBI(Name,Address)
      return redirect(url_for('success',name = Name,address=Address))
   else:
      Name= request.args.get('Name')
      Address= request.args.get('Address')
      GBI(Name,Address)
      return redirect(url_for('success',name = Name,address=Address))

@app.route("/success/<name>/<address>")
def success(name,address):
   return render_template("Submit.HTML",name=name,add=address)


# print(data.head())


@app.route("/Address")
def Address():
   data=pd.read_csv('./MainData.csv',dtype={'Address':'str', 'BarcodeID': 'str'})
   data=data.filter(["Address","BarcodeID"])
   data=data.dropna(axis=0)
   barcode=data.filter(["BarcodeID"]) 

   barcode['BarcodeID'] = '/static/Barcode/' + barcode['BarcodeID']+'.png.png'
   items = []
   for i in range(len(data)):
      varToSend = dict(Address=data['Address'].iloc[i], BarcodeID=data['BarcodeID'].iloc[i],Barcodeimg=barcode['BarcodeID'].iloc[i])
      items.append(varToSend)
   return render_template("Address.html", data=items)
   


if __name__ == "__main__":
    app.run(debug=True)

