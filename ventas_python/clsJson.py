import json
class JsonFile:
    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)# dump:graba datos a un archivo json
      
    def read(self):
        try:
            with open(self.filename,'r') as file:
                data = json.load(file)# load:carga datos desde un archivo json
        except FileNotFoundError:
            data = []
        return data
     
    def find(self,atributo,buscado):
        try:
            with open(self.filename,'r') as file:
                datas = json.load(file)
                data = [item for item in datas if item[atributo] == buscado ]
        except FileNotFoundError:
            data = []
        return data
    def delete(self,atributo,buscado):
        try:
            # Buscar los elementos a eliminar 
            items_to_delete = self.find(atributo, buscado)
            if items_to_delete:
                # Obtener los datos actuales del archivo items_to_delete
                datas = self.read()
                
                # Verificar si el atributo es un identificador de secuencia (como un número)
                identificador = atributo
                es_secuencia = all(isinstance(item[identificador], int) for item in items_to_delete)
                
                # Eliminar los elementos encontrados de la lista original
                for item in items_to_delete:
                    if identificador in item:
                        datas = [data for data in datas if data[identificador] != item[identificador]]
                
                # Reorganizar los identificadores solo si el atributo es un identificador de secuencia
                if es_secuencia and any(item[identificador] != max(data[identificador] for data in datas) for item in items_to_delete):
                    for i, item in enumerate(datas):
                        item[identificador] = i + 1
                # Guardar los cambios de vuelta al archivo JSON
                self.save(datas)
                
                mensaje="Elementos eliminados exitosamente."
            else:
                mensaje = "No se encontraron elementos para eliminar."
        
        except FileNotFoundError:
            mensaje="Archivo no encontrado."
        return mensaje
    