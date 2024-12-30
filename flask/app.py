from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # Cambia esto en producción
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)
db = SQLAlchemy(app)

# Modelo de Usuarios
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Modelo de Vocabulario
class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)  # La palabra en el idioma original
    translation = db.Column(db.String(100), nullable=False)  # La traducción al idioma destino
    level = db.Column(db.String(50))  # Ejemplo: 'A1', 'B1'
    topic = db.Column(db.String(100))  # Ejemplo: 'Colores', 'Familia'

# Crear la base de datos
with app.app_context():
    db.create_all()

def add_default_admin():
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", password="admin123", is_admin=True)
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['username'] = username
        return redirect(url_for('home'))
    else:
        return render_template('login.html', error="Usuario o contraseña incorrectos.")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not User.query.filter_by(username=username).first():
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Usuario ya registrado."

    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('home.html')

@app.route('/area/<area>')
def area(area):
    if 'username' not in session:
        return redirect(url_for('index'))

    questions_db = {
        'Derecho': [
            {'question': '¿Qué es el delito?', 'answer': 'Delito es aquello del dolo'},
            {'question': '¿Qué es derecho?', 'answer': 'sobre el derecho'},
            {'question': '¿Qué es dolo?', 'answer': 'sobre el dolo es intención'}
        ],
        'Medicina': [
            {'question': 'Pregunta 1 sobre Medicina', 'answer': 'Respuesta 1 sobre Medicina'},
            {'question': 'Pregunta 2 sobre Medicina', 'answer': 'Respuesta 2 sobre Medicina'},
            {'question': 'Pregunta 3 sobre Medicina', 'answer': 'Respuesta 3 sobre Medicina'}
        ],
        'Psicología': [
            {'question': 'Pregunta 1 sobre Psicología', 'answer': 'Respuesta 1 sobre Psicología'},
            {'question': 'Pregunta 2 sobre Psicología', 'answer': 'Respuesta 2 sobre Psicología'},
            {'question': 'Pregunta 3 sobre Psicología', 'answer': 'Respuesta 3 sobre Psicología'}
        ]
    }

    questions = questions_db.get(area, [])
    return render_template('area.html', area=area, questions=questions)

@app.route('/question_trainer/<area>/<path:question>', methods=['GET', 'POST'])
def question_trainer(area, question):
    if 'username' not in session:
        return redirect(url_for('index'))

    from urllib.parse import unquote
    question = unquote(question)

    questions_db = {
        'Derecho': [
            {'question': '¿Qué es el delito?', 'answer': 'Delito es aquello del dolo'},
            {'question': '¿Qué es derecho?', 'answer': 'sobre el derecho'},
            {'question': '¿Qué es dolo?', 'answer': 'sobre el dolo es intención'}
        ],
        'Medicina': [
            {'question': 'Pregunta 1 sobre Medicina', 'answer': 'Respuesta 1 sobre Medicina'},
            {'question': 'Pregunta 2 sobre Medicina', 'answer': 'Respuesta 2 sobre Medicina'},
            {'question': 'Pregunta 3 sobre Medicina', 'answer': 'Respuesta 3 sobre Medicina'}
        ],
        'Psicología': [
            {'question': 'Pregunta 1 sobre Psicología', 'answer': 'Respuesta 1 sobre Psicología'},
            {'question': 'Pregunta 2 sobre Psicología', 'answer': 'Respuesta 2 sobre Psicología'},
            {'question': 'Pregunta 3 sobre Psicología', 'answer': 'Respuesta 3 sobre Psicología'}
        ]
    }

    question_data = next((item for item in questions_db.get(area, []) if item['question'] == question), None)

    if not question_data:
        return "Pregunta no encontrada."

    return render_template('question_trainer.html', area=area, question=question_data['question'], answer=question_data['answer'])

@app.route('/quick_trainer', methods=['GET', 'POST'])
def quick_trainer():
    if 'username' not in session:
        return redirect(url_for('index'))

    from random import choice
    questions_db = {
        'Derecho': [
            {'question': '¿Qué es el delito?', 'answer': 'Delito es aquello del dolo'},
            {'question': '¿Qué es derecho?', 'answer': 'sobre el derecho'},
            {'question': '¿Qué es dolo?', 'answer': 'sobre el dolo es intención'}
        ],
        'Medicina': [
            {'question': 'Pregunta 1 sobre Medicina', 'answer': 'Respuesta 1 sobre Medicina'},
            {'question': 'Pregunta 2 sobre Medicina', 'answer': 'Respuesta 2 sobre Medicina'},
            {'question': 'Pregunta 3 sobre Medicina', 'answer': 'Respuesta 3 sobre Medicina'}
        ],
        'Psicología': [
            {'question': 'Pregunta 1 sobre Psicología', 'answer': 'Respuesta 1 sobre Psicología'},
            {'question': 'Pregunta 2 sobre Psicología', 'answer': 'Respuesta 2 sobre Psicología'},
            {'question': 'Pregunta 3 sobre Psicología', 'answer': 'Respuesta 3 sobre Psicología'}
        ]
    }

    all_questions = [q for questions in questions_db.values() for q in questions]
    random_question = choice(all_questions)

    if request.method == 'POST':
        user_answer = request.form['user_answer']
        correct_answer = random_question['answer']

        feedback = "¡Correcto! 🎉" if user_answer.strip().lower() == correct_answer.strip().lower() else f"Incorrecto. La respuesta correcta es: {correct_answer}"

        return render_template('quick_trainer.html', question=random_question['question'], feedback=feedback)

    return render_template('quick_trainer.html', question=random_question['question'])

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if 'username' not in session:
        return redirect(url_for('index'))

    current_user = User.query.filter_by(username=session['username']).first()
    if not current_user or not current_user.is_admin:
        return "Acceso denegado. No tienes permisos para acceder a esta página."

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = 'is_admin' in request.form

        if not User.query.filter_by(username=username).first():
            new_user = User(username=username, password=password, is_admin=is_admin)
            db.session.add(new_user)
            db.session.commit()
        else:
            return "El usuario ya existe."

    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Ruta de lecciones
@app.route('/lessons')
def lessons():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    # Aquí se pueden filtrar las palabras por tema o nivel si lo deseas
    words = Word.query.all()  # Obtiene todas las palabras
    return render_template('lessons.html', words=words)

# Ruta para agregar palabras
@app.route('/add_word', methods=['GET', 'POST'])
def add_word():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    current_user = User.query.filter_by(username=session['username']).first()
    if not current_user or not current_user.is_admin:
        return "Acceso denegado. No tienes permisos para agregar palabras."
    
    if request.method == 'POST':
        word = request.form['word']
        translation = request.form['translation']
        level = request.form['level']
        topic = request.form['topic']
        
        new_word = Word(word=word, translation=translation, level=level, topic=topic)
        db.session.add(new_word)
        db.session.commit()
        return redirect(url_for('lessons'))  # Redirige a la página de lecciones

    return render_template('add_word.html')

if __name__ == '__main__':
    with app.app_context():
        add_default_admin()  # Añadir el admin por defecto
    app.run(debug=True)
