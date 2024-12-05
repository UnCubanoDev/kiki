# Proyecto Kiki

Este proyecto es una aplicación web desarrollada con Django y Django REST Framework, diseñada para gestionar usuarios, direcciones, pedidos y más. Incluye funcionalidades como autenticación, gestión de contraseñas, y un panel de administración personalizado.

## Requisitos

- Python 3.8+
- Django 4.1.1
- PostgreSQL
- Redis (para Channels)
- Node.js (para el servicio de WhatsApp)

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/tu_usuario/kiki.git
   cd kiki
   ```

2. **Crear y activar un entorno virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. **Instalar las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno:**

   Crea un archivo `.env` en la raíz del proyecto y define las siguientes variables:

   ```
   SECRET_KEY=tu_secreto
   DEBUG=1
   SQL_DATABASE=kiki
   SQL_USER=postgres
   SQL_PASSWORD=postgres
   SQL_HOST=localhost
   SQL_PORT=5432
   ```

5. **Realizar las migraciones de la base de datos:**

   ```bash
   python manage.py migrate
   ```

6. **Cargar datos de prueba (opcional):**

   ```bash
   python populate_db.py
   ```

7. **Ejecutar el servidor de desarrollo:**

   ```bash
   python manage.py runserver
   ```

## Funcionalidades

- **Autenticación de Usuarios:**

  - Registro, inicio de sesión y recuperación de contraseñas.
  - Activación de cuenta vía enlace de activación.

- **Gestión de Pedidos:**

  - Creación y seguimiento de pedidos.
  - Notificaciones de estado de pedidos vía WhatsApp.

- **Panel de Administración:**

  - Personalizado con Jazzmin.
  - Dashboard con estadísticas de ventas y pedidos.

- **Internacionalización:**
  - Soporte para inglés y español.

## Estructura del Proyecto

- `src/`: Contiene la configuración principal de Django.
- `directorio/`: Aplicación para la gestión de usuarios y direcciones.
- `api/`: Aplicación para la gestión de pedidos, productos y configuraciones.
- `templates/`: Plantillas HTML para el frontend.
- `locale/`: Archivos de traducción para internacionalización.


## Despliegue

Este proyecto está configurado para ser desplegado en un VPS usando Docker y GitHub Actions. Asegúrate de configurar correctamente los secretos en GitHub para el despliegue automático.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue el flujo de trabajo de GitHub para enviar tus pull requests.
