from application import app, db
from flask import render_template, redirect, url_for, request, flash
from application.forms import RegisterForm, LoginForm, UpdateForm
from application.models import Employee
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
import requests

# route for home image
@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

# route for register page
@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_employee = Employee(firstName=form.firstName.data.capitalize(), lastName=form.lastName.data.capitalize(), email_address=form.email_address.data, password=form.password1.data, dob=form.dob.data, phoneNumber=form.phoneNumber.data, address=form.address.data, isAdmin=False)
        db.session.add(new_employee)
        db.session.commit()
        login_user(new_employee)
        flash(f'Account created successfully!!', category='success')
        return redirect(url_for('emp_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg[0]}', category='danger')
    return render_template('register.html', form=form)

# route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        # if form validates then check if the employee with entered email exists or not
        emp = Employee.query.filter_by(email_address=form.email_address.data).first()
        if emp and emp.check_password(attempted_password=form.password.data):
            login_user(emp)
            # if the chosen role is admin, redirect to the admin page 
            if emp.isAdmin and request.form.getlist('role')[0] == 'admin':
                return redirect(url_for('admin_page'))
            # otherwise redirect to the employee page 
            elif not emp.isAdmin and request.form.getlist('role')[0] == 'employee':
                return redirect(url_for('emp_page'))
            # else if the chosen role is incorrect show a flash message
            else:
                flash('Chose correct role', category='danger')
        else:
            flash('Email and password do not match! Please try again!!', category='danger')
    return render_template('login.html', form=form)

# route for employee page
@app.route('/employee', methods=['GET', 'POST'])
@login_required
def emp_page():
    if current_user.isAdmin:
        flash("You need to login as employee to access this page!!", category='info')
        return redirect(url_for('admin_page'))
    emp = Employee.query.filter_by(id=current_user.id).first()
    updateEmployeeForm = UpdateForm()
    # handling the update employee form
    if updateEmployeeForm.validate_on_submit():
        cur_emp = Employee.query.filter_by(id=updateEmployeeForm.id_.data).first()
        cur_emp.firstName = updateEmployeeForm.firstName.data
        cur_emp.lastName = updateEmployeeForm.lastName.data
        cur_emp.address = updateEmployeeForm.address.data
        cur_emp.phoneNumber = updateEmployeeForm.phoneNumber.data
        cur_emp.dob = updateEmployeeForm.dob.data
        db.session.commit()
        flash('Employee Info updated successfully!!', category='success')
        return redirect(url_for('emp_page'))
    if updateEmployeeForm.errors != {}:
        for err_msg in updateEmployeeForm.errors.values():
            flash(f'{err_msg[0]}', category='danger')  
        return redirect(url_for('emp_page'))    
    return render_template('emp_page.html', emp=emp, updateEmployeeForm=updateEmployeeForm)

# route for admin page
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_page():
    if not current_user.isAdmin:
        flash('You need to login as admin to access this page!!',category='info')
        return redirect(url_for('emp_page'))
    
    # two forms for updating the info of employee and adding new employee
    addEmployeeForm = RegisterForm()
    updateEmployeeForm = UpdateForm()

    emp_data = Employee.query.all()
    return render_template('admin.html', emp_data=emp_data, addEmployeeForm=addEmployeeForm, updateEmployeeForm = updateEmployeeForm)

# adding new employee from the admin
@app.route('/admin/add', methods=['POST', 'GET'])
def add_from_admin():
    addEmployeeForm = RegisterForm()
    
    if addEmployeeForm.validate_on_submit():
        new_employee = Employee(firstName=addEmployeeForm.firstName.data.capitalize(), lastName=addEmployeeForm.lastName.data.capitalize(), email_address=addEmployeeForm.email_address.data, password=addEmployeeForm.password1.data, dob=addEmployeeForm.dob.data, phoneNumber=addEmployeeForm.phoneNumber.data, address=addEmployeeForm.address.data, isAdmin=False)
        db.session.add(new_employee)
        db.session.commit()
        flash(f'Account created successfully!!', category='success')
        return redirect(url_for('admin_page'))
    if addEmployeeForm.errors != {}:
        for err_msg in addEmployeeForm.errors.values():
            flash(f'{err_msg[0]}', category='danger') 
        return redirect(url_for('admin_page'))

# updating existing employee info from admin
@app.route('/admin/update', methods=['GET', 'POST'])
def update_from_admin():
    updateEmployeeForm = UpdateForm()

    if updateEmployeeForm.validate_on_submit():
        cur_emp = Employee.query.filter_by(id=updateEmployeeForm.id_.data).first()
        cur_emp.firstName = updateEmployeeForm.firstName.data
        cur_emp.lastName = updateEmployeeForm.lastName.data
        cur_emp.address = updateEmployeeForm.address.data
        cur_emp.phoneNumber = updateEmployeeForm.phoneNumber.data
        cur_emp.dob = updateEmployeeForm.dob.data
        db.session.commit()
        flash('Employee Info updated successfully!!', category='success')
        return redirect(url_for('admin_page'))
    if updateEmployeeForm.errors != {}:
        for err_msg in updateEmployeeForm.errors.values():
            flash(f'{err_msg[0]}', category='danger')  
        return redirect(url_for('admin_page'))


# delete employee -> by admin
@app.route('/admin/delete/<id>/', methods=['POST', 'GET'])
def delete_from_admin(id):
    emp = Employee.query.get(id)
    db.session.delete(emp)
    db.session.commit()
    flash('Employee deleted Successfully!!', category='success')
    return redirect(url_for('admin_page'))
    
# route for search page
@app.route('/admin/searchresult', methods = ['GET', 'POST'])
@login_required
def search_page():
    updateEmployeeForm = UpdateForm()
    if request.method == 'POST':
        search_data = request.form['search-input'] + " "
        url = f'http://127.0.0.1:5000/searchApi/{search_data}'
        # get the api response
        response = requests.get(url, auth=('admin', '*@SuperSecretPwd@*'))
        # if response is valid show the search result page
        if response:
            response = response.json()
            return render_template('search_page.html', result = response['payload'], updateEmployeeForm=updateEmployeeForm)
    flash('There was some issue in fetching data!!', category='danger')
    return redirect(url_for('admin_page'))

# logout
@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!!', category='info')
    return redirect(url_for('home_page'))