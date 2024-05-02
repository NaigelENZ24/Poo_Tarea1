from utilities import borrarPantalla, gotoxy
import datetime
import time

class Menu:
    def __init__(self,titulo="",opciones=[],col=6,fil=1):
        self.titulo=titulo
        self.opciones=opciones
        self.col=col
        self.fil=fil
        
    def menu(self):
        gotoxy(self.col,self.fil);print(self.titulo)
        self.col-=5
        for opcion in self.opciones:
            self.fil +=1
            gotoxy(self.col,self.fil);print(opcion)
        gotoxy(self.col+5,self.fil+2)
        opc = input(f"Elija opcion[1...{len(self.opciones)}]: ") 
        return opc 
    
   #Definición del decorador DNI
def cedula_decorador(func):
    def nueva_funcionalidad(*args, **kwargs):
        func.__name__
        result = func(*args, **kwargs)
        return result
    
    return nueva_funcionalidad

class Valida:
    
    def solo_numeros(self, mensajeError, col, fil):
        while True:
            gotoxy(col, fil)
            valor = input(" ")
            try:
                if valor == "":
                    break  
                elif int(valor) >= 0:
                    break  
            except ValueError:
                pass

            gotoxy(col, fil)
            print(mensajeError)
            time.sleep(1)
            gotoxy(col, fil)
            print(" " * 20)

        return int(valor) if valor != "" else 0

    def solo_letras(self, mensajeError, col, fil): 
        while True:
            gotoxy(col, fil)
            valor = input(" ")
            if valor == "":
                break 
            elif valor.strip().isalpha():
                break  
            else:
                gotoxy(col, fil); print(" {}".format(mensajeError))
                time.sleep(1)
                gotoxy(col, fil); print(" " * 20)
        return valor

    def solo_decimales(self, mensajeError, col, fil):
        while True:
            gotoxy(col, fil)
            valor = input()
            try:
                if valor == "":
                    break 
                elif float(valor) >= 0:
                    break  
            except ValueError:
                pass  

            gotoxy(col, fil)
            print(mensajeError)
            time.sleep(1)
            gotoxy(col, fil)
            print(" " * 20)

        return float(valor) if valor != "" else 0.0
    
    @cedula_decorador
    def cedula(self,mensajeError,col,fil):
        def validar_cedula_ecuatoriana(cedula):
            # Códigos de provincias de Ecuador
            provincias = range(1, 25) 
            tercer_digito = range(0, 6)
            if (len(cedula) == 10 and cedula.isdigit() and
                int(cedula[:2]) in provincias and
                int(cedula[2]) in tercer_digito):
                coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
                suma = 0
                verificador = int(cedula[9])
            
                for i in range(9):
                    valor = int(cedula[i]) * coeficientes[i]
                    suma += valor if valor < 10 else valor - 9
            
                digito_calculado = (suma // 10 + 1) * 10 - suma if suma % 10 != 0 else suma
                return digito_calculado % 10 == verificador
            return False

        while True:
            gotoxy(col, fil)
            valor = input()
            if validar_cedula_ecuatoriana(valor):
                break
            else:
                gotoxy(col, fil); print(mensajeError)
                time.sleep(1)
                gotoxy(col, fil); print(" " * 50)
        return valor
    
    def validar_fecha(self,mensajeError,col,fil):
        while True:
            gotoxy(col,fil)
            nueva_fecha = input()
            try:
                # Intenta convertir el string a un objeto datetime.
                datetime.datetime.strptime(nueva_fecha, '%Y-%m-%d')
                return nueva_fecha
            except ValueError:
                # Si ocurre un error en la conversión, imprime un mensaje y repite el bucle.
                gotoxy(col,fil);print(" {}".format(mensajeError))
                time.sleep(1)
                gotoxy(col,fil);print(" "*30)
class otra:
    pass    

if __name__ == '__main__':
    # instanciar el menu
    opciones_menu = ["1. Entero", "2. Letra", "3. Decimal"]
    menu = Menu(titulo="-- Mi Menú --", opciones=opciones_menu, col=10, fil=5)
    # llamada al menu
    opcion_elegida = menu.menu()
    print("Opción escogida:", opcion_elegida)
    valida = Valida()
    if(opciones_menu==1):
      numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
      print("Número validado:", numero_validado)
    
    numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
    print("Número validado:", numero_validado)
    
    letra_validada = valida.solo_letras("Ingrese una letra:", "Mensaje de error")
    print("Letra validada:", letra_validada)
    
    decimal_validado = valida.solo_decimales("Ingrese un decimal:", "Mensaje de error")
    print("Decimal validado:", decimal_validado)