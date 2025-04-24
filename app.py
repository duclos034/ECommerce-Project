from flask import Flask, render_template, request, url_for, redirect
from time import sleep
import csv
import psycopg2



app = Flask(__name__)


sql1 = '''
        select * from items;
        
       '''

sql2 = '''
        select supnr, supname, supaddress, supcity, supstatus
        from supplier2;
       '''

#functions for reading and writing to csv
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
   loggedin = False
   if request.method == 'POST':
      input_username = request.form['username']
      input_password = request.form['password']
      if input_username == username and input_password == password:
         print("Login success")
         return render_template('main.html')
         loggedin = True
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
   connection =psycopg2.connect("host =localhost port=5432 dbname=postgres user=postgres password=password")
   cur = connection.cursor()
   cur.execute(sql1)
   data=cur.fetchall()
   print("get all", cur.rowcount)

   connection.commit()
   cur.close()
   connection.close()
   if request.method == "POST":
      print("receiving transmission")
      

      return redirect(url_for('itempage', data = data))
      
   
   return render_template('storefront.html', data = data)
   
@app.route("/itempage", methods = ['GET', 'POST'])
def itempage():
   connection =psycopg2.connect("host =localhost port=5432 dbname=postgres user=postgres password=password")
   cur = connection.cursor()

   item_id = request.args.get('item_id', None)
   print(item_id)
   cur.execute("SELECT * FROM items WHERE itemid = %s;", (item_id,))
   data=cur.fetchone()
   print("get item", cur.rowcount)

   connection.commit()
   cur.close()
   connection.close()

   if data:
      return render_template('itempage.html',data = data)
   else:
      return render_template('itempage.html', error = "Item not found")
   
   
   


@app.route("/signup", methods = ['GET', 'POST'])
def signup():
   if request.method == "POST":
      firstname = request.form['firstname']
      lastname = request.form['lastname']
      username = request.form['username']
      password = request.form['password']
      csv_writer([firstname,lastname, username, password])
      print("the data has been received")
      return redirect(url_for('login'))
   return render_template('signup.html')

@app.route("/get")
def database_table():
   connection =psycopg2.connect("host =localhost port=5432 dbname=postgres user=postgres password=password")
   cur = connection.cursor()
   cur.execute(sql1)
   data=cur.fetchall()
   print("get all", cur.rowcount)
   connection.commit()
   cur.close()
   connection.close()
   return render_template('supplier.html', data=data)
   #return render_template('storefront.html', data=data)


@app.route('/insert')
def insert_supplier():
    itemid = request.args.get("itemid",)
    itemname = request.args.get("itemname",)
    description = request.args.get("description",)
    sellername = request.args.get("sellername", )
    price = request.args.get("price", )

    connection =psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password ")
    cur = connection.cursor()
    
    cur.execute("INSERT INTO items(itemid, itemname, description, sellername, price) VALUES(%s,%s,%s,%s,%s);" , (itemid, itemname, description, sellername, price))
    
    connection.commit()
    cur.close()
    connection.close()
    return redirect(url_for('database_table'))

@app.route('/delete/<number>')
def delete_supplier_by_number(number):
    connection =psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password ")
    cur = connection.cursor()
    number_str = str(number)
    cur.execute("DELETE FROM items WHERE itemid = %s;", (number_str,))
    connection.commit()
    connection.close()
    return redirect(url_for('database_table'))
   

