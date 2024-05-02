from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,blue_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient, VipClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce

path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create(self):
        
        validar = Valida()
        while True:
            borrarPantalla()
            print('\033c', end='')
            gotoxy(2,1);print(cyan_color+"█"*90)
            gotoxy(2,2);print(cyan_color+"██"+" "*34+"INGRESO DE CLIENTE"+" "*34+"██")
            
            #****************************************************
            gotoxy(7,4);print("dni: ")
            dni=validar.cedula("Error: debe contener 10 dígitos",23,4)
            json_file = JsonFile(path+'/archivos/clients.json')
            client = json_file.find("dni",dni)
            if client:
                gotoxy(38,6);print("Cliente ya existente")
                time.sleep(1)
            else: 
                break
            
        #****************************************************
        gotoxy(7,5);print("Nombre: ")
        first_name=validar.solo_letras("Error: Solo letras",23,5)
        gotoxy(7,6);print("Apellido:")
        last_name=validar.solo_letras("Error: Solo letras",23,6)
        
        #****************************************************
        gotoxy(7,7);type_client = str(input("El cliente es VIP? (s/n): ")).lower()
        if type_client =="s":
            vip=VipClient(first_name,last_name,dni)
            save = VipClient.getJson(vip)
        else:
            gotoxy(7,8);discount = input("Aplica al descuento el cliente? (s/n): ").lower()
            if discount == "s" : discount=True
            else:discount=False
            regular = RegularClient(first_name,last_name,dni, discount)
            save = RegularClient.getJson(regular)
            
        gotoxy(15,10);print(cyan_color+"Está seguro de grabar el cliente? (s/n):")
        gotoxy(58,10);procesar = input().lower()
        if procesar == "s":
            json_file = JsonFile(path+'/archivos/clients.json')
            invoices = json_file.read()
            invoices.append(save)
            json_file = JsonFile(path+'/archivos/clients.json')
            json_file.save(invoices)
            gotoxy(15,11);print("😊 cliente guardado satisfactoriamente 😊"+reset_color)
            gotoxy(15,13);input("Presione una tecla para continuar...") 
            
        else:
            gotoxy(15,10);print("🤣 No pudo registrar al cliente 🤣"+reset_color)    
        time.sleep(2)
        
    def update(self):
        validar = Valida()
        
        print('\033c', end='')
        gotoxy(2,1);print(cyan_color+"█"*90)
        gotoxy(2,2);print("██"+" "*30+"ACTUALIZACIÓN DE CLIENTES"+" "*31+"██"+reset_color)
        json_file = JsonFile(path+'/archivos/clients.json')
        gotoxy(2,2);clients = json_file.read()
        gotoxy(7,4);dni = print(cyan_color+"Ingrese el dni del cliente a actualizar: ")
        dni=validar.cedula("Error: debe contener 10 dígitos",50,4)
        
        client_update = None
        for client in clients:
            if client["dni"] == dni:
                client_update = client
                break
            
        if client_update:
    # Verificar que las claves existan antes de acceder a ellas
            if "nombre" in client_update:
                gotoxy(7,5);print("Nombre:", client_update["nombre"])
            if "apellido" in client_update:
                gotoxy(7,6);print("Apellido:", client_update["apellido"])
            if "valor" in client_update:
                gotoxy(7,7);print("Valor:", client_update["valor"])
    
    # Solicitar la nueva información del cliente
            gotoxy(7,8); print("Ingrese el nuevo nombre (enter si no desea actualizar): ")
            nuevo_nombre=validar.solo_letras("Error: Solo letras",65,8)
            gotoxy(7,9); print("Ingrese el nuevo apellido (enter si no desea actualizar): ")
            nuevo_apellido=validar.solo_letras("Error: Solo letras",65,9)
            gotoxy(7,10); print("Ingrese el nuevo valor (enter si no desea actualizar): ")
            nuevo_valor = validar.solo_numeros("Error: Solo letras",65,10)

    # Actualizar la información del cliente proporcionado
            if nuevo_nombre:
                client_update["nombre"] = nuevo_nombre
            if nuevo_apellido:
                client_update["apellido"] = nuevo_apellido
            if nuevo_valor:
                client_update["valor"] = int(nuevo_valor)

    # Guardar los cambios en el archivo JSON de productos
            json_file.save(clients)
            gotoxy(15,12);print(cyan_color+"Cliente actualizado exitosamente. :3")
        else:
            print("No se encontró ningún cliente con el dni proporcionado.")


        gotoxy(18,14);input("Presione Enter para continuar...")       
         
    def delete(self):
        validar = Valida()
        
        print('\033c', end='')
        gotoxy(2,1);print(cyan_color+"█"*90)
        gotoxy(2,2);print("██"+" "*30+"ELIMINACIÓN DE CLIENTE"+" "*34+"██")
        json_file = JsonFile(path+'/archivos/clients.json')
        gotoxy(2,2);json_file.read()
        gotoxy(7,5);dni = print("Ingrese el dni del cliente a eliminar: ")
        dni=validar.cedula("Error: debe contener 10 dígitos",50,5)
        client = json_file.find('dni',dni)
            
            
        if client:
            gotoxy(7,6);print(cyan_color + "DATOS DEL CLIENTE:" + reset_color)
            gotoxy(15,7);headers = "DNI".ljust(15) + "NOMBRE".ljust(20) + "APELLIDO".ljust(20) + "VALOR".ljust(15)
            gotoxy(10,8);print(cyan_color + "█" * len(headers) + reset_color)
            gotoxy(15,9);print(headers)
            gotoxy(10,10);print(cyan_color + "█" * len(headers) + reset_color)
                
            for find in client:
                client_info = find['dni'].ljust(15) + find['nombre'].ljust(20) + find['apellido'].ljust(20) + str(find['valor']).ljust(15)
                gotoxy(15,11);print(client_info)
                gotoxy(10,12);print(cyan_color + "█" * len(headers) + reset_color)
                    
            gotoxy(4,14);print(cyan_color+"Está seguro de eliminar el cliente? (s/n): ")
            gotoxy(50,14);procesar = input().lower()

            if procesar == "s":
                delete = json_file.delete('dni',dni)
                if delete:
                    gotoxy(20,15);print("😊 Cliente eliminado 😊"+reset_color)
                    gotoxy(4,16);input("Presione una tecla para continuar...") 
            else:
                gotoxy(20,15);print("❗El cliente no será eliminado❗"+reset_color) 
                gotoxy(4,16);input("Presione una tecla para continuar...")    
            time.sleep(2)
        else:
            gotoxy(35,6);print("Cliente no existente")
            time.sleep(1)
            
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(cyan_color + "█"*90)
        gotoxy(2,2);print("██" + " " * 32 + "Consulta de Clientes" + " " * 34 + "██")

        # Mostrar lista de clientes
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.read()
        gotoxy(15,5);print(cyan_color + "Lista de Clientes" + reset_color)
        gotoxy(15,6);print("-" * 60)
        gotoxy(15,7);print("DNI".ljust(15) + "NOMBRE".ljust(20) + "APELLIDO".ljust(20) + "VALOR".ljust(15))
        gotoxy(15,8);print("-" * 60)

        row = 9
        for client in clients:
            gotoxy(15,row);print(client['dni'].ljust(15) + client['nombre'].ljust(20) + client['apellido'].ljust(20) + str(client['valor']).ljust(15))
            row += 1

        # Solicitar DNI del cliente para la consulta más detallada
        gotoxy(8,row+5);print("Ingrese DNI del Cliente: ", end='')
        validar = Valida()
        client_dni = validar.cedula("Solo números", 37, row+5)

        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.find("dni", client_dni)
        if clients:
            gotoxy(15,row+7);print(cyan_color + "DNI".ljust(15) + "NOMBRE".ljust(20) + "APELLIDO".ljust(20) + "VALOR".ljust(15))
            gotoxy(15,row+8);print("-" * 60)

            # Detalles del cliente
            for client in clients:
                gotoxy(15,row+9);print(client['dni'].ljust(15) + client['nombre'].ljust(20) + client['apellido'].ljust(20) + str(client['valor']).ljust(15) + reset_color)
            gotoxy(30,row+12);print("😊 Gracias por consultar 😊")
        else:
            gotoxy(2,row+7);print(cyan_color + "El cliente con el DNI proporcionado no se encuentra." + reset_color)

        # Pie de página
        gotoxy(2,row+10);print(cyan_color + "█" * 90 + reset_color)
        gotoxy(3,row+13);input("Presione una tecla para continuar...")

class CrudProducts(ICrud):
    def create(self):
        
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(cyan_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Registro de Producto"+" "*32+"██")
        
        # Obtener datos del nuevo producto
        validar = Valida()

        gotoxy(7,4); print("Ingrese el nombre del producto:")
        nombre=validar.solo_letras("El nombre del producto solo puede contener letras",40,4)
        gotoxy(7,5); print("Ingrese el precio del producto:")
        precio=validar.solo_decimales("El precio del producto debe ser un número",40,5)
        gotoxy(7,6); print("Ingrese el stock:")
        stock=validar.solo_numeros("Por favor, ingrese un número válido.",40,6)
        
        # Generar un ID único para el nuevo producto
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()
        if products:
            last_id = max(product["id"] for product in products)
            new_id = last_id + 1
        else:
            new_id = 1
        
        # Crear instancia de la clase Product con los datos ingresados
        new_product = Product(new_id, nombre, precio, stock)
        
        # Guardar el nuevo producto en el archivo JSON de productos
        products.append(new_product.getJson())
        json_file.save(products)
    
        gotoxy(7,7);print("Producto registrado exitosamente con ID:", new_id)
        gotoxy(30,9);input("Presione Enter para continuar...")
        
    
    def update(self):
        
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(cyan_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Actualización de Producto"+" "*27+"██")
        validar= Valida()

        gotoxy(7,4); print("Ingrese el ID del producto que desea actualizar: ")
        product_id = validar.solo_numeros("Por favor, ingrese un número válido.",60,4)
        
        #product_id = int(input("Ingrese el ID del producto que desea actualizar: "))
        
        # Buscar el producto en el archivo JSON de productos
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()
        product_to_update = None
        for product in products:
            if product["id"] == product_id:
                product_to_update = product
                break
        
        if product_to_update:
    # Verificar que las claves existan antes de acceder a ellas
            if "descripcion" in product_to_update:
                gotoxy(7,5);print("Nombre:", product_to_update["descripcion"])
            if "precio" in product_to_update:
                gotoxy(7,6);print("Precio:", product_to_update["precio"])
            if "stock" in product_to_update:
                gotoxy(7,7);print("Stock:", product_to_update["stock"])
    
    # Solicitar la nueva información del producto
            gotoxy(7,8); print("Ingrese el nuevo nombre del producto (deje vacío si no desea actualizar): ")
            nuevo_nombre=validar.solo_letras("El nombre del producto solo puede contener letras",80,8)

            gotoxy(7,9); print("Ingrese el nuevo precio del producto (deje vacío si no desea actualizar): ")
            nuevo_precio=validar.solo_decimales("El precio del producto debe ser un número",80,9)

            gotoxy(7,10); print("Ingrese el nuevo stock del producto (deje vacío si no desea actualizar): ")
            nuevo_stock=validar.solo_numeros("Por favor, ingrese un número válido.",80,10)

    # Actualizar la información del producto si se proporciona
            if nuevo_nombre:
                product_to_update["descripcion"] = nuevo_nombre
            if nuevo_precio:
                product_to_update["precio"] = float(nuevo_precio)
            if nuevo_stock:
                product_to_update["stock"] = int(nuevo_stock)

    # Guardar los cambios en el archivo JSON de productos
            json_file.save(products)
    
            gotoxy(30,12);print("Producto actualizado exitosamente. :3")
        else:
            gotoxy(18,12);print("No se encontró ningún producto con el ID proporcionado.")
        
        gotoxy(34,14);input("Presione Enter para continuar...")
    
    def delete(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(cyan_color+"*"*90+reset_color)
        gotoxy(30,2);print(cyan_color+"Eliminación de Producto")
        
        json_file = JsonFile(path+'/archivos/products.json')
        invoices1 = json_file.read()
        
        #Impresión de los productos
        ancho_consola = 80
        gotoxy(2,3);print("Productos:")
        print("-" * ancho_consola)

        # Encabezados de las columnas
        print(f"{'ID'.center(10)}{'Descripción'.center(20)}{'Precio'.center(15)}{'Stock'.center(10)}")
        print("-" * ancho_consola)

        # Para cada producto, imprime los detalles en columnas alineadas
        for product in invoices1:
            print(f"{str(product['id']).center(10)}{product['descripcion'].center(20)}{str(product['precio']).center(15)}{str(product['stock']).center(10)}")
            
        gotoxy(4,20);product_id = input("Ingrese el ID del producto que desea eliminar: ")
        
        # Buscar el producto en el archivo JSON de productos
        if product_id.isdigit():
            invoices1 = json_file.delete("id",int(product_id))
            print(invoices1)
            gotoxy(4,16);input("Presione una tecla para continuar...") 

        else:
            gotoxy(20,15);print(cyan_color+"❗El ID no es válido❗"+reset_color)  
            print("No ingresó el id correspondiente.... intentelo mas tarde...")  
            time.sleep(3)
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(cyan_color+"█"*90)
        gotoxy(2,2);print("██"+" "*32+"Consulta de Producto"+" "*34+"██")

        # Mostrar lista de productos
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()
        gotoxy(15,5);print(cyan_color + "Lista de Productos" + reset_color)
        gotoxy(15,6);print("-" * 60)
        gotoxy(15,7);print("ID".ljust(10) + "DESCRIPCIÓN".ljust(25) + "PRECIO".ljust(15) + "STOCK".ljust(10))
        gotoxy(15,8);print("-" * 60)

        total_precio = 0
        total_stock = 0
        row = 9
        for product in products:
            gotoxy(15,row);print(str(product['id']).ljust(10) + product['descripcion'].ljust(25) + f"{product['precio']:.2f}".ljust(15) + str(product['stock']).ljust(10))
            total_precio += product['precio']
            total_stock += int(product['stock'])  # Convertir stock a entero
            row += 1

        # Mostrar la suma total de precio y stock
        gotoxy(15,row+2);print(f"Total del Precio: {total_precio:.2f}".ljust(40))
        gotoxy(15,row+3);print(f"Total del Stock: {total_stock}".ljust(40))

        # Solicitar ID del producto para la consulta
        gotoxy(8,row+5);print("Ingrese ID del Producto: ", end='')
        validar = Valida()
        product_id = validar.solo_numeros("Solo numeros", 37, row+5)

        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.find("id", int(product_id))
        if products:
            gotoxy(15,row+7);print(cyan_color+"ID".ljust(10) + "DESCRIPCIÓN".ljust(25) + "PRECIO".ljust(15) + "STOCK".ljust(10))
            gotoxy(15,row+8);print("-" * 60)

            # Detalles del producto
            for product in products:
                gotoxy(15,row+9);print(str(product['id']).ljust(10) + product['descripcion'].ljust(25) + f"{product['precio']:.2f}".ljust(15) + str(product['stock']).ljust(10)+reset_color)
            gotoxy(30,row+12);print("😊 Gracias por consultar 😊")
        else:
            gotoxy(2,row+7);print(cyan_color + "El producto con el ID proporcionado no se encuentra." + reset_color)

        # Pie de página
        gotoxy(2,row+10);print(cyan_color + "█" * 90 + reset_color)
        gotoxy(3,row+13);input("Presione una tecla para continuar...")  


class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')

        gotoxy(2,1);print(cyan_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Registro de Venta"+" "*35+"██")
        
        gotoxy(17,3);print(cyan_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.cedula("Error: debe contener 10 dígitos",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(cyan_color+"*"*90+reset_color) 
        gotoxy(5,9);print(cyan_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line)
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(cyan_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(cyan_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
        time.sleep(2)    
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(cyan_color+"█"*90)
        gotoxy(2,2);print(cyan_color+"██"+" "*34+"Consulta de Venta"+" "*35+"██")
        json_file = JsonFile(path+'/archivos/invoices.json')
        gotoxy(2,2);invoices = json_file.read()
        
        #Mostrar las facturas
        gotoxy(42,3);print(cyan_color+"Facturas"+reset_color)
        gotoxy(9,5);print(f"{'ID'.ljust(10)}{'Fecha'.ljust(20)}{'Cliente'.ljust(30)}{'Total'.rjust(10)}")
        gotoxy(7,6);print("█" * 80)

        f = 7
        for fac in invoices:
            id_str = str(fac['factura']).ljust(10)
            fecha_str = fac['Fecha'].ljust(20)
            cliente_str = fac['cliente'].ljust(30)
            total_str = f"{fac['total']:.2f}".rjust(10) 
            gotoxy(9, f);print(f"{id_str}{fecha_str}{cliente_str}{total_str}")
            f += 1
        gotoxy(7, 12);invoice = input("Ingrese el ID: ")
        borrarPantalla()
        
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            gotoxy(30,1);print(f"IMPRESIÓN DE LA FACTURA")
            gotoxy(2,2);print(cyan_color+"█"*90+reset_color)
            for fac in invoices:
                gotoxy(5,4);print(f"Factura#: {fac['factura']} {''*3} Fecha:{fac['Fecha']}")
                gotoxy(5,6);print(f"Comprador: {fac['cliente']}")
                gotoxy(66,4);print(f"Subtotal: {fac['subtotal']}")
                gotoxy(66,5);print(f"Decuento: {fac['descuento']}")
                gotoxy(66,6);print(f"Iva     : {fac['iva']}")
                gotoxy(66,7);print(f"Total   : {fac['total']}")
                gotoxy(2,9);print(cyan_color+"█"*90+reset_color) 
                gotoxy(5,10);print(cyan_color) 
                gotoxy(12,10);print("Articulo") 
                gotoxy(24,10);print("Precio") 
                gotoxy(38,10);print("Cantidad") 
                gotoxy(48,10);print("Subtotal") 
                gotoxy(58,10);print(reset_color)
                gotoxy(5,10);print(cyan_color) 
                d=11
                for det in fac['detalle']:
                    gotoxy(12,d);print(det['poducto']) 
                    gotoxy(24,d);print(det['precio']) 
                    gotoxy(38,d);print(det['cantidad']) 
                    gotoxy(48,d);print(det['precio']*det['cantidad']) 
                    d+=1
                gotoxy(58,d);print(reset_color)
                
            x=input("presione una tecla para continuar...")    
        else:    
            print("regresando.....")
            
    def update(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print(cyan_color+"█"*90)
        gotoxy(2,2);print("██"+" "*31+"Modificación de Factura"+" "*32+"██")
        json_file = JsonFile(path+'/archivos/invoices.json')
        gotoxy(2,2);invoices = json_file.read()
        
        #Mostrar las facturas
        gotoxy(9,6);print(f"{'ID'.ljust(10)}{'Fecha'.ljust(20)}{'Cliente'.ljust(30)}{'Total'.rjust(10)}")
        gotoxy(7,7);print("-" * 80)
        f = 8
        for fac in invoices:
            id_str = str(fac['factura']).ljust(10)
            fecha_str = fac['Fecha'].ljust(20)
            cliente_str = fac['cliente'].ljust(30)
            total_str = f"{fac['total']:.2f}".rjust(10) 
            gotoxy(9, f);print(f"{id_str}{fecha_str}{cliente_str}{total_str}")
            f += 1
        gotoxy(2,4);print("Ingrese el ID de la factura a actualizar: ")
        gotoxy(2,4);invoice_number = validar.solo_numeros("Error: Solo Numeros",44,4)
        borrarPantalla()
        
        if str(invoice_number).isdigit(): 
            invoice_number = int(invoice_number)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            invoice_found = False
            for invoice in invoices:
                if invoice["factura"] == invoice_number:
                    invoice_found = True

                    gotoxy(2,1);print(cyan_color+"█"*90)
                    gotoxy(2,2);print("██"+" "*85+" "+"██")
                    gotoxy(2,3);print("██"+" "*30+f"Impresion de la Factura#{invoice_number}"+" "*31+"██")
                    gotoxy(5,5);print("█" * 84)  # Agrega una línea divisoria para resaltar el comienzo de la factura

                    # Definir la longitud máxima de las etiquetas para alinear los valores
                    max_label_length = max(len(key) for key in invoice if key != 'detalle') + 1  

                    for key, value in invoice.items():
                        if key == 'detalle':
                            print(f"{key.title()}:") 
                            for i, detalle in enumerate(value, start=1):
                                print(f"Detalle {i}:")
                                for d_key, d_value in detalle.items():
                                    print(f"{' ' * 4}{d_key.title().ljust(max_label_length - 4)}: {d_value}")
                        else:
                            print(f"{key.title().ljust(max_label_length)}: {value}")

                    print("-" * 30)  # Agrega una línea divisoria al final de la factura
                    x=input("Presione una tecla para continuar...")
                    borrarPantalla() 
                    print('\033c', end='')
                    gotoxy(2,1);print(cyan_color+"█"*90)
                    gotoxy(2,2);print("██"+" "*34+"Actualización de Factura"+" "*28+"██") 
                    gotoxy(7,4);print("¿Qué desea actualizar?")
                    gotoxy(7,5);print("1. Fecha")
                    gotoxy(7,6);print("2. Cliente")
                    gotoxy(7,7);print("3. Subtotal")
                    gotoxy(7,8);print("4. Descuento")
                    gotoxy(7,9);print("5. Iva")
                    gotoxy(7,10);print("6. Total")
                    # gotoxy(5,11);print("7. Detalle (Agregar/Actualizar/Eliminar)")
                    gotoxy(7,11);print("7. Cancelar")
                    
                    gotoxy(7,13);print('Seleccione una opción:',end="")
                    gotoxy(7,13);opcion = validar.solo_numeros("Error: Solo numeros",30, 13)
                    opcion = str(opcion)
                    if opcion == '1':
                        gotoxy(7,14);nueva_fecha = input("Ingrese la nueva fecha (YYYY-MM-DD): ")
                        gotoxy(7,14);opcion = validar.validar_fecha("Error: Fecha incorrecta",30, 14)
                        invoice["Fecha"] = nueva_fecha
                        
                    elif opcion == '2':
                        gotoxy(7,14);print("Ingrese el nombre del cliente: ")
                        nuevo_cliente = validar.solo_letras("Error: Solo letras",32,14).lower().capitalize()
                        # Verificar si el campo se ha modificado
                        if nuevo_cliente:
                            invoice["cliente"] = nuevo_cliente
                        else:
                            print("El cliente no ha sido modificado. Manteniendo el valor actual.")

                    elif opcion == '3':
                        gotoxy(7,14);print("Ingrese el nuevo subtotal: ")
                        gotoxy(7,14);nuevo_subtotal = validar.solo_decimales("Error: Solo numeros",32,14) 
                        invoice["subtotal"] = float(nuevo_subtotal)
                        
                    elif opcion == '4':
                        gotoxy(7,14);print("Ingrese el nuevo descuento: ")
                        gotoxy(7,14);nuevo_descuento = validar.solo_decimales("Error: Solo numeros",34,14) 
                        invoice["descuento"] = float(nuevo_descuento)
                        
                    elif opcion == '5':
                        gotoxy(7,14);print("Ingrese el nuevo IVA: ")
                        gotoxy(7,14);nuevo_iva = validar.solo_decimales("Error: Solo numeros",29,14) 
                        invoice["iva"] = float(nuevo_iva)
                        
                    elif opcion == '6':
                        gotoxy(7,14);print("Ingrese el nuevo total: ")
                        gotoxy(7,14);nuevo_total = validar.solo_decimales("Error: Solo numeros",32,14)
                        invoice["total"] = float(nuevo_total)
                        
                    elif opcion == '7':
                        print("Operación de actualización cancelada.")
                        break
                    else:
                        gotoxy(7,14);print("Opción no válida.")
                        break
                    
                    json_file.save(invoices)
                    gotoxy(24,14);print("Factura actualizada exitosamente.")
                    break

            if not invoice_found:
                print(f"No se encontró la factura con el número {invoice_number}.")
        else:
            print("Por favor, ingrese un número de factura válido.")
        gotoxy(7,16);input("Presione una tecla para continuar...")
        
    def delete(self):
        print('\033c', end='')
        gotoxy(2,1);print(cyan_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Eliminar factura"+" "*36+"██")
        json_file = JsonFile(path+'/archivos/invoices.json')
        invoices1 = json_file.read()

        gotoxy(42,3);print("FACTURAS")
        gotoxy(9,5);print(f"{'ID'.ljust(10)}{'Fecha'.ljust(20)}{'Cliente'.ljust(30)}{'Total'.rjust(10)}")
        gotoxy(7,6);print("-" * 80)

        f = 7
        for fac in invoices1:
            id_str = str(fac['factura']).ljust(10)
            fecha_str = fac['Fecha'].ljust(20)
            cliente_str = fac['cliente'].ljust(30)
            total_str = f"{fac['total']:.2f}".rjust(10) 
            gotoxy(9, f);print(f"{id_str}{fecha_str}{cliente_str}{total_str}")
            f += 1
        print(reset_color)
        
        invoice= input("\tIngrese Factura a eliminar: ")
        if invoice.isdigit():
            invoices = json_file.delete("factura",int(invoice))
            print(invoices)
        else:
            print("No ingreso el id correspondiente.... intentelo mas tarde...")

#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()    
            cliente = CrudClients()
            menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                cliente.create()

            elif opc1 == "2":
                cliente.update()
      
            elif opc1 == "3":
                cliente.delete()
            elif opc1 == "4":
                cliente.consult()
            print("Regresando al menu Clientes...")
            # time.sleep(2)            
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()    
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            products_crud=CrudProducts()

            if opc2 == "1":
                products_crud.create()
            elif opc2 == "2":
                products_crud.update()
            elif opc2 == "3":
                products_crud.delete()
            elif opc2 == "4":
                products_crud.consult()
            
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
                
            elif opc3 == "2":
                sales.consult()
            elif opc3 == "3":
                sales.update()
            elif opc3 == "4":
                sales.delete()
     
    print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()

