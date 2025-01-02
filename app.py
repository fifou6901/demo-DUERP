from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__, static_folder='assets')  # Configuration pour servir les fichiers statiques
app.secret_key = '123456789'  # Changez cela pour sécuriser votre application

# Simuler une base de données
users = {
    "flo@gmail.com": "admin"  # Utilisateur de test
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email in users and users[email] == password:
        session['user'] = email
        return redirect(url_for('dashboard'))
    else:
        flash('Identifiants invalides. Veuillez réessayer.', 'error')
        return redirect(url_for('index'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        if email in users:
            flash(f"Un email de réinitialisation a été envoyé à {email}.", 'success')
        else:
            flash("Cet email n'existe pas dans notre base.", 'error')
        return redirect(url_for('index'))
    return render_template('forgot_password.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Vous avez été déconnecté.", 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
