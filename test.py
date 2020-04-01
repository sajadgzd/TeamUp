from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder='view')

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

@app.route('/test1', methods=['GET'])
def get_tasks():
    # print(request.get_json())
    return jsonify({'tasks': tasks})
    
@app.route('/test2', methods=['POST'])
def push_tasks():
    # Get data received from javascript
    data = request.get_data()
    resp = {"message": "Your msg is " + data}
    print(data)
    return jsonify(resp)

@app.route('/', methods=['GET', 'POST'])
def html_route():
    return render_template("landing.html")

if __name__ == '__main__':
    app.run(debug=True)