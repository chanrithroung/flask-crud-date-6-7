from flask import Flask, render_template, request, redirect
import psycopg2
import password
app = Flask(__name__)

DB_HOST = "127.0.0.1" # or localhost
DB_NAME = "flask_6_7"
DB_USER = "postgres"
DB_PASSWORD = password.password

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/")
def index():    
    return redirect("/create")

@app.route("/create")
def create():
    return render_template("create.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    email = request.form['email']

    qeury = f""" INSERT INTO users(first_name, last_name, email) 
        VALUES ('{first_name}', '{last_name}', '{email}');
    """
    con = get_db_connection()
    cusor = con.cursor()
    cusor.execute(qeury)
    con.commit()
    cusor.close()
    con.close()
    return redirect("/create")


@app.route("/list-users")
def list_user():
    con = get_db_connection()
    cursor = con.cursor()
    query = "SELECT * FROM users ORDER BY ID DESC"
    cursor.execute(query=query)
    users = cursor.fetchall()
    return render_template('list_user.html', users=users)



@app.route("/update/<id>")
def update(id):
    
    query = f""" 
        SELECT * FROM users WHERE id = {id};
    """

    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute(query=query)
    user = cursor.fetchall()

    return render_template("update.html", user=user[0])


@app.route("/update-submit", methods=["GET", "POST"])
def update_submit():
    id = request.form['id']
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    emial = request.form['email']


    query = f"""
        UPDATE users SET first_name = '{first_name}', 
                last_name = '{last_name}',
                email = '{emial}' WHERE id = {id};
    """
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute( query=query )
    
    con.commit()
    cursor.close()
    con.close()

    return redirect("/list-users")

    # return f"username = {first_name}, last_name = {last_name}, email = {emial}"


# Delete use 
@app.route("/delete-user", methods=["GET", "POST"])
def delete_user():
    id = request.form['remove-id']

    query = f"""
        DELETE FROM users WHERE id = {id};
    """

    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute(query=query)
    con.commit()

    return redirect("list-users")

if __name__ == "__main__":
    app.run(debug=True)