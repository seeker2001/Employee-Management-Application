from application import db,bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_employee(emp_id):
    return Employee.query.get(emp_id)

class Employee(db.Model, UserMixin):
    __tablename__ = 'Employee'
    id = db.Column(db.Integer(), primary_key=True)
    firstName = db.Column(db.String(length=30), nullable=False)
    lastName = db.Column(db.String(length=30), nullable=False)
    email_address= db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    phoneNumber = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False)

    # setting the password 
    @property
    def password(self):
        return self.password
    
    # this method will change the plain password to a hash value
    @password.setter
    def password(self, plain_password):
        self.password_hash = bcrypt.generate_password_hash(plain_password).decode('utf-8')
    
    # function will check whether the password entered is correct
    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    # this method will be used for flask restful api to get serialized data of a employee object
    def serialize(self):
        dict = {"id":self.id, "firstName":self.firstName, "lastName":self.lastName, "email_address":self.email_address, "dob":str(self.dob), "address":self.address, "isAdmin":self.isAdmin, "phoneNumber":self.phoneNumber}
        return dict
    