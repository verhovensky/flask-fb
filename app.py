from flask import Flask, render_template, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

app = Flask(__name__)
# app.config['SECRET_KEY']= os.getenv('mykey')
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()


links = (
    ('/', 'Homepage'),
    ('/add_form', 'Add new country'),
    ('/list', 'View all countries'),
)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    heading = 'Flask Country Application'
    description = 'Flask application for countries adding and listing with Firebase.'
    return render_template('index.html', heading=heading, description=description, links=links)


@app.route('/add_form', methods=['GET', 'HEAD'])
def add_form():
    # TODO: Add Flask-WTF for form validation
    heading = 'Add country'
    description = 'Fill in the form and press Create butoon'
    return render_template('add_form.html', heading=heading,
                           description=description, links=links), 200


@app.route('/add', methods=['POST'])
def add_country():
    try:
        c = {
            'name': request.form['name'],
            'area': request.form['area'],
            'population': request.form['population'],
            'density': request.form['density'],
        }
        country_ref = db.collection(u'Countries').document(c['name'])
        country_ref.set(c)
        return render_template('success.html', country=c,
                               heading='Country created successfully!',
                               description='Your country was added to database',
                               links=links), 200
    except Exception as e:
        return f"An Error occured: {e}"


@app.route('/list')
def list_all_countries():
    try:
        country_ref = db.collection(u'Countries')
        # Check if ID was passed to URL query
        country_id = request.args.get('id')
        if country_id:
            todo = country_ref.document(country_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            countries = [doc.to_dict() for doc in country_ref.stream()]
            return render_template('list.html', countries=countries,
                                   heading='All countries',
                                   description='Table displays all countries in a database',
                                   links=links), 200
    except Exception as e:
        return f"An Error Occured: {e}"


if __name__ == '__main__':
    app.run()
