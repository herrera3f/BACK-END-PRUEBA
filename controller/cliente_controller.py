from model.cliente_model import Client

## '' = char , "" = int
## un array solo se puede guardar datos de unsolo tipo
## una lista agrega datos de varios tipos

class ClienController:

    def __init__(self):
        self.clientes = []

    def add_client(self, id,nombre ,email):
        cliente = Client(id,nombre,email)
        self.clientes.append(cliente)

    def get_clientes(self):
        return self.clientes
    
    def update_client(self, id, nombre, email):
        for cl in self.clientes:
            if cl.id == id:
                cl.nombre = nombre
                cl.email = email
                ##esta funcion es para que se pueda actualizar un cliente y funciona con el id
                break
            
    def delete_client(self, id):
        for cl in self.clientes:
            if cl.id == id:
                ##esta funcion es para que se pueda eliminar un cliente y funciona con el id
                self.clientes.remove(cl)
                break