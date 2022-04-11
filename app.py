from flask import Flask, request, jsonify, render_template, abort
from flask import make_response, redirect, url_for
from flask_wtf import FlaskForm
from models import todos
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config["SECRET_KEY"] = "qwerty123"
csrf = CSRFProtect()


#def create_app():
#    app = Flask(__name__)
#    csrf.init_app(app)


@app.route("/api/todos/", methods=["GET"])
@csrf.exempt
def todos_api():
    return jsonify(todos.all())

@app.route("/api/todos/", methods=["POST"])
@csrf.exempt
def add_todo():
    if not request.json:
        abort(400)
    todo = {
    'id': todos.all()[-1]['id'] + 1,
    'title': request.json.get('title'),
    'description': request.json.get('description', ""),
    }
    todos.create(todo)
    return jsonify({'todo': todo}), 201


@app.route("/todos/<int:todos_id>", methods=["GET"])
def get_todo(todos_id):
    todo = todos.get(todos_id)
    if not todo:
        abort(404)
    return jsonify({"todo": todo})


@app.route("/todos/<int:todo_id>", methods=['DELETE'])
def remove_todos(todo_id):
    result = todos.delete(todo_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todos(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        ]):
        abort(400)
        todo = {
        'title': data.get('title', todo['title']),
        'description': data.get('description', todo['description']),
        }
        todos.update(todo_id, todo)
        return jsonify({'todo': todo})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=True)




