from flask import Flask, jsonify

#se realiza la instancia de la clase Flask
app = Flask(__name__)

# se declara la clase conjunto y sus métodos
class Conjunto:
    def __init__(self):
        self.numeros = set(range(1,101))
    # método para extraer el número que se le proporcione (retorna valores)    
    def extract(self, numero):
        if (numero in self.numeros):
            self.numeros.remove(numero)
            msg = f'se removio el número {numero} del conjunto'
            return msg
        else:
            msg = f'el número {numero} no se encuentra en el conjunto'
            return msg
    # calcula el número faltante y valida longitud del conjunto
    def num_falt(self):
        if len(self.numeros) == 99:
            number = sum(range(1,101)) - sum(self.numeros)
            msg = f'el número faltante es {number}'
            return msg
        elif len(self.numeros) == 100:
            msg = 'Aún no se extrae un número'
            return msg
        else:
            self.numeros = set(range(1,101))
            msg = 'ya se ha eliminado mas de un elemento, vuelve a ingresar un número a retirar'
            return msg

#instncia de clase conjunto
conjuto = Conjunto()

#se definen las rutas y métodos permitidos
@app.route('/', methods = ['GET'])
def index():
    return jsonify({'bienvenido' : 'rutas y descripción',
                    'extract' : 'extrae del conjunto el número que se le pase',
                    'view_num': 'devuelve el/los números/números que hacen falta en el conjunto'})


#convierte el argumento en un entero, indica al usuario ingresar un valor correcto en caso de no haberlo hecho
@app.route('/extract/<numero>', methods = ['GET'])
def quit(numero):
    try:    
        number = int(numero)
        if (number < 0):
            return jsonify({'mensaje' : 'ingresa un número entero en un rango del 1 al 100'})
        elif (number <= 100):
            msg = conjuto.extract(number)
            return jsonify({'mensaje' : msg})
        else:
            return jsonify({'mensaje' : 'ingresa un número entero en un rango del 1 al 100'})
    except ValueError as e:
        print(f'El error es: {e}')
        return jsonify({'mensaje' : 'ingresa un número válido',
                        'instrucción' : 'numero entero en un rango de 1 hasta 100'}), 500


# indica al usuario el número faltante del conjunto
@app.route('/view_num', methods = ['GET'])
def out():
    try:
        msg = conjuto.num_falt()
        return jsonify({'mensaje' : msg})
    except ValueError as e:
        return jsonify({'mensaje' : f'error detectado: {e}'}), 500
    
# funciones para manjerar errores 400
def method_not(error):
    return jsonify({'mensaje' : 'método no válido para la ruta'}), 405

def not_found(error):
    return jsonify({'mensaje' : 'página no encontrada'}), 404


# indica que hacer cuando se levanta el servidor
if __name__ == "__main__":
    app.register_error_handler(404, not_found)
    app.register_error_handler(405, method_not)
    app.run(host='0.0.0.0', port= 7777, debug=True)