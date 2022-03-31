def load():
    with open('host_port.txt', 'r') as f:
        return f.read().split(':')
