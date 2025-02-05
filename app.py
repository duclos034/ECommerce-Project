from flask import Flask, render_template, request, url_for, redirect
import csv

app = Flask(__name__)

def csv_writer(users):
   with open('users.csv', mode='a') as file:
      writer = csv.writer(file)
      writer.writerow(users)

def csv_reader(items):
   data = []
   with open(items,mode = 'r') as file:
      reader = csv.reader(file)
      for row in reader:
         data.append(row)
      return data
#show site information, recomendations etc in this page
#This is will be used as the primary directory for all other pages in the future
#seacrhbar
@app.route("/", methods =['GET', 'POST'])
def main_page():
   print(request.method)

   if request.method == 'POST':
      if request.form.get('Open Coconut') == 'Open Coconut':
         print("button pressed, congrats")
         return redirect(url_for('squid_page'))
   
   

   elif request.method == 'GET':
      print("")


   return render_template('main.html')

@app.route("/login",methods = ['GET','POST'])
def login():
   username = "admin"
   password = "password"
   if request.method == 'POST':
      input_username = request.form['username']
      input_password = request.form['password']
      if input_username == username and input_password == password:
         print("Login success")
         return render_template('main.html')
      else:
         print("WRONG")
         return render_template('squid.html', error="Invalid credentials")
   
   return render_template('Login.html')

@app.route("/squid_page", methods = ['GET', 'POST'])
def squid_page():
  # image_url = 'C:\Users\duclo\Downloads\ECommerce Project\coconut.jpg'
   return render_template('coconut.html')


   

@app.route('/storefront', methods = ['GET', 'POST'])
def storefront():
   #need database to fill in the information
   #have button redirect to store page, using the index values of the button to plug in the item values
   items = csv_reader('items.csv')
   if request.method == "POST":
      print("receiving transmission")
      item_id = request.form.get('item_id')
      
      print({item_id})
      return redirect(url_for('itempage', item_id = item_id))
      
   items = csv_reader('items.csv')
   return render_template('storefront.html', items = items)
   
@app.route("/itempage", methods = ['GET', 'POST'])
def itempage():
   item_id = request.args.get('item_id', None)
   items = csv_reader('items.csv')
   for item in items:
      if item[0] == item_id:
         val = item
   
   return render_template('itempage.html', item = val )


@app.route("/signup", methods = ['GET', 'POST'])
def signup():
   if request.method == "POST":
      username = request.form['username']
      password = request.form['password']
      csv_writer([username, password])
      print("the data has been received")
      return redirect(url_for('login'))
   return render_template('signup.html')

