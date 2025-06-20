if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.perro import Raza

class Usuario:
    def __init__(self, nombre:str, dni:str|int, email:str):
        self.nombre = self.validar_nombre(nombre)
        self.dni = self.validar_dni(dni)
        self.email = self.validar_email(email)

    # Validar atributos
    @staticmethod # el método no necesitará instancia (self)
    def validar_nombre(nombre):
        if not isinstance(nombre, str) :
            raise TypeError(f"El nombre de la raza debe ser un string")
        nombre = nombre.strip().title()
        if nombre == "":
            raise TypeError(f"El nombre de la raza no puede estar vacío")
        return nombre

    @staticmethod
    def validar_dni(dni):
        if not isinstance(dni, (str, int)):
            raise TypeError("DNI debe ser un string o int")
        dni = str(dni).strip().lower()
        if len(dni) != 8:
            raise ValueError("DNI debe contener 8 caracteres")
        return dni

    @staticmethod
    def validar_email(email):
        if not isinstance(email, str) or len(email.strip()) == 0:
            raise ValueError("Email debe ser un string no vacío")
        if email.count('@') != 1 or '.' not in email:
            raise ValueError("Email debe contener '@' y '.'")
        return email

    # Cambiar datos
    def cambiar_nombre(self, nombre:str):
        self.nombre = self.validar_nombre(nombre)

    def cambiar_email(self, email:str):
        self.email = self.validar_email(email)

    # Mostrar datos
    def mostrar_datos_personales(self):
        return f"Nombre: {self.nombre}\nDNI: {self.dni}\nEmail: {self.email}"

    def __str__(self):
        return self.mostrar_datos_personales()


class Preferencias:
    EDADES = {
        'C':'Cachorro',
        'J':'Joven',
        'A':'Adulto',
        'M':'Adulto Mayor',
    }
    def __init__(self, raza:str="", edad:int|str="", tamanio:str=""):
        self.raza = self.validar_raza(raza)
        self.edad = self.validar_edad(edad)
        self.tamanio = self.validar_tamanio(tamanio)

    # Validar atributos
    @staticmethod
    def validar_raza(raza:str):
        if not isinstance(raza, str):
            raise TypeError("La raza debe ser un string")
        return raza.strip().title()

    @staticmethod
    def validar_edad(edad:int|str):
        if not edad:
            return edad
        try:
            edad = int(edad)
            if edad < 1:
                return "C"
            if edad < 3:
                return "J"
            if edad < 7:
                return "A"
            return "M"
        except ValueError:
            raise ValueError("Edad debe ser un número entero")

    @staticmethod
    def validar_tamanio(tamanio:str): # (S/M/L/X)
        if not isinstance(tamanio, str):
            raise TypeError("Tamaño debe ser un string")
        tamanio = tamanio.strip().title()
        if tamanio == "":
            return tamanio
        for clave, valor in Raza.TAMANIOS.items():
            if tamanio in (clave, valor):
                return clave
        raise ValueError(f"El tamaño '{tamanio}' no está registrado. Opciones disponibles: {list(Raza.TAMANIOS.values())}")

    # Cambiar atributos
    def cambiar_raza(self, raza):
        self.raza = self.validar_raza(raza)

    def cambiar_edad(self, edad):
        self.edad = self.validar_edad(edad)

    def cambiar_tamanio(self, tamanio):
        self.tamanio = self.validar_tamanio(tamanio)

    # Mostrar datos
    def mostrar_preferencias(self):
        raza, edad, tamanio = ("Todas", "Todas", "Todos")
        if self.raza:
            raza = self.raza
        if self.edad:
            edad = self.EDADES[self.edad]
        if self.tamanio:
            tamanio = Raza.TAMANIOS[self.tamanio]
        return f"Preferencias:\n- Edad: {edad}\n- Tamaño: {tamanio}\n- Raza: {raza}"

    def __str__(self):
        return self.mostrar_preferencias()




class UsuarioAdoptante(Usuario):
    def __init__(self, nombre:str, dni:str|int, email:str, pref_raza:str="", pref_edad:str="", pref_tamanio:str=""):
        super().__init__(nombre, dni, email) # Herencia
        self.preferencias = Preferencias(pref_raza, pref_edad, pref_tamanio) # Composición (Preferencias solo existe dentro de UsuarioAdoptante)
        self.historial_adopciones = []
        self.reserva = None

    # Validar atributos
    def validar_preferencias(self, preferencias):
        if not isinstance(preferencias, Preferencias):
            raise TypeError("Preferencias debe ser un objeto de tipo 'Preferencias'")
        return preferencias

    # Verificar adopciones
    def puede_adoptar(self, id_perro:int):
        '''Verifica que el usuario haya reservado al perro y no sea el dueño'''
        if not isinstance(id_perro, int):
            raise TypeError("El ID debe ser de tipo entero")
        return self.reserva == id_perro and id_perro not in self.historial_adopciones

    def puede_reservar(self, id_perro:int):
        '''Verifica que el usuario no sea el dueño'''
        if not isinstance(id_perro, int):
            raise TypeError("El ID debe ser de tipo entero")
        return id_perro not in self.historial_adopciones

    def puede_devolver(self, id_perro:int):
        '''Verifica que el usuario sea dueño del perro o lo tenga reservado'''
        if not isinstance(id_perro, int):
            raise TypeError("El ID debe ser de tipo entero")
        return id_perro in self.historial_adopciones or id_perro == self.reserva

    # Cambiar adopciones
    def adoptar(self, id_perro:int):
        '''Agrega ID del perro al historial de adopciones'''
        if self.puede_adoptar(id_perro):
            self.historial_adopciones.append(id_perro)
            self.reserva = None
            return True
        return False

    def reservar(self, id_perro:int):
        '''Reserva ID del perro, no lo agrega a historial de adopciones'''
        if self.puede_reservar(id_perro):
            self.reserva = id_perro
            return True
        return False

    def devolver(self, id_perro:int):
        '''Remueve ID del perro del historial de adopciones o de la reserva'''
        if self.puede_devolver(id_perro):
            if id_perro == self.reserva:
                self.reserva = None
            else:
                self.historial_adopciones.remove(id_perro)
            return True
        return False

    def mostrar_adopciones(self):
        return f"Perro reservado: {self.reserva}\nPerros Adoptados: {self.historial_adopciones}"

    def __str__(self):
        return (
            f"{self.mostrar_datos_personales()}\n"  # Método heredado de "Usuario"
            f"{self.mostrar_adopciones()}\n"          # Método propio
            f"{self.preferencias.mostrar_preferencias()}" # Método de 
        )


if __name__ == "__main__":
    usuario1 = UsuarioAdoptante(
        nombre = "Tito",
        dni = "12345678",
        email = "a@b.c"
    )
    print("------mostrar------")
    print(usuario1)
    print("------cambiar------")
    usuario1.cambiar_nombre("Tico")
    usuario1.cambiar_email("aaaaaaa@bbbb.ccc")
    usuario1.preferencias.cambiar_raza("    caniche")
    usuario1.preferencias.cambiar_edad("M")
    usuario1.preferencias.cambiar_tamanio("S")
    print(usuario1.mostrar_datos_personales())
    print(usuario1.preferencias)
    print("------reservar------")
    print(usuario1.mostrar_adopciones())
    usuario1.reservar(123)
    print(usuario1.mostrar_adopciones())
    print("------adoptar------")
    usuario1.adoptar(123)
    print(usuario1.mostrar_adopciones())
    print("------devolver------")
    usuario1.devolver(123)
    print(usuario1.mostrar_adopciones())
    print("------errores------")
    usuario1.reservar(123)
    print(usuario1.reservar(123))
    print(usuario1.adoptar(222))
    print(usuario1.devolver(222))
    try:
        # usuario1.cambiar_nombre("")
        usuario1.cambiar_email("ccccd.2")
        # usuario1.preferencias.cambiar_raza(1)
        # usuario1.preferencias.cambiar_edad("joven")
        # usuario1.preferencias.cambiar_tamanio("grande")
        # print(usuario1.reservar("asd"))
        # print(usuario1.adoptar(None))
        # print(usuario1.devolver(""))
        print(usuario1)
    except Exception as e:
        print("[!]", e)
