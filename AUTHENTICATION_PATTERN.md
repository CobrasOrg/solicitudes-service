# Patrón de Autenticación - Solicitudes Service

## 🎯 **Resumen del Patrón Implementado**

Este documento describe el patrón de autenticación implementado en el servicio de solicitudes, que permite asociar cada solicitud con el usuario autenticado que la crea.

## 🔐 **Flujo de Autenticación**

### **1. Endpoint POST - Creación con Autenticación**

```python
# app/api/v1/endpoints/solicitudes/vet/post.py
async def create_solicitud(
    current_user_id: Annotated[str, Depends(get_current_user_id_clinic)],
    solicitud_data: SolicitudCreateInput = Depends(get_solicitud_create_input),
    foto_mascota: UploadFile = File(None, description="Imagen de la mascota (opcional)")
):
    # 1. Valida token y obtiene user_id
    # 2. Crea solicitud asociada al usuario
    return await SolicitudMongoModel.create_solicitud_with_owner(nueva_solicitud, current_user_id)
```

### **2. Dependencias - Validación de Token**

```python
# app/api/dependencies.py
async def get_current_user_id_clinic() -> str:
    """
    Dependencia para obtener el ID del usuario autenticado de tipo 'clinic'
    """
    return AuthService.get_current_user_id()
```

### **3. Servicio de Autenticación**

```python
# app/services/auth_service.py
@staticmethod
def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_type: str = Header(..., alias="X-User-Type")
) -> str:
    # 1. Extrae token del header Authorization
    # 2. Valida formato "Bearer <token>"
    # 3. Verifica token (prueba o servicio externo)
    # 4. Retorna user_id del token
    return user_id
```

### **4. Modelo - Asociación con Usuario**

```python
# app/models/solicitud_mongo.py
@staticmethod
async def create_solicitud_with_owner(solicitud_data: Dict, owner_id: str) -> Solicitud:
    # 1. Recibe owner_id del endpoint
    # 2. Agrega ownerId al documento
    data_to_insert["ownerId"] = owner_id
    # 3. Inserta en MongoDB
    result = await collection.insert_one(data_to_insert)
```

## 📋 **Headers Requeridos**

### **Para crear una solicitud:**

```bash
POST /api/v1/solicitudes/vet/
Headers:
  Authorization: Bearer <token>
  X-User-Type: clinic
```

### **Ejemplo de request:**

```bash
curl -X POST "https://solicitudes-service.fly.dev/api/v1/solicitudes/vet/" \
  -H "Authorization: Bearer valid_token_123" \
  -H "X-User-Type: clinic" \
  -F "nombre_veterinaria=AnimalCare" \
  -F "nombre_mascota=Canela" \
  -F "especie=Perro" \
  -F "localidad=Usaquén" \
  -F "descripcion_solicitud=Mascota que necesita donación" \
  -F "direccion=Av. 19 #120-56" \
  -F "ubicacion=Usaquén, Bogotá" \
  -F "contacto=+57 301 234 5678" \
  -F "peso_minimo=18.0" \
  -F "tipo_sangre=DEA 1.1+" \
  -F "urgencia=Alta"
```

## 🔍 **Respuesta de Ejemplo**

```json
{
  "id": "684a01e4c351aa9d49b145b8",
  "nombre_veterinaria": "AnimalCare",
  "nombre_mascota": "Canela",
  "especie": "Perro",
  "localidad": "Usaquén",
  "descripcion_solicitud": "Mascota que necesita donación",
  "direccion": "Av. 19 #120-56",
  "ubicacion": "Usaquén, Bogotá",
  "contacto": "+57 301 234 5678",
  "peso_minimo": 18.0,
  "tipo_sangre": "DEA 1.1+",
  "fecha_creacion": "2025-01-13T21:01:38.439421",
  "urgencia": "Alta",
  "estado": "Activa",
  "foto_mascota": null,
  "ownerId": "user_123"
}
```

## 🧪 **Tests de Autenticación**

### **Tests implementados:**

1. **Sin token** → Error 401
2. **Sin header X-User-Type** → Error 422
3. **UserType inválido** → Error 400
4. **Token válido de clínica** → Éxito 201
5. **Asociación con usuario** → Verificar ownerId
6. **Usuario tipo 'owner'** → Error 403 (solo clínicas)
7. **Con imagen y autenticación** → Éxito completo

### **Ejecutar tests:**

```bash
pytest tests/test_solicitudes_authentication.py -v
```

## 🚨 **Códigos de Error**

| Código | Descripción | Causa |
|--------|-------------|-------|
| 401 | No autorizado | Falta token o token inválido |
| 400 | Bad Request | UserType inválido |
| 403 | Forbidden | Usuario no tiene permisos |
| 422 | Validation Error | Falta header X-User-Type |

## 🔧 **Configuración para Producción**

### **Para integrar con un servicio de autenticación real:**

1. **Modificar `AuthService.get_current_user_id()`:**
   ```python
   # Validar JWT token con servicio externo
   # Extraer user_id del payload del token
   # Verificar permisos del usuario
   ```

2. **Configurar variables de entorno:**
   ```bash
   AUTH_SERVICE_URL=https://auth-service.com
   JWT_SECRET=your_jwt_secret
   ```

3. **Implementar validación de tokens:**
   ```python
   # Validar token con servicio de autenticación
   # Verificar expiración
   # Extraer claims del token
   ```

## 📊 **Ventajas del Patrón**

✅ **Seguridad**: Cada solicitud está asociada a un usuario autenticado
✅ **Trazabilidad**: Se puede rastrear quién creó cada solicitud
✅ **Autorización**: Solo clínicas pueden crear solicitudes
✅ **Escalabilidad**: Fácil de extender para más roles
✅ **Testing**: Tests completos de autenticación

## 🔄 **Próximos Pasos**

1. **Implementar validación real de JWT tokens**
2. **Agregar endpoints para filtrar por usuario**
3. **Implementar autorización por roles más granular**
4. **Agregar logs de auditoría**
5. **Implementar rate limiting por usuario** 