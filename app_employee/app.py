from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
ma = Marshmallow()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://restful:2QlLm>A81bsz{@127.0.0.1:3306/restful'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    position = db.relationship("Position", back_populates="employee", uselist=False)

    def __init__(self, email, mobile):
        self.email = email
        self.mobile = mobile

    def __repr__(self):
        return f"id: {self.id}, email: {self.email}"

class Position(db.Model):
    __tablename__ = "position"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    employee = db.relationship("Employee", back_populates="position")

    def __init__(self, title, department, employee_id):
        self.title = title
        self.department = department
        self.employee_id = employee_id

    def __repr__(self):
        return f"id: {self.title}, email: {self.department}"

class EmployeeSchema(ma.Schema):
    class Meta:
        model = Employee
    id = ma.Int()
    email = ma.Str()
    mobile = ma.Str()
    position = ma.Nested('PositionSchema')

class PositionSchema(ma.Schema):
    class Meta:
        model = Position
    title = ma.Str()
    department = ma.Str()
    # employee_id = ma.Integer()


db.create_all()

@app.route("/employee", methods=["POST"])
def create_employee():
    data = request.get_json()
    employee_schema = EmployeeSchema()
    try:
        employee_schema.load(data)
        employee = Employee(
            email=data['email'], mobile=data['mobile']
        )
        db.session.add(employee)
        db.session.flush()
        position = Position(
            department=data['position']['department'],
            title=data['position']['title'],
            employee_id=employee.id
        )
        db.session.add(position)
        db.session.flush()
        db.session.commit()
    except ValidationError:
        app.logger.warning("Invalid data")
        return make_response(jsonify({"error": "Invalid data"}), 400)
    except IntegrityError as err:
        if "Duplicate entry" in str(err):
            app.logger.warning("employee already exist")
            return make_response(jsonify({"error": "employee already exist"}), 400)
        if "foreign key constraint fails" in str(err):
            app.logger.warning("employee not exist")
            return make_response(jsonify({"error": "employee not exist"}), 400)
    except Exception as err:
        app.logger.error(str(err))
        return make_response(jsonify({'error': 'Internal server error'}), 500)
    return make_response(jsonify(data), 200)

@app.route('/employee', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    employee_schema = EmployeeSchema()
    results = employee_schema.dump(employees, many=True)
    return make_response(jsonify(results))

@app.route('/employee/<id>', methods=['GET'])
def get_employee_by_id(id):
    employee_qs = Employee.query.get(id)
    if not employee_qs:
        app.logger.warning("employee not found")
        return make_response(jsonify({'error': 'employee not found'}), 400)
    employee_schema = EmployeeSchema()
    employee = employee_schema.dump(employee_qs)
    return make_response(jsonify(employee))

@app.route('/employee/<id>', methods=['PUT'])
def update_employee_by_id(id):
    data = request.get_json()
    employee = Employee.query.get(id)
    if data.get('email'):
        employee.email = data['email']
    if data.get('mobile'):
        employee.mobile = data['mobile']
    db.session.add(employee)
    db.session.commit()
    employee_schema = EmployeeSchema()
    employee = employee_schema.dump(employee)
    return make_response(jsonify({"employee": employee}))


@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee_by_id(id):
    employee_qs = Employee.query.get(id)
    if employee_qs:
        db.session.delete(employee_qs)
        db.session.commit()
    return make_response(jsonify({"status": "ok"}), 200)

@app.errorhandler(404)
def not_found(error):
    app.logger.warning(error)
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(error)
    return make_response(jsonify({'error': 'Internal server error'}), 500)

if __name__ == "__main__":
    app.run(debug=False)