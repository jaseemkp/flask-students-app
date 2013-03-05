import sqlite3
from flask import Flask, render_template, request, url_for, redirect, \
                  Response

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main.html')
@app.route('/details', methods = ['POST', 'GET'])
def details():
    if request.method == 'GET':
        return render_template('details.html')
    if request.method == 'POST':
        name=request.form['studentname']
        sex = request.form['sex']
        age = request.form['age']
        mark = request.form['mark']
        
        data = (name, sex, age, mark)
        
        con = sqlite3.connect('students.db')
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS student(name text, sex text, age text, mark text)")
        cur.execute("INSERT INTO student VALUES(?, ?, ?, ?)", data)
        con.commit()
        con.close()
        return redirect(url_for('main_page'))	
@app.route('/view', methods=['POST', 'GET'])
def view():
    if request.method == 'GET':
        con = sqlite3.connect('students.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM student")
        
        rows = cur.fetchall()
        entries = [dict(name=row[0], sex=row[1], age=row[2], mark=row[3]) for row in rows]
        return render_template('show.html', entries=entries)

@app.route('/sort_age', methods=['POST', 'GET'])
def sort_age():
    if request.method == 'GET':
        con = sqlite3.connect('students.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM student ORDER by age ASC")
        rows = cur.fetchall()
        entries = [dict(name=row[0], sex=row[1], age=row[2], mark=row[3]) for row in rows]
        return render_template('show.html', entries=entries)

@app.route('/sort_mark', methods = ['GET', 'POST'])
def sort_mark():
    if request.method == 'GET':
        con =  sqlite3.connect('students.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM student ORDER by mark DESC")
        rows = cur.fetchall()
        entries = [dict(name=row[0], sex=row[1], age=row[2], mark=row[3]) for row in rows]
        return render_template('show.html', entries=entries)

@app.route('/remove', methods=['POST', 'GET'])
def remove_details():
    if request.method == 'GET':
        return render_template('remove.html')
  
    if request.method == 'POST':
        remove = request.form['remove']
	con = sqlite3.connect('students.db')
        cur = con.cursor()
        cur.execute("DELETE FROM student WHERE name=:name", {'name': remove})
        con.commit()
        con.close()
        resp = Response("""<html>
			   <link rel="stylesheet" type="text/css" href="/static/style.css" />
                           <div class=metanav>
                           <p><a href="/">Home</a></p>
			   </div>
			   <body>
                           <div><h2><center>"""+remove+"""'s details removed...!</center></h2></div>
                           </body></html>""", status=200, mimetype='html')  
        return resp
        
@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    if request.method == 'POST':
        search= request.form['search']
        con = sqlite3.connect('students.db')   
        cur = con.cursor()
        cur.execute("SELECT * FROM student WHERE name=:name", {"name": search})
        rows =cur.fetchall()
        entries = [dict(name=row[0], sex=row[1], age=row[2], mark=row[3]) for row in rows]
        return render_template('show.html', entries=entries)

if __name__ == '__main__':
    app.debug = True
    app.run()
    
