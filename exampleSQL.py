from flask import Flask, render_template, request, url_for, redirect
import psycopg2

app = Flask(__name__)

sql1 = '''
        select supnr, supname, supaddress, supcity, supstatus
        from supplier2;
       '''
sql2 = '''
        select supnr, supname, supcity, supstatus
        from supplier2
        where supname = %s;
       '''
sql3 = '''
        insert into supplier2(supnr, supname, supcity, supstatus)
        values (%s, %s, %s, %s, %s);
        '''
sql4 = '''
        select prodnr, prodname, prodtype, available_quantity
        from product;
       '''

@app.route('/hello/<name>')
def hello_world(name=None):
    return render_template("hello.html", name=name)

@app.route('/')
def get_all_suppliers():
    connection =psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password ")
    cur = connection.cursor()
    cur.execute(sql1)
    data = cur.fetchall()
    print("get all", cur.rowcount)
    connection.commit()
    cur.close()
    connection.close()
    return render_template("suppliers.html", data=data)

@app.route('/get')
def get_supplier_by_name():
    supname = request.args.get("supname", "")
    connection =psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password")
    cur = connection.cursor()
    cur.execute(sql2, (supname,))
    print("get by name:", cur.rowcount)
    data = cur.fetchone()
    connection.commit()
    cur.close()
    connection.close()
    return render_template("supplier.html", data=data, supname=supname)



@app.route('/delete/<number>')
def delete_all_suppliers(number):
    connection = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password ")
    cur = connection.cursor()
    #cur.execute('select delete_all_suppliers()')
    cur.execute('CALL delete_supplier_by_number(%s, %s)', (number, None))
    data = cur.fetchone()[0]
    print("DELETED " + str(data) + " ROWS!" )
    connection.commit()
    cur.close()
    connection.close()
    return redirect(url_for('get_all_suppliers'))


@app.route('/insert')
def insert_supplier():
    supnr = request.args.get("supnr",)
    supname = request.args.get("supname",)
    supaddress = request.args.get("supaddress",)
    supcity = request.args.get("supcity", )
    supstatus = request.args.get("supstatus", )

    connection =psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password ")
    cur = connection.cursor()
    
    cur.execute("INSERT INTO supplier2(supnr, supname, supaddress, supcity, supstatus) VALUES(%s,%s,%s,%s,%s);" , (supnr, supname, supaddress, supcity, supstatus))
    
    connection.commit()
    cur.close()
    connection.close()
    return redirect(url_for('get_all_suppliers'))







@app.route('/delete/<number>')
def delete_supplier_by_number(number):
    connection =psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password ")
    cur = connection.cursor()
    number_str = str(number)
    cur.execute("DELETE FROM supplier2 WHERE supnr = %s;", (number_str,))
    connection.commit()
    connection.close()
    #return redirect(url for('get_suppliers')

@app.route('/products')
def get_all_products():
    connection =psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=password ")
    cur = connection.cursor()
    cur.execute(sql4)
    data = cur.fetchall()
    print("get all", cur.rowcount)
    connection.commit()
    cur.close()
    connection.close()
    return render_template("products.html", data=data)


