import os
from flask import Flask, request, session, redirect, url_for, render_template, send_file
import logging
import zipfile 
import datetime
import subprocess 

app = Flask(__name__)
app.secret_key = os.urandom(16)
username:str
logging.basicConfig(filename='WebHome.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('/etc/shadow') as f:
            shadow_content = f.readlines()
        for line in shadow_content:
            user_info = line.split(':')
            if user_info[0] == username:
                if username == 'khiatihouda':
                    if password == 'houda09122002':
                        session['username'] = username
                        logging.info(f"User {username} logged in.")
                        return redirect('/home')
                elif username == 'guess':
                    if password == '1234abcd':
                        session['username'] = username
                        logging.info(f"User {username} logged in.")
                        return redirect('/home')
                logging.warning(f"Echec de la tentative de connexion pour l'utilisateur {username}")
                session.pop('username', None)  # Supprimer les informations d'identification de la session
                return "Nom d'utilisateur et/ou mot de passe incorrect."
        logging.warning(f"Echec de la tentative de connexion pour l'utilisateur {username}")
        session.pop('username', None)  # Supprimer les informations d'identification de la session
        return "Nom d'utilisateur et/ou mot de passe incorrect."
    return render_template('login.html')

'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('/etc/shadow') as f:
            shadow_content = f.readlines()
        for line in shadow_content:
            user_info = line.split(':')
            if user_info[0] == username:
                if username == 'khiatihouda':
                    if password == 'houda09122002':
                        session['username'] = username
                        logging.info(f"User {username} logged in.")
                        return redirect('/home')
                    elif username == 'guess':
                        if password == '1234abcd':
                            session['username'] = username
                        logging.info(f"User {username} logged in.")
                        return redirect('/home')
            else:
                logging.warning(f"Echec de la tentative de connexion pour l'utilisateur {username}")
                return "Username Password invalid"
       
                password = password.encode('utf-8')
        hashed_password = hashed_password.encode('utf-8')
        if hashlib.sha512(password).hexdigest() == hashed_password.decode('utf-8'):
            session['username'] = username
            logging.info(f"User {username} logged in.")
            return redirect(url_for('index'))
        else:
            logging.warning(f"Echec de la tentative de connexion pour l'utilisateur {username}")
            return "Username Password invalid"
       

    
    return render_template('login.html')


 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
                
        if username == 'khiatihouda':
            if password == 'houda09122002':
                session['username'] = username
                logging.info(f"User {username} logged in.")
                return redirect('/home')
        elif username == 'guess':
            if password == '1234abcd':
                session['username'] = username
                logging.info(f"User {username} logged in.")
                return redirect('/home')
        logging.warning(f"Echec de la tentative de connexion pour l'utilisateur {username}")
        session.pop('username', None)  # Supprimer les informations d'identification de la session
        return "Nom d'utilisateur et/ou mot de passe incorrect."
    return render_template('login.html')
'''
@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        path = os.path.expanduser('~'+username)
        files = []
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            file_size = os.path.getsize(file_path)
            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            files.append((file_name, mod_time, file_size))
        return render_template('home.html', files=files)
    else:
        return redirect('/')


@app.route('/files')
def files():
    if 'username'  in session:   
        home_dir = f"/home/{session['username']}"
        num_files = len([f for f in os.listdir(home_dir) if os.path.isfile(os.path.join(home_dir, f))])

        return f"{session['username']} Nombre de fichiers dans votre répertoire personnel : {num_files}"
    else:
        return redirect(url_for('login'))


@app.route('/dirs')
def dirs():
    if 'username' in session:
        home_dir = f"/home/{session['username']}"
        num_dirs = len([f for f in os.listdir(home_dir) if os.path.isdir(os.path.join(home_dir, f))])
        
        return f"{session['username']} Nombre de répertoires dans votre répertoire personnel : {num_dirs}"
    else:
        return redirect(url_for('login'))



@app.route('/space')
def space():
    if 'username' in session:
        home_dir = f"/home/{session['username']}"
        
        # utiliser la commande système 'du' pour obtenir la taille totale du répertoire personnel
        process = subprocess.Popen(['du','-sh', home_dir], stdout=subprocess.PIPE)
        output, error = process.communicate()
        total_size = output.decode('utf-8').split()[0]
        
        return f" La taille de l'espace occupé par {session['username']} est : {total_size}"
    else:
        return redirect(url_for('login'))
      
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' in session:
        if request.method == 'POST':
            search_type = request.form['search_type']
            search_term = request.form['search_term']
            home_dir = f"/home/{session['username']}"

            results = []
            if search_type == 'name':
                for root, dirs, files in os.walk(home_dir):
                    for file in files:
                        if search_term in file:
                            results.append(os.path.join(root, file))
            elif search_type == 'extension':
                for root, dirs, files in os.walk(home_dir):
                    for file in files:
                        if file.endswith(search_term):
                            results.append(os.path.join(root, file))

            return redirect(url_for('search', results=results))
        else:
            results = request.args.get('results', [])
            return render_template('search.html', username=session['username'], results=results)
    else:
        return redirect(url_for('login'))
  
@app.route('/download')
def download():
    if 'username' in session:
        logging.info(f"User {session['username']} a telecharge un fichier.")
        home_dir = f"/home/{session['username']}"
        zip_path = "C:/Users/ENVY/github-classroom/esisa-dev/webhomespace-houdakhiati/fichier.zip"
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for root, dirs, files in os.walk(home_dir):
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    files = [f for f in files if not f.startswith('.')]
                    for file in files:
                        zip_file.write(os.path.join(root, file))
                    for dir in dirs:
                        zip_file.write(os.path.join(root, dir))
        
            logging.info(f"Le fichier a été créé avec succès à l'emplacement {zip_path}.")
            return send_file(zip_path, as_attachment=True)
        
        except Exception as e:
            logging.error(f"Une erreur s'est produite lors de la création du fichier ZIP: {str(e)}")
            return "Impossible de télécharger"
            
    else:
        logging.warning("Tentative d'accès non autorisée à la page de téléchargement.")
        return "Impossible de télécharger"

  

@app.route('/logout')
def logout():
    if 'username' in session:
        logging.info(f"User {session['username']} logged out.")
        session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)