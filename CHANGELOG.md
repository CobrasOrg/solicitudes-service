# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-07-12

### Added
- **Sistema de reportes PDF profesionales** para pruebas de despliegue
- **Base de datos separada para testing** (`solicitudes_test`) para no afectar datos de producción
- **Detección automática de entorno CI/CD** para optimizar generación de reportes
- **Scripts de testing mejorados** con soporte para reportes PDF
- **Configuración de variables de entorno para testing** separadas de producción
- **Documentación completa de reportes PDF** en TESTING.md
- **Estructura de assets** para logos de universidad en reportes

### Changed
- **Reorganización de scripts de testing** en estructura más lógica
- **Optimización de configuración de testing** con variables separadas
- **Mejora en documentación** con ejemplos de uso de reportes PDF
- **Actualización de .gitignore** para excluir reportes PDF del repositorio
- **Refactorización de scripts de deployment** para incluir generación de PDF

### Removed
- **Scripts de testing obsoletos** que no funcionaban correctamente
- **Dependencias problemáticas** (matplotlib) que causaban errores de instalación
- **Archivos de reportes duplicados** en ubicaciones incorrectas

### Performance
- **Tests más rápidos** con base de datos separada
- **Generación de PDF optimizada** solo en entorno local
- **Mejor gestión de recursos** con detección de entorno CI/CD

## [0.1.2] - 2025-07-11

### Changed
- Optimizado `mock_data.json` de 20 a 10 registros para reducir uso de Cloudinary
- Deshabilitada migración automática de datos mock al iniciar el servidor
- Tests optimizados para usar máximo 10 registros en todas las operaciones
- Optimizados scripts de testing para mayor velocidad y eficiencia
- Configuración de pytest mejorada con opciones optimizadas
- Consolidada documentación de testing en `TESTING.md`
- Reorganizada documentación: README.md simplificado, TESTING.md consolidado
- Separada documentación de desarrollo y producción

### Added
- Scripts para gestión manual de base de datos:
  - `populate_database.py` - Para poblar la base de datos con datos de prueba
  - `clear_database.py` - Para limpiar todas las solicitudes

### Removed
- Migración automática de datos mock desde `main.py`
- Dependencia de migración automática en el startup del servidor
- Documentación duplicada de testing

### Performance
- Reducción del 50% en uso de Cloudinary para evitar costos excesivos
- Tests rápidos ejecutándose en menos de 30 segundos
- Reducción del 40% en tiempo de ejecución de tests completos

## [0.1.0] - 2025-06-10

### Added
- Implementación inicial del servicio de solicitudes
- Estructura base del proyecto FastAPI
- Endpoints para gestión de solicitudes:
  - GET `/api/v1/user/solicitudes/activas` - Obtener solicitudes activas
  - GET `/api/v1/user/solicitudes/activas/filtrar` - Filtrar solicitudes activas
  - GET `/api/v1/vet/solicitudes` - Obtener todas las solicitudes (veterinarias)
  - GET `/api/v1/vet/solicitudes/filtrar` - Filtrar solicitudes por estado
  - GET `/api/v1/vet/solicitudes/{solicitud_id}` - Obtener solicitud específica
  - POST `/api/v1/vet/solicitudes` - Crear nueva solicitud
  - PATCH `/api/v1/vet/solicitudes/{solicitud_id}` - Actualizar estado de solicitud
- Modelos y schemas para validación de datos:
  - Validación de estados permitidos
  - Validación de localidades permitidas
  - Validación de tipos de sangre
  - Validación de niveles de urgencia
- Tests iniciales para endpoints principales:
  - Tests de creación de solicitudes
  - Tests de actualización de estado
  - Tests de filtrado por estado
  - Tests de validación de datos
- Documentación de API con Swagger y ReDoc
- Archivo de datos mock con 10 registros de ejemplo (optimizado para Cloudinary)
- Configuración de CORS para desarrollo
- Variables de entorno con python-dotenv
- Husky para validación de mensajes de commit
- Pre-commit hooks para linting y formateo

### Changed
- Refactorización de la estructura de routers para eliminar duplicación
- Mejora en la generación de IDs para mantener consistencia con el formato hexadecimal
- Actualización de la validación de estados y localidades
- Mejora en la documentación de endpoints
- Optimización de la estructura del proyecto

### Fixed
- Corrección en la validación de estados vacíos
- Corrección en la duplicación de documentación en ReDoc
- Corrección en el manejo de tags redundantes en routers
- Corrección en el formato de fechas de creación
- Corrección en la validación de localidades

### Security
- Implementación de validación de datos en todos los endpoints
- Configuración de CORS para desarrollo
- Preparación para futura implementación de autenticación

### Pending
- Completar suite de tests:
  - Tests de integración
  - Tests de rendimiento
  - Tests de carga
- Integración con base de datos MongoDB:
  - Configuración de conexión
  - Migración de datos mock
  - Índices y optimizaciones
- Implementación de autenticación y autorización:
  - JWT tokens
  - Roles y permisos
  - Middleware de autenticación
- Implementación de logging y monitoreo:
  - Logs estructurados
  - Métricas de rendimiento
  - Alertas
- Implementación de rate limiting:
  - Límites por IP
  - Límites por usuario
  - Límites por endpoint
- Implementación de caché:
  - Caché de respuestas
  - Caché de consultas frecuentes
  - Invalidación de caché 