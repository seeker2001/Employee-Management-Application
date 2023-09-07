from flask_restful import Resource
from api import Employee, db
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

auth_data = {
    "admin" : "*@SuperSecretPwd@*"
}


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return auth_data.get(username) == password

class Search(Resource):
    @auth.login_required
    def get(self, search_data):
        # the searching operation is case insensitive so while comparing everything will be changed to uppercase
        # if the employee data starts with the search data it will be sent as response
        search_data = search_data.strip().upper()
        result = []
        if search_data != "":
            all_emp = Employee.query.all()
            for emp in all_emp:
                firstName, lastName = emp.firstName.upper(), emp.lastName.upper()
                fullName, address = firstName + " " + lastName, emp.address.upper()
                checkForCurrentEmployee = (firstName.startswith(search_data) or lastName.startswith(search_data) or 
                                        lastName.startswith(search_data) or fullName.startswith(search_data) or 
                                        address.startswith(search_data))
                if checkForCurrentEmployee:
                    result.append(emp.serialize())  
        # returning a json response
        return {"payload":result}
