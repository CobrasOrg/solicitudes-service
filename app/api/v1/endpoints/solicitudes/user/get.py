from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Annotated
from app.schemas.solicitud import Solicitud
from app.schemas.auth import AuthenticatedUser
from app.models.solicitud_mongo import SolicitudMongoModel
from app.api.dependencies import get_current_user_owner

router = APIRouter()

@router.get(
    "/activas",
    response_model=List[Solicitud],
    summary="Obtener solicitudes activas",
    description="Retorna todas las solicitudes que tienen estado 'Activa'",
    responses={
        200: {
            "description": "Lista de solicitudes activas",
            "content": {
                "application/json": {
                    "example": [
                        {
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
                            "foto_mascota": "https://ejemplo.com/foto-rocky.jpg"
                        }
                    ]
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
async def get_active_solicitudes(
    current_user: Annotated[AuthenticatedUser, Depends(get_current_user_owner)]
):
    """
    Obtiene todas las solicitudes activas.
    
    Returns:
        List[Solicitud]: Lista de solicitudes activas
        
    Raises:
        HTTPException: Si ocurre un error al procesar la solicitud
    """
    try:
        solicitudes = await SolicitudMongoModel.get_active_solicitudes()
        return solicitudes
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al procesar la solicitud"
        )

@router.get(
    "/activas/filtrar",
    response_model=List[Solicitud],
    summary="Filtrar solicitudes activas",
    description="Retorna las solicitudes activas filtradas por especie, tipo de sangre, urgencia y/o localidad",
    responses={
        200: {
            "description": "Lista de solicitudes activas filtradas",
            "content": {
                "application/json": {
                    "example": [
                        {
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
                            "foto_mascota": "https://ejemplo.com/foto-rocky.jpg"
                        }
                    ]
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
async def filter_active_solicitudes(
    current_user: Annotated[AuthenticatedUser, Depends(get_current_user_owner)],
    especie: Optional[str] = Query(
        None,
        description="Filtrar por especie (ej: Perro, Gato). Múltiples valores separados por coma: Perro,Gato",
        examples={"value": "Perro", "multiple": "Perro,Gato"}
    ),
    tipo_sangre: Optional[str] = Query(
        None,
        description="Filtrar por tipo de sangre (ej: DEA 1.1+, A). Múltiples valores separados por coma: DEA 1.1+,A",
        examples={"value": "DEA 1.1+", "multiple": "DEA 1.1+,A"}
    ),
    urgencia: Optional[str] = Query(
        None,
        description="Filtrar por nivel de urgencia (Alta, Media, Baja). Múltiples valores separados por coma: Alta,Media",
        examples={"value": "Alta", "multiple": "Alta,Media"}
    ),
    localidad: Optional[str] = Query(
        None,
        description="Filtrar por localidad (ej: Suba, Chapinero). Múltiples valores separados por coma: Suba,Teusaquillo",
        examples={"value": "Suba", "multiple": "Suba,Teusaquillo"}
    )
):
    """
    Filtra las solicitudes activas por uno o más criterios.
    
    Args:
        especie (Optional[str]): Especie a filtrar. Múltiples valores separados por coma: "Perro,Gato"
        tipo_sangre (Optional[str]): Tipo de sangre a filtrar. Múltiples valores separados por coma: "DEA 1.1+,A"
        urgencia (Optional[str]): Nivel de urgencia a filtrar. Múltiples valores separados por coma: "Alta,Media"
        localidad (Optional[str]): Localidad a filtrar. Múltiples valores separados por coma: "Suba,Teusaquillo"
    
    Returns:
        List[Solicitud]: Lista de solicitudes activas que coinciden con los filtros
        
    Raises:
        HTTPException: Si ocurre un error al procesar la solicitud
        
    Examples:
        - Filtrar por una sola localidad: ?localidad=Suba
        - Filtrar por múltiples localidades: ?localidad=Suba,Teusaquillo
        - Filtrar por especie y urgencia: ?especie=Perro&urgencia=Alta,Media
        - Filtrar por múltiples criterios: ?especie=Perro,Gato&localidad=Suba,Chapinero&urgencia=Alta
    """
    try:
        solicitudes = await SolicitudMongoModel.filter_active_solicitudes(
            especie=especie,
            tipo_sangre=tipo_sangre,
            urgencia=urgencia,
            localidad=localidad
        )
        return solicitudes
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al procesar la solicitud"
        )

@router.get(
    "/{solicitud_id}",
    response_model=Solicitud,
    summary="Obtener solicitud específica",
    description="Retorna una solicitud específica por su ID",
    responses={
        200: {
            "description": "Solicitud encontrada",
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
                        "foto_mascota": "https://ejemplo.com/foto-rocky.jpg"
                    }
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
async def get_solicitud_by_id(
    solicitud_id: str,
    current_user: Annotated[AuthenticatedUser, Depends(get_current_user_owner)]
):
    """
    Obtiene una solicitud específica por su ID.
    
    Args:
        solicitud_id (str): ID de la solicitud a obtener
    
    Returns:
        Solicitud: Solicitud encontrada
        
    Raises:
        HTTPException: Si la solicitud no existe o ocurre un error
    """
    try:
        solicitud = await SolicitudMongoModel.get_solicitud_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(
                status_code=404,
                detail="Solicitud no encontrada"
            )
        return solicitud
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al procesar la solicitud"
        ) 