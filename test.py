from flask import Flask, jsonify, render_template, request, send_from_directory

app = Flask(__name__, static_folder='view/assets', template_folder="view")
# app.config['SERVER_NAME'] = 'localhost:5000'

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

# @app.route('/test1', methods=['GET'])
# def get_tasks():
#     print("GET test1")
#     return jsonify({'tasks': tasks})
    
@app.route('/test2', methods=['POST'])
def push_tasks():
    # Get data received from javascript
    result = request.form
    # resp = {"message": "Your msg is " + data}
    print("POST test2")
    print(result)
    return result

@app.route('/test2', methods=['GET'])
def get_tasks2():
    print(request.get_json())
    print("GET task2")
    return request.json


@app.route('/', methods=['GET'])
def html_route():
    print("Loaded root")
    return render_template("landing.html")
    # return send_from_directory(app.static_folder, 'landing.html')

if __name__ == '__main__':
    app.run(debug=True)
