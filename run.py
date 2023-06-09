from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/db_todolist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#### crear una tabla con el ORM #####
class Tarea(db.Model):
    id = db.Column(db.Integer,primary_key=True) #id INT NOT NULL PRIMARY KEY
    descripcion = db.Column(db.String(200),nullable=False) #descripcion VARCHAR(200) NOT NULL
    estado = db.Column(db.String(100),nullable=False)

    def __init__(self,descripcion,estado):
        self.descripcion = descripcion
        self.estado = estado


### ESQUEMAS ###

ma = Marshmallow(app)
class TareaSchema(ma.Schema):
    class Meta:
        fields = ('id','descripcion','estado')

db.create_all()
print("se creo la tabla tarea en la base de datos")

@app.route('/')
def index():
    context = {
        'status':True,
        'content':'servidor activo'
    }

    return jsonify(context)

@app.route('/tarea')
def getTarea():
    data = Tarea.query.all() #select id,descripcion,estado from tarea
    data_schema = TareaSchema(many=True)

    context = {
        'status':True,
        'content':data_schema.dump(data)
    }

    return jsonify(context)

@app.route('/tarea/<id>')
def getTareaById(id):
    data = Tarea.query.get(id)
    data_schema = TareaSchema()

    context = {
        'status':True,
        'content':data_schema.dump(data)
    }

    return jsonify(context)

@app.route('/tarea',methods=['POST'])
def setTarea():
    descripcion = request.json['descripcion']
    estado = request.json['estado']

    #insert into tarea(descripcion,estado) values(?,?)
    nuevaTarea = Tarea(descripcion,estado)
    db.session.add(nuevaTarea)
    db.session.commit()

    data_schema = TareaSchema()

    context = {
        'status':True,
        'content':data_schema.dump(nuevaTarea)
    }

    return jsonify(context)

@app.route('/tarea/<id>',methods=['PUT'])
def updateTarea(id):
    descripcion = request.json['descripcion']
    estado = request.json['estado']

    updateTarea = Tarea.query.get(id)
    updateTarea.descripcion = descripcion
    updateTarea.estado = estado
    db.session.commit()

    data_schema = TareaSchema()

    context = {
        'status':True,
        'content':data_schema.dump(updateTarea)
    }

    return jsonify(context)

@app.route('/tarea/<id>',methods=['DELETE'])
def deleteTarea(id):

    deleteTarea = Tarea.query.get(id)
    db.session.delete(deleteTarea)
    db.session.commit()

    data_schema = TareaSchema()

    context = {
        'status':True,
        'content':data_schema.dump(deleteTarea)
    }

    return jsonify(context)

app.run(debug=True)