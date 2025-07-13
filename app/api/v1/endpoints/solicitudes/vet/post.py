from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, Body
from typing import Annotated
from app.schemas.solicitud import Solicitud, SolicitudCreate, SolicitudCreateWithImage, SolicitudCreateInput
from app.schemas.auth import AuthenticatedUser
from app.models.solicitud_mongo import SolicitudMongoModel
from app.api.dependencies import get_current_user_clinic

from app.services.cloudinary_service import upload_image
from datetime import datetime
import secrets
import json

router = APIRouter()

def get_solicitud_create_input(
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
    urgencia: str = Form(..., description="Nivel de urgencia (Alta, Media, Baja)")
) -> SolicitudCreateInput:
    return SolicitudCreateInput(
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
                        "foto_mascota": "https://res.cloudinary.com/cloud_name/image/upload/v1234567890/mascotas/image.jpg"
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
    current_user: Annotated[AuthenticatedUser, Depends(get_current_user_clinic)],
    solicitud_data: SolicitudCreateInput = Depends(get_solicitud_create_input),
    foto_mascota: UploadFile = File(None, description="Imagen de la mascota (opcional)")
):
    """
    Crea una nueva solicitud de donación de sangre.
    Puede incluir imagen de la mascota (opcional).
    Endpoint exclusivo para veterinarias.
    
    Args:
        solicitud_data (SolicitudCreateInput): Datos de la solicitud
        foto_mascota (UploadFile): Imagen de la mascota (opcional)
    
    Returns:
        Solicitud: Solicitud creada
        
    Raises:
        HTTPException: Si ocurre un error al procesar la solicitud
    """
    try:
        # Validar datos usando el esquema
        solicitud_validada = SolicitudCreateWithImage(**solicitud_data.model_dump())
        
        # Subir imagen si se proporcionó
        foto_url = None
        if foto_mascota:
            # Generar un ID en formato hexadecimal de 24 caracteres
            solicitud_id = secrets.token_hex(12)  # 12 bytes = 24 caracteres hexadecimales
            try:
                foto_url = upload_image(foto_mascota.file, public_id=solicitud_id)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error al subir la imagen: {str(e)}"
                )
        else:
            solicitud_id = secrets.token_hex(12)
        # Crear la solicitud con el ID y fecha específicos
        nueva_solicitud = {
            "id": solicitud_id,
            "fecha_creacion": datetime.now().isoformat(),
            "estado": "Activa",
            "foto_mascota": foto_url,
            **solicitud_validada.model_dump()
        }
        return await SolicitudMongoModel.create_solicitud(nueva_solicitud)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear la solicitud: {str(e)}"
        )

 