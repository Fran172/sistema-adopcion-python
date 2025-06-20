if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.perro import Perro, Raza
from modules.usuario import UsuarioAdoptante

class SistemaAdopcion:
    # Singletone
    instance = None
    def __new__(cls):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
            cls.instance.__init__()
        return cls.instance

    def __init__(self):
        self.perros = []
        self.razas = []
        self.usuarios = []
        self.id_proximo_perro = 1

    # validar datos en sistema
    def hay_usuarios(self):
        '''Verifica que haya usuarios en el sistema, ValueError si no hay'''
        if self.usuarios:
            return True
        raise ValueError("El sistema no tiene usuarios registrados")

    def hay_perros(self):
        '''Verifica que haya perros en el sistema, ValueError si no hay'''
        if self.perros:
            return True
        raise ValueError("El sistema no tiene perros registrados")

    def hay_razas(self):
        '''Verifica que haya razas en el sistema, ValueError si no hay'''
        if self.razas:
            return True
        raise ValueError("El sistema no tiene razas registradas")

    # Buscar en sistema
    def buscar_usuario(self, usuario_buscado:str|int|UsuarioAdoptante|None, error:bool=True):
        '''Busca un usuario y lo retornda. Si no encuentra, retorna None o ValueError (si error=True)'''
        if usuario_buscado is None:
            return None
        if isinstance(usuario_buscado, UsuarioAdoptante):
            usuario_buscado = usuario_buscado.dni
        elif isinstance(usuario_buscado, int):
            usuario_buscado = str(usuario_buscado)
        if not isinstance(usuario_buscado, str):
            raise TypeError("DNI inválido: debe ser un string, int u objeto del tipo 'UsuarioAdoptado'")
        usuario_buscado = usuario_buscado.strip().lower()
        for usuario in self.usuarios:
            if usuario.dni == usuario_buscado:
                return usuario
        if error:
            raise ValueError(f"No se encontró '{usuario_buscado}'. Intente nuevamente")
        return None

    def buscar_perro(self, perro_buscado:str|int|Perro|None, error:bool=True):
        '''Busca un perro y lo retorna. Si no encuentra, retorna None o ValueError (si error=True)'''
        if perro_buscado is None:
            return None
        elif isinstance(perro_buscado, Perro):
            if perro_buscado.id is None:
                return None
            perro_buscado = perro_buscado.id
        elif isinstance(perro_buscado, str):
            try:
                perro_buscado = int(perro_buscado)
            except TypeError:
                raise TypeError("ID debe ser un número entero")
        if not isinstance(perro_buscado, int):
            raise TypeError("ID inválido: debe ser un string, int u objeto del tipo 'Perro'")
        for perro in self.perros:
            if perro.id == perro_buscado:
                return perro
        if error:
            raise ValueError(f"No se encontró '{perro_buscado}'. Intente nuevamente")
        return None

    def buscar_raza(self, raza_buscada:str|Raza, error:bool=True):
        '''Busca una raza y la retorna. Si no encuentra, retorna None o ValueError (si error=True)'''
        if isinstance(raza_buscada, Raza):
            raza_buscada = raza_buscada.nombre
        if not isinstance(raza_buscada, str):
            raise TypeError("Raza inválida: debe ser un string u objeto del tipo 'Raza'")
        raza_buscada = raza_buscada.strip().title()
        for raza in self.razas:
            if raza.nombre == raza_buscada:
                return raza
        if error:
            raise ValueError(f"No se encontró '{raza_buscada}'. Intente nuevamente")
        return None

    # registrar en sistema
    def registrar_usuario(self, usuario_nuevo:UsuarioAdoptante):
        '''Agrega un nuevo usuario al sistema y lo retorna'''
        # Valida usuario
        if not isinstance(usuario_nuevo, UsuarioAdoptante):
            raise TypeError("Debe ingresar un objeto de la clase 'UsuarioAdoptante'")
        if self.usuarios and self.buscar_usuario(usuario_nuevo, False):
            raise ValueError(f"Ya existe un usuario con DNI {usuario_nuevo.dni}")
        # Registra usuario
        self.usuarios.append(usuario_nuevo)
        return usuario_nuevo

    def registrar_perro(self, perro_nuevo:Perro):
        '''Agrega un nuevo perro al sistema y lo retorna con ID'''
        # Valida perro
        if not isinstance(perro_nuevo, Perro):
            raise TypeError("Debe ingresar un objeto de la clase 'Perro'")
        if self.perros and self.buscar_perro(perro_nuevo, False):
            raise ValueError(f"Ya existe un perro con ID {perro_nuevo.id}")
        # Asigna ID
        if not perro_nuevo.id:
            perro_nuevo.id = self.id_proximo_perro
            self.id_proximo_perro += 1
        # Registra perro
        self.perros.append(perro_nuevo)
        return perro_nuevo

    def registrar_raza(self, raza_nueva:Raza):
        '''Agrega una nueva raza al sistema y la retorna'''
        # Valida raza
        if not isinstance(raza_nueva, Raza):
            raise TypeError("Debe ingresar un objeto de la clase 'Raza'")
        if self.razas and self.buscar_raza(raza_nueva, False):
            raise ValueError(f"Ya existe la raza {raza_nueva.nombre}")
        # Registrar raza
        self.razas.append(raza_nueva)
        return raza_nueva

    # Eliminar del sistema
    def eliminar_usuario(self, dni_usuario:str|int|UsuarioAdoptante):
        '''Elimina a un usuario y a sus perros del sistema'''
        if self.hay_usuarios():
            usuario:UsuarioAdoptante = self.buscar_usuario(dni_usuario, False)
            if not usuario:
                raise ValueError("No se encontró al usuario en el sistema")
            # Elimina sus perros
            perros_adoptados = usuario.historial_adopciones
            for perro in perros_adoptados:
                self.eliminar_perro(perro)
            # Cancela reserva
            if usuario.reserva:
                perro = self.buscar_perro(usuario.reserva)
                self.devolver(usuario.reserva, usuario)
            # Elimina usuario
            self.usuarios.remove(usuario)

    def eliminar_perro(self, id_perro:int|Perro):
        '''Elimina a un perro del sistema y lo borra del historial de su dueño'''
        if self.hay_perros():
            perro:Perro = self.buscar_perro(id_perro, False)
            if not perro:
                raise ValueError("No se encontró al perro en el sistema")
            # Remueve al perro del dueño o reserva
            if perro.adoptante:
                self.devolver(perro, perro.adoptante)
            # Elimina perro
            self.perros.remove(perro)

    # Adopciones
    def adoptar(self, id_perro:int|Perro, dni_usuario:str|int|UsuarioAdoptante):
        if self.hay_perros() and self.hay_usuarios():
            perro = self.buscar_perro(id_perro, False)
            usuario = self.buscar_usuario(dni_usuario, False)
            if not perro:
                raise ValueError("No se encontró al perro en el sistema")
            if not usuario:
                raise ValueError("No se encontró al usuario en el sistema")
            if not usuario.puede_adoptar(perro.id) or not perro.puede_adoptar(usuario.dni):
                raise ValueError("No puede adoptar sin una reserva")
            usuario.adoptar(perro.id)
            perro.adoptar(usuario.dni)
            return True

    def reservar(self, id_perro:int|Perro, dni_usuario:str|int|UsuarioAdoptante):
        if self.hay_perros() and self.hay_usuarios():
            perro = self.buscar_perro(id_perro, False)
            usuario = self.buscar_usuario(dni_usuario, False)
            if not perro:
                raise ValueError("No se encontró al perro en el sistema")
            if not usuario:
                raise ValueError("No se encontró al usuario en el sistema")
            if not usuario.puede_reservar(perro.id) or not perro.puede_reservar(usuario.dni):
                raise ValueError("No puede reservar teniendo una reserva previa")
            usuario.reservar(perro.id)
            perro.reservar(usuario.dni)
            return True

    def devolver(self, id_perro:int|Perro, dni_usuario:str|int|UsuarioAdoptante):
        if self.hay_perros() and self.hay_usuarios():
            perro = self.buscar_perro(id_perro, False)
            usuario = self.buscar_usuario(dni_usuario, False)
            if not perro:
                raise ValueError("No se encontró al perro en el sistema")
            if not usuario:
                raise ValueError("No se encontró al usuario en el sistema")
            if not usuario.puede_devolver(perro.id) or not perro.puede_devolver(usuario.dni):
                raise ValueError("No puede devolver perros ajenos...")
            usuario.devolver(perro.id)
            perro.devolver(usuario.dni)
            return True

    # Filtrar perros
    def obtener_sugerencias_perros(self, usuario:str|int|UsuarioAdoptante):
        '''Retorna lista de perros en base a las preferencias de un usuario'''
        if self.hay_perros() and self.hay_usuarios():
            # Valida usuario
            usuario = self.buscar_usuario(usuario, False)
            if not usuario:
                raise ValueError(f"No se encontró al usuario en el sistema")
            # Filtra perros
            perros_filtrados = []
            for perro in self.perros:
                if not usuario.preferencias.raza or usuario.preferencias.raza == perro.raza.nombre:
                    if not usuario.preferencias.edad or usuario.preferencias.edad == usuario.preferencias.validar_edad(perro.edad):
                        if not usuario.preferencias.tamanio or usuario.preferencias.tamanio == perro.raza.tamanio:
                            if perro.id not in usuario.historial_adopciones and perro.estado == "disponible":
                                perros_filtrados.append(perro)
            return perros_filtrados

    def obtener_historial_perros(self, usuario:str|int|UsuarioAdoptante):
        '''Retorna lista de perros adoptados por un usuario'''
        if self.hay_perros() and self.hay_usuarios():
            # Valida usuario
            usuario = self.buscar_usuario(usuario, False)
            if not usuario:
                raise ValueError(f"No se encontró al usuario en el sistema")
            # Filtra perros
            perros_filtrados = []
            for perro in self.perros:
                if perro.id in usuario.historial_adopciones:
                    perros_filtrados.append(perro)
            return perros_filtrados

    def obtener_estado_perros(self, estado:str):
        '''Retorna lista de perros adoptados, reservados o disponibles'''
        if self.hay_perros():
            if estado in ("disponible", "reservado", "adoptado"):
                perros_filtrados = []
                for perro in self.perros:
                    if perro.estado == estado:
                        perros_filtrados.append(perro)
                return perros_filtrados
            raise ValueError(f"El estado '{estado}' no está registrado. Opciones: ['disponible', 'reservado', 'adoptado']")


