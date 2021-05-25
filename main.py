import yaml
from flask import request, render_template

from app.settings import app, BASE_DIR
from app.models import User


@app.route("/doc-schema/")
def doc_schema():
    doc = open(f'{BASE_DIR}/swagger-doc.yml', 'r', encoding='utf-8')
    return yaml.load(doc.read())


@app.route("/")
def docs():
    return render_template('documentation.html')


@app.route("/users/", methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route("/users/<user_id>", methods=['GET', 'PUT', 'DELETE'])
def user_view(user_id=None):
    if request.method == 'GET':
        if user_id is None:
            return User.objects.to_json()
        else:
            user = User.objects(id=user_id).first()
            if user is None:
                return {'message': 'Usuário não encontrado'}, 404
            return user.to_json()

    elif request.method == 'POST':
        req_data = request.get_json()
        errors = []
        if req_data.get('name') is not None and req_data.get('document') is not None:
            user = User.objects.create(
                name=req_data['name'],
                document=req_data['document'],
                address=req_data['address']
            )
            return {"message": f"Usuário {user.name} criado!"}
        if req_data.get('name') is None:
            errors.append('Nome é requerido')
        if req_data.get('document') is None:
            errors.append('Documento é requerido.')
        return {'errors': errors}, 400

    if request.method == 'PUT':
        user = User.objects(id=user_id).first()
        req_data = request.get_json()
        if user is None:
            return {'message': 'Usuário não encontrado'}, 404
        user.name = user.name if req_data.get('name') is None else req_data['name']
        user.document =  user.document if req_data.get('document') is None else req_data['document']
        user.address = user.address if req_data.get('address') is None else req_data['address']
        user.save()
        return {'message': f'Usuário {user.name} atualizado.'}

    if request.method == 'DELETE':
        user = User.objects(id=user_id).first()
        if user is None:
            return {'message': 'Usuário não encontrado'}, 404
        user.delete()
        return {'message': f'Usuário {user.name} foi deletado.'}
