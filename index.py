import os 
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from controller.cliente_controller import ClienController
from model.cliente_model import Client

clientes = ClienController()

class MySHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == "/":
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            ##esto es para llamar la variable clientes
            todosClientes = clientes.get_clientes()
            html_content = "<h1>Lista de Clientes, similar Base de datos.</h1><ul>"
            
            for cl in todosClientes:
                html_content += f"<li>{cl.id} - {cl.nombre} - {cl.email}</li>"
            
            html_content += "</ul><hr>"
            ##este es el formulario para agregar clientes, actualizar y eliminar

            html_form = """
                        <h2> Agregar clientes</h2>

                        <form method="POST" action="/add">
                            <label for="nombre">Nombre:</label><br>
                            <input type="text" id="nombre" name="nombre"><br>

                            <label for="email">Email:</label><br>
                            <input type="text" id="email" name="email"><br>

                            <input type="submit" value="Agregar Cliente">
                        </form>
                        <hr>
                        """
                        
            html_update = """
                        <h2> Actualizar clientes</h2>
                        <form method="POST" action="/update">
                            <label for="id">ID:</label><br>
                            <input type="text" id="id" name="id"><br>

                            <label for="nombre">Nombre:</label><br>
                            <input type="text" id="nombre" name="nombre"><br>

                            <label for="email">Email:</label><br>
                            <input type="text" id="email" name="email"><br>

                            <input type="submit" value="Actualizar Cliente">
                        </form>
                        <hr>
                        """
                        
                        
            html_delete = """
                        <h2> Eliminar clientes</h2>
                        <form method="POST" action="/delete">
                            <label for="id">ID:</label><br>
                            <input type="text" id="id" name="id"><br>

                            <input type="submit" value="Eliminar Cliente">
                        </form>
                        """
            ##esto es para que se muestra el formulario en el navegador
            html_content += html_form + html_update + html_delete
            self.wfile.write(html_content.encode())

    def do_POST(self):
        
        content_length = int(self.headers['content-length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        ##esto es para que se pueda leer el post_data
        parsed_data = urllib.parse.parse_qs(post_data)
        
        
        ##esta funcion es para que se pueda agregar un cliente
        if self.path == '/add':
            nombre = parsed_data['nombre'][0]
            correo = parsed_data['email'][0]
            clientes.add_client(len(clientes.get_clientes()) + 1, nombre, correo)
        elif self.path == '/update':
            ##esta funcion es para que se pueda actualizar un cliente
            id = int(parsed_data['id'][0])
            nombre = parsed_data['nombre'][0]
            correo = parsed_data['email'][0]
            clientes.update_client(id, nombre, correo)
        elif self.path == '/delete':
            ##esta funcion es para que se pueda eliminar un cliente
            id = int(parsed_data['id'][0])
            clientes.delete_client(id)

        self.send_response(303)
        self.send_header('location', '/')
        self.end_headers()
##esto es para que se pueda levantar el servidor
PORT = 8000
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

with HTTPServer(("", PORT), MySHandler) as httpd:
    print(f"Servidor levantado desde el puerto {PORT}")
    httpd.serve_forever()
