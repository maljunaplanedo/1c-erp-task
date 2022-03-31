from coffee.db.create import create

employees = []

with open('employees.txt', 'r') as f:
    for line in f:
        type_, name, login, password = map(str.strip, line.strip().split(';'))
        type_ = 0 if type_ == 'c' else 1

        employees.append({
            'type': type_,
            'login': login,
            'password': password,
            'name': name
        })

with open('coffee_types.txt', 'r') as f:
    coffee_types = list(map(str.strip,  f.read().split(';')))

create(employees, coffee_types)
