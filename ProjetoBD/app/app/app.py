import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask, request
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = {}
    stats = db.execute('''
    SELECT * FROM
      (SELECT COUNT(*) animal_id FROM Animais)
    JOIN
      (SELECT COUNT(*) continente_id FROM Continente)
    JOIN
      (SELECT COUNT(*) dieta_id FROM Dieta)
    JOIN
      (SELECT COUNT(*) habitat_id FROM Habitat)
    JOIN
      (SELECT COUNT(*) animal FROM Origens)
    ''').fetchone()
    logging.info(stats)
    return render_template('index.html', stats=stats)

# Animais
@APP.route('/animais/')
def list_animais():
    animais = db.execute(
      '''
      SELECT animal_id, animal_name, dieta
      FROM Animais
      ORDER BY animal_id
      ''').fetchall()
    return render_template('animal-list.html', animais=animais)

@APP.route('/animais/<int:id>/')
def get_animal(id):
    animal = db.execute(
        '''
        SELECT animal_name, animal_id, dieta
        FROM Animais
        WHERE animal_id = ?
        ''', [id]).fetchone()

    if animal is None:
        abort(404, 'Animal id {} does not exist.'.format(id))

    continente = db.execute(
        '''
        SELECT Continente.continente_name
        FROM Animais
        JOIN Origens ON Animais.animal_id = Origens.animal
        JOIN Continente ON Origens.continente = Continente.continente_id
        WHERE Animais.animal_id = ?
        GROUP BY Continente.continente_name
        ORDER BY Continente.continente_name
        ''', [id]).fetchall()

    habitat = db.execute(
        ''' 
        SELECT Animais.animal_name, Habitat.habitat_name
        FROM Animais
        JOIN Origens ON Animais.animal_id = Origens.animal
        JOIN Habitat ON Origens.habitat = Habitat.habitat_id
        WHERE Animais.animal_id = ?
        GROUP BY Habitat.habitat_name
        ORDER BY Habitat.habitat_name
        ''', [id]).fetchall()
    
    return render_template('animal.html',
                           animal=animal, continente=continente, habitat=habitat)

@APP.route('/animal/search/<expr>/')
def search_animal(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  animal = db.execute(
      ''' 
    SELECT animal_id, animal_name
    FROM Animais
    WHERE animal_name LIKE ?
      ''', [expr]).fetchall()
  return render_template('animal-search.html',
           search=search,animal=animal)

# Continentes
@APP.route('/continentes/')
def list_continentes():
    continentes = db.execute('''
        SELECT continente_id, continente_name
        FROM Continente
        ORDER BY continente_name
    ''').fetchall()
    
    return render_template('continentes-list.html', continentes=continentes)

@APP.route('/continentes/<int:id>/')
def view_habitats_by_continentes(id):
  
  nome_continentes = db.execute(
    '''
    SELECT Continente.continente_name, Continente.continente_id
    FROM Continente
    WHERE Continente.continente_id = ?
    ''', [id]).fetchall()

  
  continentes = db.execute('''
    SELECT continente_id, continente_name
    FROM continente
    ORDER BY continente_name
    ''').fetchall()

  habitats = db.execute(
    '''
    SELECT Habitat.habitat_name
    FROM Continente
    JOIN Habitat ON Origens.habitat = Habitat.habitat_id
    JOIN Origens ON Continente.continente_id = Origens.continente
    WHERE Continente.continente_id = ?
    GROUP BY Habitat.habitat_name
    ''', [id]).fetchall()

  if habitats is None:
     abort(404, 'Continente id {} does not exist.'.format(id))

  animais = db.execute(
    '''
    SELECT Animais.animal_id, Animais.animal_name
    FROM Animais
    JOIN Origens ON Animais.animal_id = Origens.animal
    WHERE Origens.continente = ?
    GROUP BY Animais.animal_name
    ''', [id]).fetchall()

  return render_template('continentes.html', 
          nome_continentes=nome_continentes, continentes=continentes, animais=animais, habitats=habitats)

@APP.route('/continentes/search/<expr>/')
def search_continentes(expr):
  search = { 'expr': expr }
  # SQL INJECTION POSSIBLE! - avoid this!
  continentes = db.execute(
      ' SELECT continente_id, continente_name'
      ' FROM Continente '
      ' WHERE continente_name LIKE \'%' + expr + '%\''
    ).fetchall()

  return render_template('continentes-search.html', 
           search=search,continentes=continentes)

# Habitats
@APP.route('/habitats/')
def list_habitats():
    habitats = db.execute('''
    SELECT habitat_id, habitat_name
    FROM Habitat
    ORDER BY habitat_name
    ''').fetchall()
    return render_template('habitats-list.html', habitats=habitats)

@APP.route('/habitats/<int:id>/')
def view_habitats_by_id(id):
    habitat = db.execute(
        '''
        SELECT habitat_name, habitat_id
        FROM Habitat
        WHERE habitat_id = ?
        ''', [id]).fetchone()
    
    if habitat is None:
        abort(404, 'Habitat id {} does not exist.'.format(id))

    animais = db.execute(
        '''
        SELECT Animais.animal_id, Animais.animal_name
        FROM Animais
        JOIN Origens ON Animais.animal_id = Origens.animal
        WHERE Origens.habitat = ?
        GROUP BY Animais.animal_name
        ''', [id]).fetchall()

    return render_template('habitats.html',
                           habitat=habitat, animais=animais)
 
@APP.route('/habitats/search/<expr>/')
def search_habitats(expr):
  search = { 'expr': expr }
  # SQL INJECTION POSSIBLE! - avoid this!
  habitats = db.execute(
      ' SELECT habitat_id, habitat_name'
      ' FROM Habitat '
      ' WHERE habitat_name LIKE \'%' + expr + '%\''
    ).fetchall()

  return render_template('habitats-search.html', 
           search=search,habitats=habitats)

# Dieta
@APP.route('/dietas/')
def list_dietas():
    dietas = db.execute('''
        SELECT dieta_id, dieta_name
        FROM Dieta
        ORDER BY dieta_name
    ''').fetchall()

    return render_template('dieta-list.html', dietas=dietas)

@APP.route('/dieta/<int:id>/')
def view_animals_by_dieta(id):
    dieta_info = db.execute(
        '''
        SELECT Dieta.dieta_id, Dieta.dieta_name
        FROM Dieta
        WHERE Dieta.dieta_id = ?
        ''', [id]).fetchone()

    if dieta_info is None:
        abort(404, 'Dieta id {} does not exist.'.format(id))

    dietas = db.execute('''
        SELECT dieta_id, dieta_name
        FROM Dieta
        ORDER BY dieta_name
        ''').fetchall()

    animais = db.execute(
        '''
        SELECT Animais.animal_id, Animais.animal_name
        FROM Animais
        JOIN Dieta ON Animais.dieta = Dieta.dieta_name
        WHERE Dieta.dieta_id = ?
        GROUP BY Animais.animal_name
        ''', [id]).fetchall()

    return render_template('dieta.html',
                           dieta_info=dieta_info, dietas=dietas, animais=animais)
 
@APP.route('/dietas/search/<expr>/')
def search_dietas(expr):
  search = { 'expr': expr }
  # SQL INJECTION POSSIBLE! - avoid this!
  dietas = db.execute(
      ' SELECT dieta_id, dieta_name'
      ' FROM Dieta '
      ' WHERE dieta_name LIKE \'%' + expr + '%\''
    ).fetchall()

  return render_template('dieta-search.html', 
           search=search,dietas=dietas)