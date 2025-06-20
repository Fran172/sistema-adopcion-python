# menu_        : imprime un menú con opciones, solicita que se elija una
# opc_menu_    : lo que hace una de las opciones del menú
# mostrar_     : imprime algo en pantalla
# validar_     : recibe dato, lo verifica y lo devuelve
# solicitar_   : pide input en bucle hasta obtener una validación correcta
# elegir_      : muestra listado y solicita un valor

from modules.perro import Raza, Perro
from modules.usuario import UsuarioAdoptante, Preferencias
from modules.sistema import SistemaAdopcion

# Mostrar en pantalla
def mostrar_objetos(objetos:list, titulo:str, attrs:str|list, vacio:str="No hay"):
    '''Recibe listado de usuarios, perros o razas, los muestra y los retorna. Puede elegir mensajes y atributos.'''
    print(titulo.center(27,"·"))
    if not objetos:
        print(vacio.center(27))
    else:
        for obj in objetos:
            if isinstance(attrs, str):
                print(f" - {attrs}")
            elif len(attrs) == 1:
                print(f" - {getattr(obj, attrs[0])}")
            else:
                valores = []
                for attr in attrs:
                    valores.append(str(getattr(obj, attr)))
                print(f" - {' : '.join(valores)}")
    print("···························")
    return objetos

def mostrar_detalles(texto, titulo):
    '''Da título y marco a información'''
    print("\n"+(" "+titulo+" ").center(27,"·"))
    print(texto)
    print("···························")

def mostrar_menu(titulo:str, opciones:list, salida:str="Volver"):
    '''Genera menú con título y listado de opciones'''
    print("\n---------------------------")
    print("|" + titulo.center(25) + "|")
    print("---------------------------")
    i = 0
    while i < len(opciones):
        print("| " + f"{i+1}" + " | " + f"{opciones[i]}".ljust(20) + "|")
        i += 1
    if salida:
        print(f"[ 0 ] " + f"{salida}".ljust(20) + "|")
    print("---------------------------")

# Validar datos
def validar_bool(valor:str) -> bool:
    '''Por sí o por no. ValueError si falla.'''
    valor = valor.lower().strip()
    if valor in ("s", "si", "sí", "true", "t", "1"):
        return True
    elif valor in ("n", "no", "false", "f", "0"):
        return False
    raise ValueError("Debe ingresar 'si' o 'no', intente nuevamente.")

# Solicitar input en bucle
def solicitar_dato(mensaje, validar_dato):
    '''Solicita input correcto en bucle, recibe función para validarla. Retorna resultado'''
    while True:
        valor = input(mensaje)
        try:
            return validar_dato(valor)
        except Exception as e:
            print("[!]", e)

def solicitar_bool(mensaje="¿Seguro?", opciones="(S/N)"):
    '''Solicita 'S' o 'N' en bucle. Agrega '(S/N): ' al final del mensaje.'''
    return solicitar_dato(f"{mensaje} {opciones}: ", validar_bool)

def solicitar_usuario(mensaje="Ingrese DNI del usuario: "):
    '''Solicita DNI de usuario en bucle, retorna cuando lo encuentra.'''
    return solicitar_dato(mensaje, sistema.buscar_usuario)

def solicitar_perro(mensaje="Ingrese ID del perro: "):
    '''Solicita DNI de usuario en bucle, retorna cuando lo encuentra.'''
    return solicitar_dato(mensaje, sistema.buscar_perro)

def solicitar_raza(mensaje="Ingrese nombre de la raza: "):
    '''Solicita DNI de usuario en bucle, retorna cuando lo encuentra.'''
    return solicitar_dato(mensaje, sistema.buscar_raza)

# Elige, muestra y retorna una instancia
def elegir_usuario(mensaje="Ingrese DNI del usuario: ", detalles=True):
    '''Muestra lista resumida de usuarios, solicita uno, muestra sus detalles y lo retorna.'''
    if not mostrar_objetos(sistema.usuarios, " Usuarios ", ["dni", "nombre"], "No hay usuarios"):
        return None
    usuario = solicitar_usuario(mensaje)
    if detalles:
        mostrar_detalles(usuario, "Usuario")
    return usuario

def elegir_perro(mensaje="Ingrese ID del perro: ", detalles=True):
    '''Muestra lista resumida de perros, solicita uno, muestra sus detalles y lo retorna.'''
    if not mostrar_objetos(sistema.perros, " Perros ", ["id", "nombre"], "No hay perros"):
        return None
    perro = solicitar_perro(mensaje)
    if detalles:
        mostrar_detalles(perro, "Perro")
    return perro

def elegir_raza(mensaje="Ingrese nombre de raza: ", detalles=True):
    '''Muestra lista resumida de razas, solicita una, muestra sus detalles y la retorna.'''
    if not mostrar_objetos(sistema.razas, " Razas ", ["nombre"], "No hay razas"):
        return None
    raza = solicitar_raza(mensaje)
    if detalles:
        mostrar_detalles(raza, "Raza")
    return raza

# Menu - Registrar
def opc_registrar_usuario():
    '''Solicita datos de usuario en bucle. Termina con nuevo usuario en el sistema.'''
    dni = solicitar_dato("DNI: ", UsuarioAdoptante.validar_dni)
    if sistema.buscar_usuario(dni, False):
        print(f"[!] El usuario con DNI {dni} ya está registrado")
        return
    nombre = solicitar_dato("Nombre: ", UsuarioAdoptante.validar_nombre)
    email = solicitar_dato(f"Email: ", UsuarioAdoptante.validar_email)
    usuario = UsuarioAdoptante(
        nombre=nombre,
        dni=dni,
        email=email
    )
    sistema.registrar_usuario(usuario)
    mostrar_detalles(usuario, "Usuario nuevo")

def opc_registrar_perro():
    '''Solicita datos de perro en bucle. Termina con nuevo perro en el sistema.'''
    nombre = solicitar_dato("Nombre (opcional): ", Perro.validar_nombre)
    edad = solicitar_dato(f"Edad de '{nombre}': ", Perro.validar_edad)
    peso = solicitar_dato(f"Peso: ", Perro.validar_peso)
    sexo = solicitar_dato(f"Sexo (M/F): ", Perro.validar_sexo)
    mostrar_objetos(sistema.razas, " Razas ", ["nombre"], "No hay razas")
    raza = solicitar_raza()
    vacunado = solicitar_bool(f"¿'{nombre}' está vacunado?")
    discapacitado = solicitar_bool(f"¿'{nombre}' tiene alguna discapacidad?")
    perro = Perro(
        nombre = nombre,
        edad = edad,
        peso = peso,
        sexo = sexo,
        raza = raza,
        vacunado = vacunado,
        discapacitado = discapacitado
    )
    sistema.registrar_perro(perro)
    mostrar_detalles(perro, "Perro nuevo")

def opc_registrar_raza():
    '''Solicita datos de raza en bucle. Termina con nueva raza en el sistema.'''
    nombre = solicitar_dato("Nombre de raza: ", Raza.validar_nombre)
    if sistema.buscar_raza(nombre, False):
        print(f"[!] La raza {nombre} ya está registrada")
        return
    tamanio = solicitar_dato(f"Tamaño [S/M/L/X] (puede dejarse en blanco): ", Raza.validar_tamanio)
    temperamento = solicitar_dato(f"Temperamento (puede dejarse en blanco): ", Raza.validar_temperamento)
    raza = Raza(
        nombre = nombre,
        temperamento = temperamento,
        tamanio = tamanio
    )
    sistema.registrar_raza(raza)
    mostrar_detalles(raza, "Raza nueva")

def menu_registrar():
    '''Menú de opciones para registrar usuario'''
    while True:
        mostrar_menu("Registrar", ["Registrar usuario", "Registrar perro", "Registrar raza"])
        opcion = input("Ingrese una opción: ")
        if opcion == "1":
            opc_registrar_usuario()
            input("[<] Presione 'Enter' para volver ")
        elif opcion == "2":
            opc_registrar_perro()
            input("[<] Presione 'Enter' para volver ")
        elif opcion == "3":
            opc_registrar_raza()
            input("[<] Presione 'Enter' para volver ")
        elif opcion == "0":
            break
        else:
            print("[!] Opción inválida, intente de nuevo.")

# Menu - Editar
def opc_editar_usuario():
    usuario:UsuarioAdoptante = elegir_usuario(detalles=False)
    if not usuario:
        return
    mostrar_detalles(usuario.mostrar_datos_personales(), "Usuario")
    # nombre
    validado = solicitar_bool(f"¿Cambiar nombre '{usuario.nombre}'?")
    if validado:
        solicitar_dato("Nombre: ", usuario.cambiar_nombre)
    # email
    validado = solicitar_bool(f"¿Cambiar email '{usuario.email}'?")
    if validado:
        solicitar_dato("Email: ", usuario.cambiar_email)
    mostrar_detalles(usuario.mostrar_datos_personales(), "Usuario editado")

def opc_editar_perro():
    perro:Perro = elegir_perro(detalles=False)
    if not perro:
        return
    mostrar_detalles(f"{perro.mostrar_datos_propios()}\nRaza: {perro.raza.nombre}", "Perro")
    # nombre
    validado = solicitar_bool(f"¿Cambiar nombre '{perro.nombre}'?")
    if validado:
        solicitar_dato("Nombre: ", perro.cambiar_nombre)
    # edad
    validado = solicitar_bool(f"¿Cambiar edad '{perro.edad}'?")
    if validado:
        solicitar_dato("Edad: ", perro.cambiar_edad)
    # peso
    validado = solicitar_bool(f"¿Cambiar peso '{perro.peso}'?")
    if validado:
        solicitar_dato("Peso: ", perro.cambiar_peso)
    # sexo
    validado = solicitar_bool(f"¿Cambiar sexo '{perro.sexo}'?")
    if validado:
        solicitar_dato("Sexo (M/F): ", perro.cambiar_sexo)
    # vacunado
    validado = solicitar_bool(f"¿Cambiar estado de vacunación '{perro.vacunado}'?")
    if validado:
        perro.cambiar_vacunado(solicitar_bool("Vacunado"))
    # discapacitado
    validado = solicitar_bool(f"¿Cambiar estado de discapacidad '{perro.discapacitado}'?")
    if validado:
        perro.cambiar_discapacitado(solicitar_bool("Discapacitado"))
    # raza
    validado = solicitar_bool(f"¿Cambiar raza '{perro.raza.nombre}'?")
    if validado:
        mostrar_objetos(sistema.razas, " Razas ", ["nombre"], "No hay razas")
        raza = solicitar_raza("Raza: ")
        perro.cambiar_raza(raza)
    mostrar_detalles(f"{perro.mostrar_datos_propios()}\nRaza: {perro.raza.nombre}", "Perro")

def opc_editar_raza():
    raza:Raza = elegir_raza()
    if not raza:
        return
    # tamaño
    validado = solicitar_bool("¿Cambiar tamaño?")
    if validado:
        solicitar_dato("Tamaño [S/M/L/X] (puede dejarse en blanco): ", raza.cambiar_tamanio)
    # temperamento
    validado = solicitar_bool("¿Cambiar temperamento?")
    if validado:
        solicitar_dato("Temperamento (puede dejarse en blanco): ", raza.cambiar_temperamento)
    mostrar_detalles(raza, "Raza editada")

def menu_editar():
    while True:
        mostrar_menu("Editar", ["Editar usuario", "Editar perro", "Editar raza"])
        opcion = input("Ingrese una opción: ")
        print()
        if opcion == "1":
            opc_editar_usuario()
            input("[<] Presione 'Enter' para volver ")
        elif opcion == "2":
            opc_editar_perro()
            input("[<] Presione 'Enter' para volver ")
        elif opcion == "3":
            opc_editar_raza()
            input("[<] Presione 'Enter' para volver ")
        elif opcion == "0":
            break
        else:
            print("[!] Opción inválida, intente de nuevo.")

# Menu - Borrar
def opc_borrar_usuario():
    usuario:UsuarioAdoptante = elegir_usuario("Ingrese DNI del usuario a borrar: ", False)
    if not usuario:
        return
    validado = solicitar_bool(f"¿Seguro que quiere borrar a {usuario.nombre}?")
    if validado:
        sistema.eliminar_usuario(usuario)
        print(f"[-] '{usuario.nombre}' fue borrado del sistema")
    else:
        print("[x] Se canceló la operación.")

def opc_borrar_perro():
    perro:Perro = elegir_perro("Ingrese ID del perro a borrar: ", False)
    if not perro:
        return
    validado = solicitar_bool(f"¿Seguro que quiere borrar a {perro.nombre}?")
    if validado:
        sistema.eliminar_perro(perro)
        print(f"[-] '{perro.nombre}' fue borrado del sistema :(")
    else:
        print("[x] Se canceló la operación.")

def menu_borrar():
    while True:
        mostrar_menu("Borrar", ["Borrar usuario", "Borrar perro"])
        opcion = input("Ingrese una opción: ")
        print()
        if opcion == "1":
            opc_borrar_usuario()
            input("[<] Presione 'Enter' para volver ")
        elif opcion == "2":
            opc_borrar_perro()
            input("[<] Presione 'Enter' para volver ")
        elif opcion == "0":
            break
        else:
            print("[!] Opción inválida, intente de nuevo.")

# Menu - Adopciones
def opc_reservar():
    perros_disponibles = mostrar_objetos(sistema.obtener_estado_perros("disponible"), " Perros Disponible ", ["id", "nombre"], "No hay perros disponibles")
    if not perros_disponibles:
        return
    perro = solicitar_perro("Ingrese ID del perro a reservar: ")
    print()
    mostrar_objetos(sistema.usuarios, " Usuarios ", ["dni", "nombre"], "No hay usuarios")
    usuario = solicitar_usuario("Ingrese DNI del usuario que hará la reserva: ")
    try:
        sistema.reservar(perro, usuario)
        print(f"[+] {usuario.nombre} ha reservado a {perro.nombre}")
    except ValueError as e:
        print("[!]", e)

def opc_adoptar():
    perros_reservados = mostrar_objetos(sistema.obtener_estado_perros("reservado"), " Perros Reservados ", ["id", "nombre"], "No hay perros reservados")
    if not perros_reservados:
        return
    perro = solicitar_perro(f"Ingrese ID del perro a adoptar: ")
    if perro.estado == "reservado":
        usuario = sistema.buscar_usuario(perro.adoptante, False)
        print(f"\n{usuario.nombre} ({usuario.dni}):")
        validado = solicitar_bool(f"¿quiere adoptar a {perro.nombre}?")
        try:
            if validado:
                sistema.adoptar(perro, usuario)
                print(f"[+] {usuario.nombre} ha adoptado a {perro.nombre}")
            else:
                sistema.devolver(perro, usuario)
                print(f"[-] {usuario.nombre} ha cancelado la reserva de {perro.nombre}")
        except ValueError as e:
            print("[!]", e)

def opc_devolver():
    perros_adoptados = mostrar_objetos(sistema.obtener_estado_perros("adoptado"), " Perros Adoptados ", ["id", "nombre"])
    perros_reservados = mostrar_objetos(sistema.obtener_estado_perros("reservado"), " Perros Reservados ", ["id", "nombre"])
    if not perros_adoptados and not perros_reservados:
        print(f"[x] No hay perros para adoptar o reservar")
        return
    perro = solicitar_perro(f"Ingrese ID del perro a devolver: ")
    if perro.estado != "disponible":
        usuario = sistema.buscar_usuario(perro.adoptante, False)
        print(f"\n{usuario.nombre} ({usuario.dni}):")
        validado = solicitar_bool(f"¿quiere cancelar la adopción/reserva de {perro.nombre}?")
        try:
            if validado:
                sistema.devolver(perro, usuario)
                print(f"[-] {usuario.nombre} ha cancelado la adopción/reserva de {perro.nombre}")
            else:
                print(f"[x] Se canceló la operación")
        except ValueError as e:
            print("[!]", e)

def menu_adopciones():
    if not sistema.perros:
        print("\n[x] No hay perros registrados en el sistema")
        return
    if not sistema.usuarios:
        print("\n[x] No hay usuarios registrados en el sistema")
        return
    while True:
        mostrar_menu("Adopciones", ["Reservar perro", "Adoptar perro", "Devolver perro"])
        opcion = input("Ingrese una opción: ")
        print()
        if opcion == "1":
            opc_reservar()
        elif opcion == "2":
            opc_adoptar()
        elif opcion == "3":
            opc_devolver()
        elif opcion == "0":
            break
        else:
            print("[!] Opción inválida, intente de nuevo.")

# Menú - Buscar/Mostrar/filtrar
def opc_ver_sugerencias():
    usuario:UsuarioAdoptante = elegir_usuario(detalles=False)
    pref = usuario.preferencias
    mostrar_detalles(pref, "Preferencias")
    validado = solicitar_bool(f"¿Quiere cambiar sus preferencias?")
    if validado:
        # edad
        validado = solicitar_bool(f"¿Quiere cambiar su edad preferida?")
        if validado:
            solicitar_dato("Ingrese la edad aproximada que prefiere (puede dejar en blanco): ", pref.cambiar_edad)
        # tamaño
        validado = solicitar_bool(f"¿Quiere cambiar su tamaño preferido?")
        if validado:
            solicitar_dato("Ingrese el tamaño que prefiere [S/M/L/X] (puede dejar en blanco): ", pref.cambiar_tamanio)
        # raza
        validado = solicitar_bool(f"¿Quiere cambiar su raza preferida?")
        if validado:
            raza = elegir_raza("Ingrese la raza que prefiere (puede dejar en blanco): ", detalles=False)
            pref.cambiar_raza(raza.nombre)
    print()
    mostrar_objetos(sistema.obtener_sugerencias_perros(usuario), "Sugerencias", ["id", "nombre"], "no hay coincidencia")

def menu_buscar():
    while True:
        mostrar_menu("Buscar", ["Buscar usuario", "Buscar perro", "Buscar raza", "Ver Sugerencias", "Perros disponibles", "Perros reservados", "Perros adoptados"])
        opcion = input("Ingrese una opción: ")
        print()
        if opcion == "1": # Buscar usuario
            elegir_usuario("Ingrese DNI del usuario que quiere ver: ")
            input("[<] Presione 'Enter' para volver ")
        elif opcion == "2": # Buscar perro
            elegir_perro("Ingrese ID del perro que quiere ver: ")
            input("[<] Presione 'Enter' para volver ")
        elif opcion == "3": # Buscar raza
            elegir_raza("Ingrese nombre de la raza que quiere ver: ")
            input("[<] Presione 'Enter' para volver ")
        elif opcion == "4": # Ver sugerencias
            opc_ver_sugerencias()
            input("[<] Presione 'Enter' para volver ")
        elif opcion == "5": # Perros disponibles
            mostrar_objetos(sistema.obtener_estado_perros("disponible"), "Disponibles", ["id", "nombre"], "No quedan")
            input("[<] Presione 'Enter' para volver ")
        elif opcion == "6": # Perros reservados
            mostrar_objetos(sistema.obtener_estado_perros("reservado"), "Reservados", ["id", "nombre"])
            input("[<] Presione 'Enter' para volver ")
        elif opcion == "7": # Perros adoptados
            mostrar_objetos(sistema.obtener_estado_perros("adoptado"), "Adoptados", ["id", "nombre"])
            input("[<] Presione 'Enter' para volver ")
        elif opcion == "0":
            break
        else:
            print("[!] Opción inválida, intente de nuevo.")

def menu_principal():
    while True:
        mostrar_menu("Sistema de Adopciones", ["Registrar", "Editar", "Borrar", "Adoptar", "Buscar"], "Salir")
        opcion = input("Ingrese una opción: ")
        if opcion == "1":
            menu_registrar()
        if opcion == "2":
            menu_editar()
        elif opcion == "3":
            menu_borrar()
        elif opcion == "4":
            menu_adopciones()
        elif opcion == "5":
            menu_buscar()
            pass
        if opcion == "0":
            break
    print("\n   ,,__              ")
    print(  "  ; | ·\\_.   Saludos!")
    print(  "_/ \\| ,,,|           ")
    print(  "     /               ")

sistema = SistemaAdopcion()

mestizo = sistema.registrar_raza(Raza("Mestizo"))
chihuahua = sistema.registrar_raza(Raza(nombre="Chihuahua", temperamento="Nervioso", tamanio="S"))
dalmata = sistema.registrar_raza(Raza(nombre="Dalmata", temperamento="Enérgico", tamanio="L"))
gran_danes = sistema.registrar_raza(Raza(nombre="Gran Danés", temperamento="Gentil", tamanio="X"))
sistema.registrar_raza(Raza(nombre="Poodle", temperamento="Activo", tamanio="M"))
sistema.registrar_raza(Raza(nombre="San Bernardo", temperamento="Tranquilo", tamanio="X"))
sistema.registrar_raza(Raza(nombre="Pug", temperamento="Divertido", tamanio="S"))
sistema.registrar_usuario(UsuarioAdoptante(nombre="Tito", dni="11111111", email="tatetito@bgmail.com"))
sistema.registrar_usuario(UsuarioAdoptante(nombre="Pepe", dni="22222222", email="pepocho@pp.8"))
sistema.registrar_usuario(UsuarioAdoptante(nombre="Ana", dni="33333333", email="ana@na.com"))
sistema.registrar_usuario(UsuarioAdoptante(nombre="Armando Esteban Quito", dni="44444444", email="a@a.a"))
sistema.registrar_usuario(UsuarioAdoptante(nombre="Alan Brito", dni="M5555555", email="dea@luminio.com"))
sistema.registrar_usuario(UsuarioAdoptante(nombre="Aquiles Bailo", dni="F6666666", email="b@b.com"))
sistema.registrar_perro(Perro(nombre="Pichichus", edad=1, peso=8.5, sexo="M", raza=chihuahua, vacunado=True, discapacitado=False))
sistema.registrar_perro(Perro(nombre="Catrina", edad=2, peso=7, sexo="F", raza=chihuahua, vacunado=True, discapacitado=False))
sistema.registrar_perro(Perro(nombre="La Tuerta", edad=13, peso=22.4, sexo="F", raza=mestizo, vacunado=True, discapacitado=True))
sistema.registrar_perro(Perro(nombre="Tato", edad=2, peso=42, sexo="M", raza=dalmata, vacunado=True, discapacitado=False))
sistema.registrar_perro(Perro(nombre="Milanga", edad=6, peso=12.5, sexo="M", raza=chihuahua, vacunado=True, discapacitado=True))
sistema.registrar_perro(Perro(nombre="Panceta", edad=8, peso=99.9, sexo="F", raza=gran_danes, vacunado=True, discapacitado=False))

menu_principal()
