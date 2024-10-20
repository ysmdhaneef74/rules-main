from flask import Flask, request, jsonify, render_template
from database import db, init_db, User
from rules import create_rule, evaluate_rule

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rules.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
init_db(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    """
    Add a new user to the database.

    Returns:
        A JSON response with a success message.
    """
    data = request.json

    # Create a new User object
    new_user = User(
        name=data['name'],
        age=data['age'],
        department=data['department'],
        income=data['income'],
        spend=data['spend']
    )

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # Return a JSON response
    return jsonify({'message': 'User added successfully!'}), 201

@app.route('/check_eligibility', methods=['POST'])
def check_eligibility():
    data = request.json
    rule_string = data.get('rule')

    # Validate rule format: it should contain 3 parts (field, operator, value)
    if not rule_string:
        return jsonify({'error': 'Rule is required.'}), 400

    parts = rule_string.split()
    if len(parts) != 3:
        return jsonify({'error': 'Invalid rule format. Expected format: "field operator value", e.g., "age > 30".'}), 400

    field, operator, value = parts

    # You can further validate that the field and operator are valid, if needed
    valid_fields = ['age', 'department', 'income', 'spend']
    valid_operators = ['>', '<', '=', '>=', '<=', '!=']

    if field not in valid_fields:
        return jsonify({'error': f'Invalid field "{field}". Expected one of {valid_fields}.'}), 400

    if operator not in valid_operators:
        return jsonify({'error': f'Invalid operator "{operator}". Expected one of {valid_operators}.'}), 400

    user_data = {
        "age": data.get('age'),
        "department": data.get('department'),
        "income": data.get('income'),
        "spend": data.get('spend')
    }

    try:
        ast = create_rule(rule_string)
        result = evaluate_rule(ast, user_data)
        return jsonify({'eligible': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

def init_db(app):
    with app.app_context():
        try:
            db.create_all()
            print("Database created successfully!")
        except Exception as e:
            print(f"Error creating the database: {e}")

if __name__ == '__main__':
    init_db(app)
    app.run(debug=True)
