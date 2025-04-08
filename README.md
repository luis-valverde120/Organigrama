# Organigrama

Este proyecto es una aplicación para la gestión de organigramas utilizando una arquitectura hexagonal. Está desarrollado con las siguientes tecnologías:

## Tecnologías utilizadas

- **Backend**: Python con Flask.
- **Base de datos**: PostgreSQL utilizando SQLAlchemy como ORM.
- **Frontend**:  Nextjs para el frontend

## Arquitectura

La arquitectura hexagonal permite una separación clara entre las diferentes capas de la aplicación, facilitando la mantenibilidad y escalabilidad del proyecto. Esto incluye:

- **Capa de dominio**: Contiene la lógica de negocio principal.
- **Adaptadores**: Interfaces para interactuar con el mundo exterior (por ejemplo, base de datos, API, frontend).
- **Aplicación**: Coordina las operaciones entre el dominio y los adaptadores.

## Instalación

1. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd organigrama
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configura la base de datos PostgreSQL y actualiza las credenciales en el archivo de configuración.

4. Ejecuta la aplicación Flask:
   ```bash
   flask run
   ```

5. Inicia el frontend con Streamlit:
   ```bash
   streamlit run app.py
   ```

## Configuración

Para configurar la URL de la API, utiliza un archivo `.env` en la raíz del proyecto. Este archivo debe contener la siguiente variable:

```
API_URL=<URL_DE_TU_API>
```

Asegúrate de reemplazar `<URL_DE_TU_API>` con la URL real de tu API.

## Requisitos

A continuación se detallan las dependencias necesarias para este proyecto, incluidas en el archivo `requirements.txt`:

- Flask (v2.2.5)
- SQLAlchemy (v1.4.46)
- psycopg2 (v2.9.6)
- Streamlit (v1.25.0)

## Uso

La aplicación permite crear, visualizar y gestionar organigramas de manera interactiva. El frontend desarrollado con Streamlit proporciona una interfaz amigable para los usuarios.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para discutir cualquier cambio.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
