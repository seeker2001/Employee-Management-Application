from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, PasswordField, RadioField, IntegerField
from wtforms.validators import Length, Email, DataRequired, ValidationError, Regexp, EqualTo
from datetime import date
from application.models import Employee

# Registration form for the employees
class RegisterForm(FlaskForm):

    # check from database if email already exists
    def validate_email_address(self, email_to_check):
        email = Employee.query.filter_by(email_address=email_to_check.data).first()
        if email:
            raise ValidationError('Email address already exists!')

    # check if the dob is correct or not
    def validate_dob(self, dob_to_check):
        dob_to_check = dob_to_check.data
        today = date.today()
        age = today.year - dob_to_check.year - ((today.month, today.day) < (dob_to_check.month, dob_to_check.day))
        if age < 18:
            raise ValidationError('Enter valid date of birth, age cannot be less than 18!!')
    
    # check if the password is a mix of characters, digits and special characters
    def validate_password1(self, password_to_check):
        special_characters = {'@', '#', ' ', '*'}
        password_to_check = password_to_check.data
        characterPresent, digitPresent = False, False
        specialCharacterPresent = False
        invalidSpecialCharacter = False
        for ch in password_to_check:
            if ch.isalnum():
                if ch.isalpha():
                    characterPresent = True
                else:
                    digitPresent = True
            else:
                if ch in special_characters:
                    specialCharacterPresent = True
                else:
                    invalidSpecialCharacter = True
        if not ((characterPresent and digitPresent and specialCharacterPresent) and (not invalidSpecialCharacter)):
            raise ValidationError("Password should be a mix of digits, letters and special characters like @, #, * and space")

    firstName = StringField(label='First Name:', validators=[DataRequired(), Length(min=2, max=30)])
    lastName = StringField(label='Last Name:', validators=[DataRequired()])
    email_address = StringField(label='Email Address:', validators=[DataRequired(), Email()])
    address = StringField(label='Address:', validators=[DataRequired(), Length(min=3)])
    dob = DateField(label='Date of Birth:', validators=[DataRequired()])
    phoneNumber = StringField(label='Phone Number:', validators=[DataRequired(), Regexp('^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$')])
    password1 = PasswordField(label="Create Password:", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1', message='Password must match')])
    submit = SubmitField(label='Create Account')


class UpdateForm(FlaskForm):
    # check if the dob is correct or not
    def validate_dob(self, dob_to_check):
        dob_to_check = dob_to_check.data
        today = date.today()
        age = today.year - dob_to_check.year - ((today.month, today.day) < (dob_to_check.month, dob_to_check.day))
        if age < 18:
            raise ValidationError('Enter valid date of birth, age cannot be less than 18!!')
    
    id_ = IntegerField(label='id', validators=[DataRequired()])
    firstName = StringField(label='First Name:', validators=[DataRequired(), Length(min=2, max=30)])
    lastName = StringField(label='Last Name:', validators=[DataRequired()])
    address = StringField(label='Address:', validators=[DataRequired(), Length(min=3)])
    dob = DateField(label='Date of Birth:', validators=[DataRequired()])
    phoneNumber = StringField(label='Phone Number:', validators=[DataRequired(), Regexp('^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$')])
    submit = SubmitField(label='Update')



# Login form for admin and employee
class LoginForm(FlaskForm):
    email_address = StringField(label='Email Address:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    role = RadioField(label='Role:', choices=[('employee', 'Employee'), ('admin', 'Admin')], default='employee')
    submit = SubmitField(label='Sign in')


