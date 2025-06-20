# Sistema de Adopción de Perros

Este proyecto es un sistema que gestiona adopciones de perros, permitiendo registrar, editar y eliminar usuarios, razas de perros y perros, como también procesar reservas, adopciones y devolución de perros.

## Estructura del Proyecto

El sistema tiene tres módulos principales (más el menú en main):

1. **sistema_adopcion.py**: Clase principal que maneja todo el sistema
2. **usuario.py**: Clases para usuarios adoptantes y sus preferencias
3. **perro.py**: Clases para perros y sus razas

## Funcionalidades Principales

### `SistemaAdopcion`
- Patrón Singleton para que el sistema tenga una única instancia
- Registrar, buscar y eliminar del sistema a:
  - Usuarios
  - Perros
  - Razas
- Operaciones de adopción:
  - Reservar perros
  - Adoptar perros
  - Devolver perros
- Búsqueda y filtrado de perros:
  - Por preferencias de usuario
  - Por historial de adopciones
  - Por estado (disponible/reservado/adoptado)

### `UsuarioAdoptante`
- **Hereda** atributos y métodos de `Usuario`
- Genera y mantiene en su interior su propia instancia de `Preferencias` (usando **composición**)
- Registra datos personales (nombre, DNI, email)
- Mantiene un historial de adopciones
- Puede reservar, adoptar y devolver perros (maneja datos internos, no interfiere con otras clases)

### `Perro` y `Raza`
- Registra características físicas
- Recibe y retiene instancia de Raza (usando **agregación**)
- Valida los datos ingresados
- Puede cambiar sus atributos
- Asigna dueño y gestiona sus estados (disponible/reservado/adoptado)

## Uso Básico

1. Crear una instancia del sistema:
   ```python
   sistema = SistemaAdopcion()
   ```

2. Registrar usuarios:
   ```python
   usuario = UsuarioAdoptante(nombre="Alan Brito", dni="12345678", email="dealu@minio.com")
   sistema.registrar_usuario(usuario)
   ```

3. Registrar razas:
   ```python
   raza = Raza(nombre="Labrador", tamanio="L", temperamento="Amigable")
   sistema.registrar_raza(raza)
   ```

4. Registrar perros:
   ```python
   perro = Perro(nombre="Pichichus", edad=1, peso=1.7, sexo="M", raza=raza, vacunado=True, discapacitado=False)
   sistema.registrar_perro(perro)
   ```

5. Realizar operaciones:
   ```python
   sistema.reservar(perro, usuario)  # Reservar
   sistema.adoptar(perro, usuario)   # Adoptar
   sistema.devolver(perro, usuario)  # Devolver
   ```

## Validaciones

El sistema valida (por demás):
- Tipos de datos
- Formatos correctos (DNI de 8 dígitos, email con '@')
- Estados coherentes (no adoptar sin reserva previa)
- Existencia de registros

## Ejemplos

Los archivos incluyen al final una serie de ejemplos que pueden servir para probar y entender el funcionamiento de las clases.
