from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Body, Request, Depends
from typing import Optional, Union, Annotated
from app.schemas.solicitud import SolicitudUpdate, SolicitudEstadoUpdate, Solicitud
from app.schemas.auth import AuthenticatedUser
from app.models.solicitud_mongo import SolicitudMongoModel
from app.api.dependencies import get_current_user_clinic

from app.constants.solicitudes import ESTADOS_PERMITIDOS
import json
from app.services.cloudinary_service import upload_image
import cloudinary.uploader

router = APIRouter()

@router.patch(
    "/{solicitud_id}",
    response_model=Solicitud,
    summary="Actualizar solicitud (JSON o Formulario)",
    description="Actualiza los datos de una solicitud existente. Acepta tanto JSON como datos de formulario. Solo se actualizan los campos enviados. Endpoint exclusivo para veterinarias.",
    responses={
        200: {
            "description": "Solicitud actualizada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": "684a01e4c351aa9d49b145b8",
                        "nombre_veterinaria": "Veterinaria San Patricio",
                        "nombre_mascota": "Rocky",
                        "especie": "Perro",
                        "localidad": "Suba",
                        "descripcion_solicitud": "Rocky es un pastor alemán de 5 años que ha sido diagnosticado con anemia severa después de una complicación durante una cirugía de emergencia.",
                        "direccion": "Clínica VetCentral, Av. Principal 123",
                        "ubicacion": "Suba, Bogotá",
                        "contacto": "+57 300 123 4567",
                        "peso_minimo": 25,
                        "tipo_sangre": "DEA 1.1+",
                        "fecha_creacion": "2024-02-14T10:30:00",
                        "urgencia": "Alta",
                        "estado": "Activa",
                        "foto_mascota": "https://res.cloudinary.com/cloud_name/image/upload/v1234567890/mascotas/new-image.jpg"
                    }
                }
            }
        },
        400: {
            "description": "Datos inválidos o error en imagen",
            "content": {
                "application/json": {
                    "example": {"detail": "Datos de la solicitud inválidos o error en el archivo de imagen"}
                }
            }
        },
        404: {
            "description": "Solicitud no encontrada",
            "content": {
                "application/json": {
                    "example": {"detail": "Solicitud no encontrada"}
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
async def update_solicitud(
    current_user: Annotated[AuthenticatedUser, Depends(get_current_user_clinic)],
    request: Request,
    solicitud_id: str,
    especie: Optional[str] = Form(None, description="Nueva especie de la mascota"),
    tipo_sangre: Optional[str] = Form(None, description="Nuevo tipo de sangre requerido"),
    urgencia: Optional[str] = Form(None, description="Nuevo nivel de urgencia"),
    peso_minimo: Optional[Union[float, str]] = Form(None, description="Nuevo peso mínimo requerido (en kg)"),
    descripcion_solicitud: Optional[str] = Form(None, description="Nueva descripción de la solicitud"),
    direccion: Optional[str] = Form(None, description="Nueva dirección de la veterinaria"),
    estado: Optional[str] = Form(None, description="Nuevo estado de la solicitud"),
    foto_mascota: Optional[UploadFile] = File(None, description="Nueva imagen de la mascota (opcional)")
):
    try:
        solicitud_actual = await SolicitudMongoModel.get_solicitud_by_id(solicitud_id)
        if not solicitud_actual:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        update_data = {}
        if especie is not None and especie != "":
            update_data["especie"] = especie
        if tipo_sangre is not None and tipo_sangre != "":
            update_data["tipo_sangre"] = tipo_sangre
        if urgencia is not None and urgencia != "":
            update_data["urgencia"] = urgencia
        if peso_minimo is not None and peso_minimo != "":
            if isinstance(peso_minimo, str):
                try:
                    peso_minimo = float(peso_minimo)
                except ValueError:
                    raise HTTPException(status_code=400, detail="peso_minimo debe ser un número válido")
            update_data["peso_minimo"] = peso_minimo
        if descripcion_solicitud is not None and descripcion_solicitud != "":
            update_data["descripcion_solicitud"] = descripcion_solicitud
        if direccion is not None and direccion != "":
            update_data["direccion"] = direccion
        if estado is not None and estado != "":
            update_data["estado"] = estado
        if foto_mascota:
            if solicitud_actual.foto_mascota:
                try:
                    url = solicitud_actual.foto_mascota
                    public_id = url.split("/petmatch-solicitudes/")[-1].split(".")[0]
                    cloudinary.uploader.destroy(f"petmatch-solicitudes/{public_id}")
                except Exception as e:
                    print(f"Error eliminando imagen de Cloudinary: {str(e)}")
            nueva_foto_url = upload_image(foto_mascota.file, public_id=solicitud_id)
            if nueva_foto_url:
                update_data["foto_mascota"] = nueva_foto_url
        if not update_data:
            return solicitud_actual
        solicitud_update = SolicitudUpdate(**update_data)
        solicitud_actualizada = await SolicitudMongoModel.update_solicitud_datos(solicitud_id, solicitud_update)
        if not solicitud_actualizada:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        return solicitud_actualizada
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor al procesar la solicitud")



@router.patch(
    "/{solicitud_id}/estado",
    response_model=Solicitud,
    summary="Actualizar estado de solicitud",
    description="Actualiza el estado de una solicitud existente. Endpoint exclusivo para veterinarias.",
    responses={
        200: {
            "description": "Estado de la solicitud actualizado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": "684a01e4c351aa9d49b145b8",
                        "nombre_veterinaria": "Veterinaria San Patricio",
                        "nombre_mascota": "Rocky",
                        "especie": "Perro",
                        "localidad": "Suba",
                        "descripcion_solicitud": "Rocky es un pastor alemán de 5 años que ha sido diagnosticado con anemia severa después de una complicación durante una cirugía de emergencia.",
                        "direccion": "Clínica VetCentral, Av. Principal 123",
                        "ubicacion": "Suba, Bogotá",
                        "contacto": "+57 300 123 4567",
                        "peso_minimo": 25,
                        "tipo_sangre": "DEA 1.1+",
                        "fecha_creacion": "2024-02-14T10:30:00",
                        "urgencia": "Alta",
                        "estado": "Revision",
                        "foto_mascota": "https://ejemplo.com/foto-rocky.jpg"
                    }
                }
            }
        },
        400: {
            "description": "Estado inválido",
            "content": {
                "application/json": {
                    "example": {"detail": f"Estado inválido. Los estados válidos son: {', '.join(ESTADOS_PERMITIDOS)}"}
                }
            }
        },
        404: {
            "description": "Solicitud no encontrada",
            "content": {
                "application/json": {
                    "example": {"detail": "Solicitud no encontrada"}
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
async def update_solicitud_estado(
    solicitud_id: str, 
    estado_update: SolicitudEstadoUpdate,
    current_user: Annotated[AuthenticatedUser, Depends(get_current_user_clinic)]
):
    """
    Actualiza el estado de una solicitud existente.
    Endpoint exclusivo para veterinarias.
    
    Args:
        solicitud_id (str): ID de la solicitud a actualizar
        estado_update (SolicitudEstadoUpdate): Nuevo estado de la solicitud
    
    Returns:
        Solicitud: Solicitud con estado actualizado
        
    Raises:
        HTTPException: Si ocurre un error al procesar la solicitud, si el estado es inválido o si la solicitud no existe
    """
    try:
        print(f"[DEBUG] update_solicitud_estado endpoint: ID={solicitud_id}, estado={estado_update.estado}")
        
        # Validar que el estado sea válido
        if estado_update.estado not in ESTADOS_PERMITIDOS:
            raise HTTPException(
                status_code=400,
                detail=f"Estado inválido. Los estados válidos son: {', '.join(ESTADOS_PERMITIDOS)}"
            )
        
        # Verificar que la solicitud existe antes de actualizar
        solicitud_existente = await SolicitudMongoModel.get_solicitud_by_id(solicitud_id)
        if not solicitud_existente:
            print(f"[DEBUG] update_solicitud_estado endpoint: Solicitud no encontrada")
            raise HTTPException(
                status_code=404,
                detail="Solicitud no encontrada"
            )
        
        print(f"[DEBUG] update_solicitud_estado endpoint: Solicitud encontrada, estado actual={solicitud_existente.estado}")
        
        # Solo actualizar si el estado es diferente
        if solicitud_existente.estado == estado_update.estado:
            print(f"[DEBUG] update_solicitud_estado endpoint: Estado ya es {estado_update.estado}, retornando solicitud actual")
            return solicitud_existente
        
        solicitud_actualizada = await SolicitudMongoModel.update_solicitud_estado(solicitud_id, estado_update.estado)
        if not solicitud_actualizada:
            print(f"[DEBUG] update_solicitud_estado endpoint: Error en actualización")
            raise HTTPException(
                status_code=404,
                detail="Solicitud no encontrada"
            )
        
        print(f"[DEBUG] update_solicitud_estado endpoint: Actualización exitosa")
        return solicitud_actualizada
        
    except ValueError as e:
        print(f"[DEBUG] update_solicitud_estado endpoint: ValueError - {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[DEBUG] update_solicitud_estado endpoint: Exception - {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al procesar la solicitud"
        ) 