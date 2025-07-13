# Servicio de Solicitudes de Donación de Sangre

Servicio backend para la gestión de solicitudes de donación de sangre para mascotas, desarrollado con FastAPI.

## Características

- FastAPI como framework web
- MongoDB Atlas como base de datos
- Cloudinary para almacenamiento de imágenes
- Estructura modular y escalable
- Configuración de CORS
- Variables de entorno con python-dotenv
- Documentación automática con Swagger y ReDoc
- Validación de datos con Pydantic
- Endpoints para veterinarias y usuarios
- Despliegue automático con GitHub Actions y Fly.io

## Requisitos

- Python 3.8+
- MongoDB Atlas
- Cloudinary (para almacenamiento de imágenes)
- pip

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/CobrasOrg/solicitudes-service-dev.git
cd solicitudes-service-dev
```

2. Crear y activar entorno virtual:

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:

```bash
cp env.example .env
# Editar .env con tus configuraciones de MongoDB Atlas y Cloudinary
```

5. Ejecutar el servidor:

```bash
python main.py
```

La aplicación estará disponible en:
- **API**: Configurada por variable de entorno `BASE_URL`
- **Documentación Swagger**: `${BASE_URL}/docs`
- **Health check**: `${BASE_URL}/health`

## Configuración

### MongoDB Atlas

1. Ve a [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Crea una cuenta gratuita
3. Crea un nuevo cluster (plan gratuito M0)
4. Crea un usuario de base de datos con permisos de "Read and write"
5. Configura acceso de red (usa `0.0.0.0/0` para desarrollo)
6. Obtén la cadena de conexión

### Cloudinary (para imágenes)

1. Ve a [Cloudinary](https://cloudinary.com/)
2. Crea una cuenta gratuita
3. Obtén tus credenciales desde el Dashboard:
   - Cloud Name
   - API Key
   - API Secret

### Variables de Entorno

```bash
# MongoDB Atlas
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/solicitudes?retryWrites=true&w=majority
MONGODB_DATABASE=solicitudes

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Server Configuration
HOST=127.0.0.1
PORT=8000
BASE_URL=http://127.0.0.1:8000

# Application Configuration
APP_ENV=development
DEBUG=true

# CORS Configuration
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## Ejecución

Una vez configurado todo, ejecuta:

```bash
python main.py
```

### Acceso a la API

- **API Base**: Configurada por `BASE_URL` (por defecto: http://127.0.0.1:8000)
- **Documentación Swagger**: `${BASE_URL}/docs`
- **Documentación ReDoc**: `${BASE_URL}/redoc`
- **Health Check**: `${BASE_URL}/health`

### Usar la API desde Swagger

1. Abre `${BASE_URL}/docs` en tu navegador
2. Explora los endpoints disponibles
3. Haz clic en "Try it out" para probar los endpoints
4. Completa los parámetros requeridos
5. Ejecuta la petición

## Endpoints Disponibles

### Veterinarias

#### Obtener Todas las Solicitudes
- **Endpoint**: `GET /api/v1/vet/solicitudes/`
- **Descripción**: Retorna todas las solicitudes independientemente de su estado
- **Respuestas**:
  - `200`: Lista de todas las solicitudes
  - `500`: Error interno del servidor

#### Filtrar Solicitudes por Estado
- **Endpoint**: `GET /api/v1/vet/solicitudes/filtrar`
- **Descripción**: Retorna las solicitudes filtradas por estado y otros criterios
- **Parámetros de Consulta**:
  - `estado`: Estado de las solicitudes (Activa, Completada, Cancelada, Revision)
  - `especie`: Filtrar por especie (ej: Perro, Gato)
  - `tipo_sangre`: Filtrar por tipo de sangre (ej: DEA 1.1+, A)
  - `urgencia`: Filtrar por nivel de urgencia (Alta, Media, Baja)
  - `localidad`: Filtrar por localidad (ej: Suba, Chapinero)
- **Respuestas**:
  - `200`: Lista de solicitudes filtradas
  - `400`: Estado inválido
  - `422`: Error de validación
  - `500`: Error interno del servidor

#### Obtener Solicitud Específica
- **Endpoint**: `GET /api/v1/vet/solicitudes/{solicitud_id}`
- **Descripción**: Retorna una solicitud específica por su ID
- **Parámetros de Ruta**:
  - `solicitud_id`: ID de la solicitud
- **Respuestas**:
  - `200`: Solicitud encontrada
  - `404`: Solicitud no encontrada
  - `500`: Error interno del servidor

#### Crear Nueva Solicitud
- **Endpoint**: `POST /api/v1/vet/solicitudes/`
- **Descripción**: Crea una nueva solicitud de donación de sangre
- **Cuerpo de la Solicitud** (multipart/form-data):
  ```
  nombre_veterinaria: string
  nombre_mascota: string
  especie: string
  localidad: string
  descripcion_solicitud: string
  direccion: string
  ubicacion: string
  contacto: string
  peso_minimo: number
  tipo_sangre: string
  urgencia: string
  foto_mascota: file (opcional)
  ```
- **Respuestas**:
  - `201`: Solicitud creada exitosamente
  - `422`: Error de validación
  - `500`: Error interno del servidor

#### Actualizar Datos de Solicitud
- **Endpoint**: `PATCH /api/v1/vet/solicitudes/{solicitud_id}`
- **Descripción**: Actualiza los datos de una solicitud existente
- **Parámetros de Ruta**:
  - `solicitud_id`: ID de la solicitud
- **Cuerpo de la Solicitud** (multipart/form-data o JSON):
  ```
  especie: string (opcional)
  tipo_sangre: string (opcional)
  urgencia: string (opcional)
  peso_minimo: number (opcional)
  descripcion_solicitud: string (opcional)
  direccion: string (opcional)
  estado: string (opcional)
  foto_mascota: file (opcional)
  ```
- **Respuestas**:
  - `200`: Solicitud actualizada exitosamente
  - `404`: Solicitud no encontrada
  - `422`: Error de validación
  - `500`: Error interno del servidor

#### Actualizar Estado de Solicitud
- **Endpoint**: `PATCH /api/v1/vet/solicitudes/{solicitud_id}/estado`
- **Descripción**: Actualiza el estado de una solicitud existente
- **Parámetros de Ruta**:
  - `solicitud_id`: ID de la solicitud
- **Cuerpo de la Solicitud**:
  ```json
  {
    "estado": "string"
  }
  ```
- **Respuestas**:
  - `200`: Estado actualizado exitosamente
  - `400`: Estado inválido
  - `404`: Solicitud no encontrada
  - `422`: Error de validación
  - `500`: Error interno del servidor

#### Eliminar Solicitud
- **Endpoint**: `DELETE /api/v1/vet/solicitudes/{solicitud_id}`
- **Descripción**: Elimina una solicitud existente
- **Parámetros de Ruta**:
  - `solicitud_id`: ID de la solicitud
- **Respuestas**:
  - `200/204`: Solicitud eliminada exitosamente
  - `404`: Solicitud no encontrada
  - `500`: Error interno del servidor

### Usuarios

#### Obtener Solicitudes Activas
- **Endpoint**: `GET /api/v1/user/solicitudes/activas`
- **Descripción**: Retorna todas las solicitudes que tienen estado 'Activa'
- **Respuestas**:
  - `200`: Lista de solicitudes activas
  - `500`: Error interno del servidor

#### Filtrar Solicitudes Activas
- **Endpoint**: `GET /api/v1/user/solicitudes/activas/filtrar`
- **Descripción**: Retorna las solicitudes activas filtradas por criterios
- **Parámetros de Consulta**:
  - `especie`: Filtrar por especie (ej: Perro, Gato)
  - `tipo_sangre`: Filtrar por tipo de sangre (ej: DEA 1.1+, A)
  - `urgencia`: Filtrar por nivel de urgencia (Alta, Media, Baja)
  - `localidad`: Filtrar por localidad (ej: Suba, Chapinero)
- **Respuestas**:
  - `200`: Lista de solicitudes activas filtradas
  - `422`: Error de validación
  - `500`: Error interno del servidor

## Estructura del Proyecto

```
solicitudes-service-dev/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── base.py
│   │       │   ├── solicitudes/
│   │       │   │   ├── user/
│   │       │   │   └── vet/
│   │       └── api.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   ├── database.py
│   │   └── mongodb.py
│   ├── models/
│   │   ├── base.py
│   │   ├── solicitud.py
│   │   └── solicitud_mongo.py
│   ├── schemas/
│   │   ├── base.py
│   │   └── solicitud.py
│   ├── constants/
│   │   └── solicitudes.py
│   ├── data/
│   │   └── mock_data.json
│   └── services/
│       └── cloudinary_service.py
├── scripts/
│   ├── deployment/
│   │   └── test_deployment.py
│   ├── database/
│   │   ├── populate_database.py
│   │   └── clear_database.py
│   └── testing/
│       └── test_quick.py
├── tests/
│   ├── conftest.py
│   ├── test_solicitudes.py
│   └── test_deployment.py
├── .env.example
├── .gitignore
├── main.py
├── README.md
├── CHANGELOG.md
├── requirements.txt
├── Dockerfile
├── fly.toml
└── DEPLOYMENT.md
```

### Descripción de Carpetas y Archivos

- `app/`: Directorio principal de la aplicación
  - `api/`: Endpoints y rutas de la API
  - `core/`: Configuraciones centrales
  - `db/`: Configuración y conexión a la base de datos
  - `models/`: Modelos de datos y lógica de negocio
  - `schemas/`: Esquemas Pydantic para validación de datos
  - `constants/`: Constantes y enumeraciones del sistema
  - `data/`: Datos mock y archivos de datos
  - `services/`: Servicios externos (Cloudinary, etc.)

- `scripts/`: Scripts utilitarios
  - `deployment/`: Scripts de despliegue
  - `database/`: Scripts de gestión de base de datos
  - `testing/`: Scripts de testing

- `tests/`: Tests automatizados
- `Dockerfile`: Configuración de contenedor Docker
- `fly.toml`: Configuración de Fly.io
- `DEPLOYMENT.md`: Documentación de despliegue

## Despliegue

### Staging (Este repositorio)
- **URL**: `https://solicitudes-staging.fly.dev`
- **Despliegue automático**: Al hacer push a `develop`

### Producción (Repo separado)
- **URL**: `https://solicitudes.fly.dev`
- **Despliegue automático**: Al hacer push a `main`

## Testing

### Tests básicos:
```bash
pytest tests/ -v
```

### Poblar base de datos:
```bash
python scripts/database/populate_database.py
```

**Para información detallada de testing y reportes PDF, consulta [TESTING.md](TESTING.md)**

## Características Técnicas

- ✅ FastAPI como framework web
- ✅ MongoDB Atlas como base de datos
- ✅ Cloudinary para almacenamiento de imágenes
- ✅ Estructura modular y escalable
- ✅ Configuración de CORS
- ✅ Variables de entorno con python-dotenv
- ✅ Documentación automática con Swagger y ReDoc
- ✅ Validación de datos con Pydantic
- ✅ Endpoints para veterinarias y usuarios
- ✅ Despliegue automático con GitHub Actions y Fly.io
- ✅ Tests automatizados
- ✅ CI/CD pipeline completo 