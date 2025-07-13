# GitFlow - Modelo de Branching

Este documento describe el modelo de branching GitFlow implementado en todos los repositorios del proyecto.

## 🌿 Estructura de Ramas

### **Ramas Principales**
- `main/` - Código de producción (estable)
- `develop/` - Rama de desarrollo (integración)

### **Ramas de Trabajo**
- `feature/` - Nuevas funcionalidades
- `release/` - Preparación de releases
- `hotfix/` - Correcciones urgentes en producción

## 🔄 Flujo de Trabajo

### **1. Desarrollo de Features**

```bash
# Crear feature desde develop
git checkout develop
git pull origin develop
git checkout -b feature/nombre-feature

# Trabajar en la feature
# ... código ...

# Hacer commits
git add .
git commit -m "feat: descripción de la funcionalidad"

# Push a la rama feature
git push origin feature/nombre-feature
```

### **2. Testing en Features**

```bash
# Ejecutar tests antes de merge
python test_quick.py
pytest

# Si los tests fallan, corregir y hacer commit
git add .
git commit -m "fix: corregir tests"
```

### **3. Merge Feature a Develop**

```bash
# Crear Pull Request: feature → develop
# URL: https://github.com/CobrasOrg/solicitudes-service-dev/pull/new/feature/nombre-feature

# Code review obligatorio
# Tests deben pasar
# Merge solo después de aprobación
```

### **4. Release a Producción**

```bash
# Crear release desde develop
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0

# Testing final
python test_quick.py
pytest

# Ajustes finales si es necesario
git add .
git commit -m "chore: ajustes finales para release"

# Merge a main y develop
git checkout main
git merge release/v1.2.0
git tag v1.2.0
git push origin main --tags

git checkout develop
git merge release/v1.2.0
git push origin develop

# Eliminar rama release
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

### **5. Sincronización con Producción**

```bash
# Después de validar en staging, merge a main
git checkout main
git merge develop
git push origin main

# El workflow ci-cd.yml maneja automáticamente:
# - Tests de despliegue
# - Sincronización con repo de producción
# - Exclusión de archivos de testing
```

### **6. Hotfix (Correcciones Urgentes)**

```bash
# Crear hotfix desde main
git checkout main
git pull origin main
git checkout -b hotfix/correccion-urgente

# Corregir el problema
# ... código ...

# Testing
python test_quick.py
pytest

# Merge a main y develop
git checkout main
git merge hotfix/correccion-urgente
git tag v1.2.1
git push origin main --tags

git checkout develop
git merge hotfix/correccion-urgente
git push origin develop

# Eliminar rama hotfix
git branch -d hotfix/correccion-urgente
git push origin --delete hotfix/correccion-urgente
```

## 🛡️ Reglas de Protección de Ramas

### **Rama `main`**
- ✅ Require pull request reviews
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- ✅ Restrict pushes that create files that use the gitfile: protocol
- ❌ No direct pushes (solo merge desde release/hotfix)

### **Rama `develop`**
- ✅ Require pull request reviews
- ✅ Require status checks to pass before merging
- ❌ Allow force pushes (solo para releases)

## 📋 Convenciones de Nomenclatura

### **Ramas Feature**
```
feature/nombre-descriptivo
feature/user-authentication
feature/payment-integration
```

### **Ramas Release**
```
release/v1.2.0
release/v2.0.0
```

### **Ramas Hotfix**
```
hotfix/critical-bug-fix
hotfix/security-patch
```

### **Commits**
```
feat: nueva funcionalidad
fix: corrección de bug
docs: actualización de documentación
style: cambios de formato
refactor: refactorización de código
test: agregar o modificar tests
chore: tareas de mantenimiento
```

## 🧪 Testing Obligatorio

### **Antes de Merge a Develop**
- ✅ `python run_tests.py quick` debe pasar (tests críticos)
- ✅ Tests de despliegue deben pasar
- ✅ Todos los tests críticos deben estar verdes

### **Antes de Release (Merge a Main)**
- ✅ Tests ya fueron ejecutados en develop
- ✅ Verificación manual de funcionalidades en staging
- ✅ Documentación actualizada

### **Flujo de Testing**
1. **Desarrollo**: Tests locales con `python run_tests.py quick`
2. **Develop**: Tests automáticos en CI/CD
3. **Main**: Sin tests (ya validados en develop)
4. **Producción**: Despliegue automático desde main

### **Tests Críticos para CI/CD**
Los siguientes tests se ejecutan automáticamente en el pipeline:

#### **Tests de Despliegue (siempre)**
- ✅ Configuración de la aplicación
- ✅ Conexión a MongoDB
- ✅ Configuración de Cloudinary
- ✅ Endpoints básicos (health, root)

#### **Tests de Funcionalidad (solo en develop)**
- ✅ Creación de solicitudes
- ✅ Obtención de solicitudes
- ✅ Actualización de estados
- ✅ Filtrado por estado

#### **Tests Completos (desarrollo local)**
- ✅ Todos los tests de despliegue
- ✅ Todos los tests de funcionalidad
- ✅ Tests de múltiples filtros
- ✅ Tests de autenticación

## 🚀 CI/CD Pipeline

### **Workflow: ci-cd.yml**

#### **Push a `develop`:**
1. ✅ **Tests críticos de despliegue** - Verifica configuración y conectividad
2. ✅ **Tests rápidos de funcionalidad** - Validación de endpoints principales
3. ✅ **Despliegue a staging** - Fly.io (https://solicitudes-staging.fly.dev)
4. ✅ **Validación** - Probar funcionalidades en staging

#### **Push a `main`:**
1. ✅ **Sincronización automática** - Con repo de producción
2. ✅ **Sin tests** - Ya validados en develop
3. ✅ **Despliegue a producción** - Automático desde repo de producción

### **Flujo Optimizado:**
```
Desarrollo → Tests Locales → Push a Develop → Tests CI/CD → Staging → 
Validación Manual → Merge a Main → Producción
```

### **Variables de Entorno Requeridas:**
- `