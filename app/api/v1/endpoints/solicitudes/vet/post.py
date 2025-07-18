from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import Annotated
from app.schemas.solicitud import Solicitud, SolicitudCreate, SolicitudCreateWithImage, SolicitudCreateInput
from app.schemas.auth import AuthenticatedUser
from app.models.solicitud_mongo import SolicitudMongoModel
from app.api.dependencies import get_current_user_clinic, get_current_user_id_clinic
from pydantic import ValidationError

from app.services.cloudinary_service import upload_image
from datetime import datetime
import secrets
import json

router = APIRouter()

@router.post(
    "/",
    response_model=Solicitud,
    status_code=201,
    summary="Crear solicitud de donación",
    description="Crea una nueva solicitud de donación de sangre. Puede incluir imagen de la mascota. Endpoint exclusivo para veterinarias.",
    responses={
        201: {
            "description": "Solicitud creada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": "684a01e4c351aa9d49b145b8",
                        "nombre_veterinaria": "AnimalCare",
                        "nombre_mascota": "Canela",
                        "especie": "Perro",
                        "localidad": "Usaquén",
                        "descripcion_solicitud": "Canela está anémica por parásitos y necesita una transfusión urgente.",
                        "direccion": "Av. 19 #120-56",
                        "ubicacion": "Usaquén, Bogotá",
                        "contacto": "+57 301 234 5678",
                        "peso_minimo": 18.0,
                        "tipo_sangre": "DEA 1.1+",
                        "fecha_creacion": "2025-06-13T21:01:38.439421",
                        "urgencia": "Alta",
                        "estado": "Activa",
                        "foto_mascota": "https://res.cloudinary.com/cloud_name/image/upload/v1234567890/mascotas/image.jpg",
                        "ownerId": "user_123"
                    }
                }
            }
        },
        400: {
            "description": "Error en el archivo de imagen",
            "content": {
                "application/json": {
                    "example": {"detail": "El archivo debe ser una imagen"}
                }
            }
        },
        401: {
            "description": "No autorizado - Token requerido",
            "content": {
                "application/json": {
                    "example": {"detail": "No autorizado"}
                }
            }
        },
        422: {
            "description": "Error de validación",
            "content": {
                "application/json": {
                    "example": {"detail": "Error de validación en los datos de la solicitud"}
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Error interno del servidor al procesar la solicitud"}
                }
            }
        }
    }
)
async def create_solicitud(
    current_user_id: Annotated[str, Depends(get_current_user_id_clinic)],
    nombre_veterinaria: str = Form(..., description="Nombre de la veterinaria o clínica"),
    nombre_mascota: str = Form(..., description="Nombre de la mascota que necesita la donación"),
    especie: str = Form(..., description="Especie de la mascota (Perro, Gato, etc.)"),
    localidad: str = Form(..., description="Localidad donde se encuentra la veterinaria"),
    descripcion_solicitud: str = Form(..., description="Descripción detallada de la solicitud y situación de la mascota"),
    direccion: str = Form(..., description="Dirección física de la veterinaria"),
    ubicacion: str = Form(..., description="Ubicación específica (barrio, ciudad)"),
    contacto: str = Form(..., description="Número de teléfono o contacto de la veterinaria"),
    peso_minimo: float = Form(..., description="Peso mínimo requerido para el donante (en kg)"),
    tipo_sangre: str = Form(..., description="Tipo de sangre requerido para la donación"),
    urgencia: str = Form(..., description="Nivel de urgencia (Alta, Media, Baja)"),
    foto_mascota: UploadFile = File(None, description="Imagen de la mascota (opcional)")
):
    """
    Crea una nueva solicitud de donación de sangre.
    Puede incluir imagen de la mascota (opcional).
    Endpoint exclusivo para veterinarias.
    """
    # Construir el modelo Pydantic dentro del endpoint para que FastAPI maneje los errores de validación
    try:
        solicitud_validada = SolicitudCreateWithImage(
            nombre_veterinaria=nombre_veterinaria,
            nombre_mascota=nombre_mascota,
            especie=especie,
            localidad=localidad,
            descripcion_solicitud=descripcion_solicitud,
            direccion=direccion,
            ubicacion=ubicacion,
            contacto=contacto,
            peso_minimo=peso_minimo,
            tipo_sangre=tipo_sangre,
            urgencia=urgencia
        )
    except ValidationError as e:
        # Convertir errores de validación de Pydantic a errores HTTP 422
        error_details = []
        for error in e.errors():
            field = error['loc'][0] if error['loc'] else 'unknown'
            message = error['msg']
            error_details.append(f"{field}: {message}")
        
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Error de validación en los datos de la solicitud",
                "errors": error_details
            }
        )
    
    # Subir imagen si se proporcionó
    foto_url = None
    solicitud_id = secrets.token_hex(12)  # 12 bytes = 24 caracteres hexadecimales
    if foto_mascota:
        try:
            foto_url = upload_image(foto_mascota.file, public_id=solicitud_id)
        except Exception as e:
            print(f"[DEBUG][POST /vet] Error al subir imagen: {type(e).__name__}: {e}")
            raise HTTPException(
                status_code=400,
                detail=f"Error al subir la imagen: {str(e)}"
            )
    
    # Crear la solicitud con el ID y fecha específicos
    nueva_solicitud = {
        "id": solicitud_id,
        "fecha_creacion": datetime.now().isoformat(),
        "estado": "Activa",
        "foto_mascota": foto_url,
        **solicitud_validada.model_dump()
    }
    
    # Crear la solicitud asociada al usuario autenticado
    return await SolicitudMongoModel.create_solicitud_with_owner(nueva_solicitud, current_user_id)

 