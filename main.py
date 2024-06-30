from flask import *
import mysql.connector
import os
from connect import get_connection
app = Flask(__name__)

get_connection()

cu = mydb.cursor()

cu.execute('drop table if exists all_songs, free_songs, playlists')
cu.execute('CREATE TABLE IF NOT EXISTS users (uid INT PRIMARY KEY AUTO_INCREMENT, email VARCHAR(20), password VARCHAR(20))')
cu.execute('create table if not exists playlists(pid int primary key, playlist_name varchar(20))')
cu.execute('create table if not exists free_songs(sid int primary key auto_increment,name varchar(255),path varchar(255))')
cu.execute('create table if not exists all_songs(sid int primary key auto_increment,name varchar(255),path varchar(255), pid int, foreign key(pid) references playlists(pid) on delete cascade)')


# start when the program runs
@app.route('/')
def free():
    return render_template('free.html')


# scans the songs from folder and store it into table
def scan_free_songs():  
    free_dir = os.path.join(os.getcwd(), 'static', 'songs', 'Free_songs')
    for filename in os.listdir(free_dir):
        if filename.endswith('.mp3'):
            song_name = filename[:-4]
            song_src = f'/static/songs/Free_songs/{filename}'
            cu.execute('insert into free_songs(name,path) values(%s,%s)',(song_name,song_src))
            mydb.commit()
scan_free_songs()

@app.route('/get_freesongs')
def get_freesongs():
    free_songs=[]
    cursor=mydb.cursor(dictionary=True)
    cursor.execute('select name, path as src from free_songs')
    print("Free song retrival - Query executed successfully")
    free_songs=cursor.fetchall()
    return jsonify(free_songs)

def scan_all_songs():
    main_folder = 'static/songs/All_songs'
    index=0
    for folder_name in os.listdir(main_folder):
        if not folder_name.endswith('.txt'):
            index+=1
            cu.execute('insert into playlists(pid, playlist_name) values(%s,%s)',(index,folder_name))
            mydb.commit()
            folder_path = os.path.join(main_folder, folder_name)
            if os.path.isdir(folder_path):
                for filename in os.listdir(folder_path):
                    if filename.endswith('.mp3') or filename.endswith('.wav'):
                        song_name = os.path.splitext(filename)[0]
                        song_src = f'/static/songs/All_songs/{folder_name}/{filename}'
                        cu.execute('insert into all_songs(name,path,pid) values(%s,%s,%s)',(song_name,song_src,index))
                        mydb.commit()
scan_all_songs()

@app.route('/get_allsongs')
def get_allsongs(): 
    all_songs=[]
    cursor=mydb.cursor(dictionary=True)
    cursor.execute('select name, path as src from all_songs')
    all_songs=cursor.fetchall()
    print("All song retrival - Query executed successfully")
    return jsonify(all_songs)

@app.route('/test')
def display_playlists():
    return render_template('listofplaylist.html')



# login function
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cur = mydb.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            return render_template("index.html")
        else:
            return render_template("login.html", alert_message="Credentials do not match")


# sign up function
@app.route('/signup')
def signup_page():
    return render_template('sign-up.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')# fetching details
        password = request.form.get('password')

        c = mydb.cursor()
        c.execute('SELECT * FROM users WHERE email=%s', (email,))# checking if user is available
        existing_user = c.fetchone()

        if existing_user:
            return render_template("index.html", alert_message="User with this email already exists, please login instead")
        else:
            c.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
            mydb.commit()
            return render_template("index.html")


#admin login 
@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin_panel')
def admin_panel():
    return render_template('admin_panel.html')

@app.route('/upload_song', methods=['POST'])
def upload_song():
    uploaded_file = request.files['song']
    playlist = request.form['playlist']
    if uploaded_file:
        destination_folder = os.path.join('static\songs\All_songs', playlist)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        uploaded_file.save(os.path.join(destination_folder, uploaded_file.filename))
        cu.execute('drop table if exists all_songs, free_songs, playlists')
        cu.execute('create table if not exists playlists(pid int primary key, playlist_name varchar(20))')
        cu.execute('create table if not exists free_songs(sid int primary key auto_increment,name varchar(255),path varchar(255))')
        cu.execute('create table if not exists all_songs(sid int primary key auto_increment,name varchar(255),path varchar(255), pid int, foreign key(pid) references playlists(pid) on delete cascade)')
        scan_free_songs()
        scan_all_songs()
        return 'File uploaded successfully'
    else:
        return 'No file uploaded'

@app.route('/admin_login',methods=['POST'])
def admin_login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    cu.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    admin = cu.fetchone()
    if admin and email=='admin@dbms' and password=='dbms' :
        return render_template('admin_panel.html')
    else:
        return render_template('admin_login.html', alert_message="Invalid credentials")
    
@app.route('/fetch_playlists')
def fetch_playlists():
    playlists = []
    cursor = mydb.cursor(dictionary=True)
    cursor.execute('SELECT * FROM playlists')
    playlists = cursor.fetchall()
    return jsonify(playlists)

@app.route('/remove/<int:index>', methods=['DELETE'])
def remove_playlist(index):
    print(index)
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM playlists WHERE pid=%s", (index,))
    mydb.commit()
    return fetch_playlists()



@app.route('/search/<searched_song>')
def search_songs(searched_song):
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM all_songs WHERE name = "'%'+searched_song+'%'"")
        songs = cursor.fetchall()
        return jsonify(songs)
    except mysql.connector.Error as err:
        print("Error fetching songs:", err)
        return jsonify([]), 500


@app.route('/playlist.html')
def playlist():
    return render_template('playlist.html')
@app.route('/playlist')
def playlists():
    return render_template('playlist.html')

@app.route('/fetch_songs/<playlist_id>')
def fetch_songs(playlist_id):
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM all_songs WHERE pid = %s", (playlist_id,))
        songs = cursor.fetchall()
        return jsonify(songs)
    except mysql.connector.Error as err:
        print("Error fetching songs:", err)
        return jsonify([]), 500

if __name__ == '__main__':
    app.run(debug=True)
