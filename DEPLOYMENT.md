# Configuración de Despliegue - Fly.io

Esta guía explica cómo configurar el despliegue en Fly.io para staging y producción.

## 🏗️ **Arquitectura**

```
📁 solicitudes-service-dev/     # Este repositorio (Desarrollo)
├── 🌿 develop                  # Desplegado en Fly.io (staging)
└── 🌿 main                     # Sincroniza con producción

📁 solicitudes-service-prod/    # Repositorio de producción
├── 🌿 main                     # Desplegado en Fly.io (producción)
└── 🌿 develop                  # Sincronización con dev
```

## 🚀 **Configuración de Staging (Este repositorio)**

### **1. Instalar Fly CLI**
```bash
# Windows
winget install Fly.Flyctl

# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh
```

### **2. Autenticarse con Fly.io**
```bash
flyctl auth login
```

### **3. Crear aplicación de staging**
```bash
flyctl apps create solicitudes-staging
```

### **4. Configurar variables de entorno**
```bash
# MongoDB Atlas
flyctl secrets set MONGODB_URL="mongodb+srv://username:password@cluster.mongodb.net/solicitudes?retryWrites=true&w=majority"
flyctl secrets set MONGODB_DATABASE="solicitudes"

# Cloudinary
flyctl secrets set CLOUDINARY_CLOUD_NAME="your_cloud_name"
flyctl secrets set CLOUDINARY_API_KEY="your_api_key"
flyctl secrets set CLOUDINARY_API_SECRET="your_api_secret"



# Server Configuration
flyctl secrets set BASE_URL="https://solicitudes-staging.fly.dev"
flyctl secrets set HOST="0.0.0.0"
flyctl secrets set PORT="8000"
```

### **5. Desplegar manualmente (primer despliegue)**
```bash
flyctl deploy
```

## 🔧 **Configuración de GitHub Secrets**

### **Secrets requeridos para staging:**
```bash
FLY_API_TOKEN=your_fly_api_token
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/solicitudes?retryWrites=true&w=majority
MONGODB_DATABASE=solicitudes
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
STAGING_BASE_URL=https://solicitudes-staging.fly.dev
```

## 🔄 **Flujo de trabajo**

### **Desarrollo:**
1. Trabajar en rama `develop`
2. Hacer cambios y commits
3. Push a `develop`
4. GitHub Actions despliega automáticamente a staging
5. Probar en `https://solicitudes-staging.fly.dev`

### **Producción:**
1. Cuando esté listo, merge `develop` a `main`
2. Push a `main`
3. GitHub Actions ejecuta automáticamente:
   - Tests críticos de despliegue
   - Sincronización con repo de producción (`CobrasOrg/solicitudes-service`)
4. El repo de producción maneja su propio despliegue a producción

## 📊 **URLs de despliegue**

### **Staging (Este repo):**
- **URL**: `https://solicitudes-staging.fly.dev`
- **Health Check**: `https://solicitudes-staging.fly.dev/health`
- **Documentación**: `https://solicitudes-staging.fly.dev/docs`
- **Tests**: Ejecuta tests de despliegue antes del deploy
- **Reportes**: Solo en consola (no PDF en CI/CD)

### **Producción (Repo separado):**
- **URL**: `https://solicitudes.fly.dev`
- **Health Check**: `https://solicitudes.fly.dev/health`
- **Documentación**: `https://solicitudes.fly.dev/docs`
- **Tests**: Ejecuta tests completos antes del deploy

## 🛠️ **Comandos útiles**

### **Ver logs de staging:**
```bash
flyctl logs -a solicitudes-staging
```

### **Ver estado de la aplicación:**
```bash
flyctl status -a solicitudes-staging
```

### **Escalar aplicación:**
```bash
flyctl scale count 1 -a solicitudes-staging
```

### **Reiniciar aplicación:**
```bash
flyctl restart -a solicitudes-staging
```

## 🔍 **Monitoreo**

### **Health Check:**
- **Endpoint**: `/health`
- **Intervalo**: 30 segundos
- **Timeout**: 5 segundos

### **Métricas disponibles:**
- CPU y memoria
- Requests por segundo
- Latencia de respuesta
- Errores HTTP

## 🚨 **Solución de problemas**

### **Error de conexión a MongoDB:**
```bash
# Verificar variables de entorno
flyctl secrets list -a solicitudes-staging

# Actualizar variable
flyctl secrets set MONGODB_URL="nueva_url" -a solicitudes-staging
```

### **Error de despliegue:**
```bash
# Ver logs detallados
flyctl logs -a solicitudes-staging

# Reintentar despliegue
flyctl deploy -a solicitudes-staging
```

### **Error de memoria:**
```bash
# Escalar a más memoria
flyctl scale memory 512 -a solicitudes-staging
```

## 📝 **Notas importantes**

1. **Staging usa la misma base de datos que desarrollo** para ahorrar recursos
2. **Producción tendrá su propia base de datos** separada
3. **Las variables de entorno son diferentes** para cada entorno
4. **Los logs se mantienen por 30 días** en Fly.io
5. **El despliegue es automático** cuando se hace push a `develop` 