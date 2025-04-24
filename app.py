from flask import Flask, render_template, request, url_for, redirect, session
from time import sleep
import psycopg2
from werkzeug.utils import secure_filename
import os
import random

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' ])
#We must buildthe fish of the day page



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'poggers'


sql1 = '''
        select * from items;
        
       '''

sql2 = '''
        select supnr, supname, supaddress, supcity, supstatus
        from supplier2;
       '''
sql3 = '''
        SELECT * FROM items
        ORDER BY itemid DESC
        LIMIT 5;
       '''
sql4 = '''
        Select * from items
        ORDER BY item_category;
      '''
sql5 = '''
         SELECT * FROM items
         ORDER BY price;
      '''

def allowed_file(filename):
   return '.' in filename and \
      filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.context_processor
def inject_audio_files():
    # Define audio files and labels
    audio_files = {
        "intro.wav": "What are you?",
        "login.wav": "How to Use the Website"
    }
    wav_file = None
    return dict(audio_files=audio_files, wav_file=wav_file)




   

   

#show site information, recomendations etc in this page
#This is will be used as the primary directory for all other pages in the future
#seacrhbar
@app.route("/main", methods =['GET', 'POST'])
def main_page():
   print(request.method)

   if request.method == 'POST':
      if request.form.get('Open Coconut') == 'Open Coconut':
         print("button pressed, congrats")
         return render_template('coconut.html')
   
   elif request.method == 'GET':
      print("")

   connection =psycopg2.connect("host =localhost port=5432 dbname=postgres user=postgres password=password")
   cur = connection.cursor()
   cur.execute(sql3)
   data=cur.fetchall()
   print("get all", cur.rowcount)

   connection.commit()
   cur.close()
   connection.close()
   if request.method == "POST":
      print("receiving transmission")
      

      return redirect(url_for('itempage', data = data))
      
   
   return render_template('main.html', data = data)

   


   #return render_template('main.html')



#Needs to be connected to the database
@app.route("/login",methods = ['GET','POST'])
def login():
   if request.method == 'POST':
      input_username = request.form['username']
      input_password = request.form['password']
      

      connection = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password")
      cur = connection.cursor()

      cur.execute("SELECT userid FROM userbase WHERE username = %s AND password = %s;", (input_username, input_password))
      user = cur.fetchone()

      cur.close()
      connection.close()


      if user:
         print("User recognized")
         session['userid'] = user[0]
        
        
        
         
         return redirect(url_for('main_page'))
      else:
         print("WRONG")
         return render_template('login.html', error="Invalid")

   return render_template('Login.html')




@app.route("/",methods = ['GET', 'POST'])
def welcome():
   return render_template('welcome.html')



@app.route("/coconut", methods = ['GET', 'POST'])
def squid_page():
  # image_url = 'C:\Users\duclo\Downloads\ECommerce Project\coconut.jpg'
   return render_template('coconut.html')


@app.route("/profile", methods =['GET', 'POST'])
def profile_page():
   return render_template('profile.html')


   

@app.route('/storefront', methods = ['GET', 'POST'])
def storefront():
   
  
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

@app.route('/categorySort', methods = ['GET', 'POST'])
def categorySort():
  
   connection =psycopg2.connect("host =localhost port=5432 dbname=postgres user=postgres password=password")
   cur = connection.cursor()
   cur.execute(sql4)
   data=cur.fetchall()
   return render_template('storefront.html',data=data)


@app.route('/priceSort', methods = ['GET', 'POST'])
def priceSort():
  
   connection =psycopg2.connect("host =localhost port=5432 dbname=postgres user=postgres password=password")
   cur = connection.cursor()
   cur.execute(sql5)
   data=cur.fetchall()
   return render_template('storefront.html',data=data)

   


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
   #pleases remember this was changed to the temp file
   if data:
      return render_template('itempage.html',data = data)
   else:
      return render_template('itempage.html', error = "Item not found")
      
#In progress
@app.route("/cart", methods=['POST', 'GET'])
def cart():
   userid = session.get('userid')
  
   
   connection = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password")
   cur = connection.cursor()
   cur.execute("SELECT * FROM shoppingcart WHERE userid = %s;", (userid,))
   cart_items = cur.fetchall()
   
   connection.commit()
   cur.close()
   connection.close()
   return render_template('cart.html', cart_items=cart_items)

   
@app.route("/add_to_cart", methods=['POST'])
def add_to_cart():
   userid = session.get('userid')
   

   
   item_id = request.form['item_id']
   item_name = request.form['item_name']
   description = request.form['description']
   price = request.form['price']

   connection = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password")
   cur = connection.cursor()

   cur.execute("INSERT INTO shoppingcart (cartitemid,itemname,description,price, userid) VALUES (%s, %s, %s, %s, %s);",
               (item_id,item_name,description,price,userid))

   
   connection.commit()
   cur.close()
   connection.close()

   print("send to the elephant")
   return redirect(url_for('itempage',item_id=item_id))



@app.route("/checkout", methods = ['GET', 'POST'])
def checkout():
   connection = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password")
   cur = connection.cursor()
   cur.execute("SELECT * FROM shoppingcart")
   cart_items = cur.fetchall()
   connection.commit()
   cur.close()
   connection.close()
   
  
   return render_template('checkout.html', cart_items = cart_items)

@app.route("/purchase", methods = ['GET', 'POST'] )
def purchase():
   userid = session.get('userid')
   connection = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password")
   cur = connection.cursor()
   cur.execute("SELECT cartitemid, itemname, description, price FROM shoppingcart WHERE userid = %s;", (userid,))
   cart_items = cur.fetchall()

   for item in cart_items:
      cur.execute("""
            INSERT INTO purchasehistory (cartitemid, itemname, description, price, userid)
            VALUES (%s, %s, %s, %s, %s);
        """, (item[0], item[1], item[2], item[3], userid))


   cur.execute("DELETE FROM shoppingcart WHERE userid = %s", (userid,))
   connection.commit()
   cur.close()
   connection.close()
   return render_template('checkout.html')

@app.route("/purchase_history", methods = ["GET", "POST"])
def purchase_history():
   userid = session.get('userid')
   connection = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password")
   cur = connection.cursor()
   cur.execute("SELECT * FROM purchasehistory WHERE userid = %s;", (userid,))
   purchase_history = cur.fetchall()
   connection.commit()
   cur.close()
   connection.close()
   return render_template('purchasehistory.html', history = purchase_history)
   


#Needs to be connected to database
@app.route("/signup", methods = ['GET', 'POST'])
def signup():
   if request.method == "POST":
      firstname = request.form['firstname']
      lastname = request.form['lastname']
      username = request.form['username']
      password = request.form['password']
      
      connection = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password")
      cur = connection.cursor()

      cur.execute("INSERT INTO userbase (firstname,lastname,username,password) VALUES (%s, %s, %s, %s);",
                  (firstname, lastname,username,password))
      print("Send to the elephant")

      connection.commit()
      cur.close()
      connection.close()

      return redirect(url_for('login'))
   return render_template('signup.html')

@app.route("/itemsubmission", methods=['GET', 'POST'])
def itemsubmission():
   if request.method == "POST":
      itemname = request.form['itemname']
      #image handling
      if 'file' not in request.files:
         print('No file part')
         return redirect(request.url)
      file = request.files['file']
      if file.filename == '':
         print('No selected file')
         return redirect(request.url)
      if file and allowed_file(file.filename):
         file_extension = os.path.splitext(file.filename)[1]
         filename = secure_filename(f"{itemname}{file_extension}")
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         #return redirect(url_for('main_page', name=filename))
     
         itemname = request.form['itemname']
         description = request.form['description']
         sellername = request.form['sellername']
         price = request.form['price']
         quantity = request.form['quantity']
         condition = request.form['condition']
         category = request.form['category']  # Retrieve the category from the form
         
         connection = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password")
         cur = connection.cursor()

         cur.execute("INSERT INTO items (itemid, itemname, description, sellername, price, quantity, condition, image, item_category ) VALUES (DEFAULT, %s, %s, %s, %s, %s,%s, %s, %s);",
                     (itemname, description, sellername, price, quantity, condition, filename, category))
         print("Elephant has received")
      
         connection.commit()
         cur.close()
         connection.close()
         return redirect(url_for('main_page', name=filename))
   return render_template('itemsubmission.html')




@app.route("/search", methods=["GET"])
def search():
   query = request.args.get("query")
   if not query:
        return render_template("itempage.html", error="No search term provided.")

   print(query)

   connection =psycopg2.connect("host =localhost port=5432 dbname=postgres user=postgres password=password")
   cur = connection.cursor()
   cur.execute("SELECT * FROM items WHERE itemname ILIKE %s;", (f"%{query}%",))
  
   data=cur.fetchone()
   print("get item", cur.rowcount)

   connection.commit()
   cur.close()
   connection.close()

   if data:
      return render_template('itempage.html',data = data)
   else:
      return render_template('itempage.html', error = "Item not found")
  

@app.route("/dailyfish", methods = ["GET", "POST"])
def daily_fish():
   fish_images = {
        "Bass": "Bass.jpg",
        "GreatWhite": "GreatWhite.jpg",
        "feesh": 'lame.gif',
        "angryFish":'screaming-fish.gif',
        "squid":"squid.jpg",
        "anomalocaris": "anomalocaris.jpg",
        
        "Sockeye Salmon": "Sockeye Salmon.jpg"
    }
   fish_facts = {
        "Bass": "Bass are a diverse group of fish, including freshwater species like largemouth and smallmouth bass, as well as saltwater species like striped bass and sea bass. They are known for being aggressive predators and are highly sought-after sport fish. Bass have a wide range of interesting characteristics, including their intelligence, unique sensory abilities, and spawning behaviors. ",
        "GreatWhite": "The great white shark (Carcharodon carcharias), also known as the white shark, white pointer, or simply great white, is a species of large mackerel shark which can be found in the coastal surface waters of all the major oceans. It is the only known surviving species of its genus Carcharodon. The great white shark is notable for its size, with the largest preserved female specimen measuring 5.83 m (19.1 ft) in length and around 2,000 kg (4,400 lb) in weight at maturity.[3] However, most are smaller; males measure 3.4 to 4.0 m (11 to 13 ft), and females measure 4.6 to 4.9 m (15 to 16 ft) on average.[4][5] According to a 2014 study, the lifespan of great white sharks is estimated to be as long as 70 years or more, well above previous estimates,[6] making it one of the longest lived cartilaginous fishes currently known.[7] According to the same study, male great white sharks take 26 years to reach sexual maturity, while the females take 33 years to be ready to produce offspring.[8] Great white sharks can swim at speeds of 25 km/h (16 mph)[9] for short bursts and to depths of 1,200 m (3,900 ft).[10]",
        "feesh": 'This fish does not understand Forward Propogation.',
        "angryFish":'Hes angry',
        "squid":"A squid (pl.: squid) is a mollusc with an elongated soft body, large eyes, eight arms, and two tentacles in the orders Myopsida, Oegopsida, and Bathyteuthida (though many other molluscs within the broader Neocoleoidea are also called squid despite not strictly fitting these criteria). Like all other cephalopods, squid have a distinct head, bilateral symmetry, and a mantle. They are mainly soft-bodied, like octopuses, but have a small internal skeleton in the form of a rod-like gladius or pen, made of chitin. ",
        "anomalocaris": "Anomalocaris was a giant, shrimp-like creature that lived during the Early Cambrian period, considered one of the first apex predators. It had large, compound eyes on stalks and unique mouthparts for crushing prey. The fossils of Anomalocaris are primarily found in the Burgess Shale and Emu Bay Shale. ",

        "Sockeye Salmon" : "Sockeye salmon are a species of Pacific salmon, known for their vibrant orange-red flesh and their long migration from the ocean back to freshwater rivers to spawn. They are anadromous, meaning they live in both salt and freshwater. During spawning season, sockeye salmon undergo dramatic physical changes, including turning red and developing hooked jaws. "
   }

   random_fish = random.choice(list(fish_images.items()))
   fish_title = random_fish[0]
   fish_image = random_fish[1]
   random_fact = fish_facts[fish_title]
   return render_template("dailyfish.html", fish_title=fish_title, fish_image=fish_image, fish_fact=random_fact)
     

@app.route("/adminlogin" ,methods = ["GET", "POST"])
def adminlogin():
    if request.method == 'POST':
      input_adminname = request.form['adminname']
      input_password = request.form['password']
      

      connection = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password")
      cur = connection.cursor()

      cur.execute("SELECT adminid FROM admin WHERE adminname = %s AND password = %s;", (input_adminname, input_password))
      admin = cur.fetchone()

      cur.close()
      connection.close()


      if admin:
         print("User recognized")
         session['adminid'] = admin[0]  # Store admin ID in the session
         return redirect(url_for('admin'))
      else:
         print("WRONG")
         return render_template('adminlogin.html', error="Invalid")
    return render_template('adminlogin.html')

      


@app.route("/admin", methods = ["GET", "POST"])
def admin():
   
   connection =psycopg2.connect("host =localhost port=5432 dbname=postgres user=postgres password=password")
   cur = connection.cursor()
   cur.execute(sql1)
   data=cur.fetchall()
   cur.execute("SELECT * FROM USERBASE")
   user = cur.fetchall()
   connection.commit()
   cur.close()
   connection.close()
   return render_template('admin.html', data = data, users = user)



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
   return render_template('admin.html', data=data)
   #return render_template('storefront.html', data=data)



@app.route('/insert')
def insert_supplier():
    itemid = "null"
    itemname = request.args.get("itemname",)
    description = request.args.get("description",)
    sellername = request.args.get("sellername", )
    price = request.args.get("price", )
    quantity = request.args.get("quantity",)
    condition = request.args.get("condition",)
    item_category= request.args.get("item_category",)
    
    connection =psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password ")
    cur = connection.cursor()
    
    cur.execute("INSERT INTO items (itemid, itemname, description, sellername, price, quantity, condition, image) VALUES (DEFAULT, %s, %s, %s, %s, %s,%s, %s);",
                     (itemname, description, sellername, price, quantity, condition, item_category))
    connection.commit()
    cur.close()
    connection.close()
    return redirect(url_for('admin'))



@app.route('/delete/<number>')
def delete_supplier_by_number(number):
    connection =psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password ")
    cur = connection.cursor()
    number_str = str(number)
    cur.execute("DELETE FROM items WHERE itemid = %s;", (number_str,))
    connection.commit()
    connection.close()
    return redirect(url_for('admin'))

@app.route('/userdelete/<number>')
def delete_user_by_number(number):
    connection =psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password ")
    cur = connection.cursor()
    number_str = str(number)
    cur.execute("DELETE FROM userbase WHERE userid = %s;", (number_str,))
    connection.commit()
    connection.close()
    return redirect(url_for('admin'))
   





