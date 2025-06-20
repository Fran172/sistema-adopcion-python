class Raza:
    TAMANIOS = {
        'S':'Pequeño',
        'M':'Mediano',
        'L':'Grande',
        'X':'Extra Grande'
    }

    def __init__(self, nombre:str, tamanio:str="", temperamento:str=""):
        self.nombre = self.validar_nombre(nombre)
        self.temperamento = self.validar_temperamento(temperamento)
        self.tamanio = self.validar_tamanio(tamanio)

    # Validar atributos
    @staticmethod # el método no necesitará instancia (self)
    def validar_nombre(nombre:str):
        if not isinstance(nombre, str) :
            raise TypeError(f"El nombre de la raza debe ser un string")
        nombre = nombre.strip().title()
        if nombre == "":
            raise TypeError(f"El nombre de la raza no puede estar vacío")
        return nombre

    @staticmethod
    def validar_temperamento(temperamento:str):
        if not isinstance(temperamento, str):
            raise TypeError(f"El temperamento debe ser un string")
        temperamento = temperamento.strip().capitalize()
        if temperamento == "":
            return "Sorpresa!"
        return temperamento

    @classmethod # método sin self, pero con acceso a atributos de clase
    def validar_tamanio(cls, tamanio):
        if not isinstance(tamanio, str):
            raise TypeError("Tamaño debe ser un string")
        tamanio = tamanio.strip().title()
        if tamanio == "":
            return tamanio
        for clave, valor in cls.TAMANIOS.items():
            if tamanio in (clave, valor):
                return clave
        raise ValueError(f"El tamaño '{tamanio}' no está registrado. Opciones disponibles: {list(cls.TAMANIOS.values())}")

    # Cambiar atributos
    def cambiar_temperamento(self, temperamento):
        self.temperamento = self.validar_temperamento(temperamento)

    def cambiar_tamanio(self, tamanio):
        self.tamanio = self.validar_tamanio(tamanio)

    def __str__(self):
        tamanio, temperamento = ("Sorpresa!", "Sorpresa!")
        if self.tamanio:
            tamanio = self.TAMANIOS[self.tamanio]
        if self.temperamento:
            temperamento = self.temperamento
        return f"Raza: {self.nombre}\nTamaño: {tamanio}\nTemperamento: {temperamento}"


class Perro:
    SEXOS = {
        'M':'Macho',
        'F':'Hembra'
    }
    # EDADES = {
    #     'C':'Cachorro',
    #     'J':'Joven',
    #     'A':'Adulto',
    #     'M':'Adulto Mayor',
    # }
    # ESTADOS = ("disponible", "reservado", "adoptado")

    def __init__(self, nombre:str, edad:int|str, peso:float|str, sexo:str, raza:Raza, vacunado:bool, discapacitado:bool, id:int|None=None):
        self.nombre = self.validar_nombre(nombre)
        self.id = self.validar_id(id)
        self.edad = self.validar_edad(edad)
        self.peso = self.validar_peso(peso)
        self.sexo = self.validar_sexo(sexo)
        self.raza = self.validar_raza(raza) # Agregación (Raza existe fuera de Perro)
        self.vacunado = self.validar_vacunado(vacunado)
        self.discapacitado = self.validar_discapacitado(discapacitado)
        self.estado = "disponible"
        self.adoptante = None

    # Validar atributos
    @staticmethod # método sin self, no necesita instancia para usarse
    def validar_nombre(nombre):
        if not isinstance(nombre, str):
            raise TypeError("Nombre debe ser un string")
        nombre = nombre.strip().title()
        if nombre == "":
            nombre = "Sin nombre"
        return nombre

    @staticmethod
    def validar_id(id):
        if id is not None and not isinstance(id, int):
            raise TypeError("ID debe ser un número entero")
        return id

    @staticmethod
    def validar_edad(edad:int):
        try:
            edad = int(edad)
            if edad < 0:
                raise ValueError
            return edad
        except ValueError:
            raise ValueError("Edad debe ser un número positivo")

    @staticmethod
    def validar_peso(peso):
        try:
            peso = float(peso)
            if not peso > 0:
                raise ValueError
            return peso
        except ValueError:
            raise ValueError("Peso debe ser un número mayor a cero")

    @classmethod
    def validar_sexo(cls, sexo):
        if not isinstance(sexo, str):
            raise TypeError("Sexo debe ser un string")
        sexo = sexo.strip().capitalize()
        for clave, valor in cls.SEXOS.items():
            if sexo in (clave, valor):
                return clave
        raise ValueError(f"El sexo '{sexo}' no está registrado. Opciones disponibles: {list(cls.SEXOS.values())}")

    @staticmethod
    def validar_raza(raza:Raza):
        if not isinstance(raza, Raza):
            raise TypeError("Raza debe ser un objeto del tipo 'Raza'")
        return raza

    @staticmethod
    def validar_vacunado(vacunado):
        if not isinstance(vacunado, bool):
            raise TypeError("Vacunado debe ser un booleano (True o False)")
        return vacunado

    @staticmethod
    def validar_discapacitado(discapacitado):
        if not isinstance(discapacitado, bool):
            raise TypeError("Discapacitado debe ser un booleano (True o False)")
        return discapacitado

    # Cambiar Atributos
    def cambiar_nombre(self, nombre:str):
        self.nombre = self.validar_nombre(nombre)

    def cambiar_edad(self, edad:int):
        self.edad = self.validar_edad(edad)

    def cambiar_peso(self, peso:float):
        self.peso = self.validar_peso(peso)

    def cambiar_sexo(self, sexo:str):
        self.sexo = self.validar_sexo(sexo)

    def cambiar_raza(self, raza:Raza):
        self.raza = self.validar_raza(raza)

    def cambiar_vacunado(self, vacunado:bool):
        self.vacunado = self.validar_vacunado(vacunado)

    def cambiar_discapacitado(self, discapacitado:bool):
        self.discapacitado = self.validar_discapacitado(discapacitado)

    # verificar estado
    def puede_adoptar(self, dni_usuario:str):
        '''Verifica que el perro esté reservado por el usuario'''
        if not isinstance(dni_usuario, str):
            raise TypeError("El DNI debe ser de tipo string")
        return self.estado == "reservado" and self.adoptante == dni_usuario

    def puede_reservar(self, dni_usuario:str):
        '''Verifica que el perro esté disponible y no tenga dueño'''
        if not isinstance(dni_usuario, str):
            raise TypeError("El DNI debe ser de tipo string")
        return self.estado == "disponible" and self.adoptante != dni_usuario

    def puede_devolver(self, dni_usuario:str):
        '''Verifica que el perro esté adoptado o reservado por el usuario'''
        if not isinstance(dni_usuario, str):
            raise TypeError("El DNI debe ser de tipo string")
        return self.estado != "disponible" and self.adoptante == dni_usuario

    # Cambiar estado
    def adoptar(self, dni_usuario:str):
        '''Guarda DNI de adoptante y cambia estado a "adoptado"'''
        if self.puede_adoptar(dni_usuario):
            self.adoptante = dni_usuario
            self.estado = "adoptado"
            return True
        return False

    def reservar(self, dni_usuario:str):
        '''Guarda DNI de posible adoptante y cambia estado a "reservado"'''
        if self.puede_reservar(dni_usuario):
            self.adoptante = dni_usuario
            self.estado = "reservado"
            return True
        return False

    def devolver(self, dni_usuario:str):
        '''Remueve DNI de adoptante y cambia estado a "disponible"'''
        if self.puede_devolver(dni_usuario):
            self.adoptante = None
            self.estado = "disponible"
            return True
        return False

    # Mostrar
    def mostrar_datos_propios(self):
        return f"Nombre: {self.nombre}\nID: {self.id}\nEdad: {self.edad}\nPeso: {self.peso}kg\nSexo: {self.SEXOS[self.sexo]}\nVacunado: {self.vacunado}\nDiscapacitado: {self.discapacitado}"

    def mostrar_estado(self):
        return f"Estado: {self.estado}\nDueño: {self.adoptante}"

    def __str__(self):
        return f"{self.mostrar_datos_propios()}\n{self.raza}\n{self.mostrar_estado()}"


if __name__ == "__main__":
    raza1 = Raza(
        nombre="Chihuahua",
        temperamento="Nervioso",
        tamanio="S"
    )
    perro1 = Perro(
        nombre="Pichichus",
        id=2,
        edad=1,
        peso=1.7,
        sexo="M",
        raza=raza1,
        vacunado=False,
        discapacitado=False
        )

    print("------mostrar------")
    print(perro1)
    print("------cambiar------")
    perro1.cambiar_nombre("  pichicha ")
    perro1.cambiar_edad("5")
    perro1.cambiar_peso("2")
    perro1.cambiar_sexo("F")
    perro1.cambiar_vacunado(True)
    perro1.cambiar_discapacitado(True)
    print(perro1)
    print("------reservar------")
    perro1.reservar("12345678")
    print(perro1.mostrar_estado())
    print("------adoptar------")
    perro1.adoptar("12345678")
    print(perro1.mostrar_estado())
    print("------devolver------")
    perro1.devolver("12345678")
    print(perro1.mostrar_estado())
    print("------errores------")
    perro1.reservar("12345678")
    print(perro1.reservar("12345678"))
    print(perro1.adoptar("87654321"))
    print(perro1.devolver("87654321"))
    try:
        # perro1.cambiar_nombre(1)
        perro1.cambiar_edad("")
        # perro1.cambiar_peso("3")
        # perro1.cambiar_sexo("macho")
        # perro1.cambiar_vacunado("nose")
        # perro1.cambiar_discapacitado("medio")
        # perro1.reservar(12345678)
        # perro1.adoptar(True)
        # perro1.devolver(None)
        print(perro1)
    except Exception as e:
        print("[!]", e)
