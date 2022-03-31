from coffee.db.create import create

with open('employees.txt', 'r') as f:
    employees = []
    for line in f:
        type_, name, login, password = map(str.strip, line.strip().split(';'))
        type_ = 0 if type_ == 'c' else 1

        employees.append({
            'type': type_,
            'login': login,
            'password': password,
            'name': name
        })

    create(employees)

