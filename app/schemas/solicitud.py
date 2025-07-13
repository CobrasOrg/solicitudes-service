from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from fastapi import UploadFile
from app.constants.solicitudes import (
    ESTADOS_PERMITIDOS,
    ESPECIES_PERMITIDAS,
    TIPOS_SANGRE_PERMITIDOS,
    URGENCIAS_PERMITIDAS,
    LOCALIDADES_PERMITIDAS
)

class Solicitud(BaseModel):
    id: str = Field(..., alias="id")
    nombre_veterinaria: str
    nombre_mascota: str
    especie: str
    localidad: str
    descripcion_solicitud: str
    direccion: str
    ubicacion: str
    contacto: str
    peso_minimo: float
    tipo_sangre: str
    urgencia: str
    estado: str
    fecha_creacion: datetime
    foto_mascota: Optional[str] = None

    @field_validator('especie')
    @classmethod
    def validate_especie(cls, v):
        if v not in ESPECIES_PERMITIDAS:
            raise ValueError(f"Especie inválida. Las especies permitidas son: {', '.join(ESPECIES_PERMITIDAS)}")
        return v

    @field_validator('tipo_sangre')
    @classmethod
    def validate_tipo_sangre(cls, v):
        if v not in TIPOS_SANGRE_PERMITIDOS:
            raise ValueError(f"Tipo de sangre inválido. Los tipos permitidos son: {', '.join(TIPOS_SANGRE_PERMITIDOS)}")
        return v

    @field_validator('urgencia')
    @classmethod
    def validate_urgencia(cls, v):
        if v not in URGENCIAS_PERMITIDAS:
            raise ValueError(f"Urgencia inválida. Los niveles permitidos son: {', '.join(URGENCIAS_PERMITIDAS)}")
        return v

    @field_validator('localidad')
    @classmethod
    def validate_localidad(cls, v):
        if v not in LOCALIDADES_PERMITIDAS:
            raise ValueError(f"Localidad inválida. Las localidades permitidas son: {', '.join(LOCALIDADES_PERMITIDAS)}")
        return v

    @field_validator('estado')
    @classmethod
    def validate_estado(cls, v):
        if v not in ESTADOS_PERMITIDOS:
            raise ValueError(f"Estado inválido. Los estados permitidos son: {', '.join(ESTADOS_PERMITIDOS)}")
        return v

    model_config = ConfigDict(
        populate_by_name=True,
        title="Solicitud de Donación",
        description="Modelo completo de una solicitud de donación de sangre",
        json_schema_extra={
            "example": {
                "id": "684a01e4c351aa9d49b145c2",
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
                "fecha_creacion": "2025-06-12T18:32:00.000000",
                "urgencia": "Alta",
                "estado": "Completada",
                "foto_mascota": "https://ejemplo.com/foto-canela.jpg"
            }
        }
    )

class SolicitudCreate(BaseModel):
    nombre_veterinaria: str
    nombre_mascota: str
    especie: str
    localidad: str
    descripcion_solicitud: str
    direccion: str
    ubicacion: str
    contacto: str
    peso_minimo: float
    tipo_sangre: str
    urgencia: str
    foto_mascota: Optional[str] = None

    @field_validator('especie')
    @classmethod
    def validate_especie(cls, v):
        if v not in ESPECIES_PERMITIDAS:
            raise ValueError(f"Especie inválida. Las especies permitidas son: {', '.join(ESPECIES_PERMITIDAS)}")
        return v

    @field_validator('tipo_sangre')
    @classmethod
    def validate_tipo_sangre(cls, v):
        if v not in TIPOS_SANGRE_PERMITIDOS:
            raise ValueError(f"Tipo de sangre inválido. Los tipos permitidos son: {', '.join(TIPOS_SANGRE_PERMITIDOS)}")
        return v

    @field_validator('urgencia')
    @classmethod
    def validate_urgencia(cls, v):
        if v not in URGENCIAS_PERMITIDAS:
            raise ValueError(f"Urgencia inválida. Los niveles permitidos son: {', '.join(URGENCIAS_PERMITIDAS)}")
        return v

    @field_validator('localidad')
    @classmethod
    def validate_localidad(cls, v):
        if v not in LOCALIDADES_PERMITIDAS:
            raise ValueError(f"Localidad inválida. Las localidades permitidas son: {', '.join(LOCALIDADES_PERMITIDAS)}")
        return v

    model_config = ConfigDict(
        extra='forbid',
        title="Datos para Crear Solicitud",
        description="Datos requeridos para crear una nueva solicitud de donación",
        json_schema_extra={
            "example": {
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
                "urgencia": "Alta",
                "foto_mascota": "https://ejemplo.com/foto-canela.jpg"
            }
        }
    )

# Nuevo esquema para crear solicitud con archivo de imagen
class SolicitudCreateWithImage(BaseModel):
    nombre_veterinaria: str
    nombre_mascota: str
    especie: str
    localidad: str
    descripcion_solicitud: str
    direccion: str
    ubicacion: str
    contacto: str
    peso_minimo: float
    tipo_sangre: str
    urgencia: str

    @field_validator('especie')
    @classmethod
    def validate_especie(cls, v):
        if v not in ESPECIES_PERMITIDAS:
            raise ValueError(f"Especie inválida. Las especies permitidas son: {', '.join(ESPECIES_PERMITIDAS)}")
        return v

    @field_validator('tipo_sangre')
    @classmethod
    def validate_tipo_sangre(cls, v):
        if v not in TIPOS_SANGRE_PERMITIDOS:
            raise ValueError(f"Tipo de sangre inválido. Los tipos permitidos son: {', '.join(TIPOS_SANGRE_PERMITIDOS)}")
        return v

    @field_validator('urgencia')
    @classmethod
    def validate_urgencia(cls, v):
        if v not in URGENCIAS_PERMITIDAS:
            raise ValueError(f"Urgencia inválida. Los niveles permitidos son: {', '.join(URGENCIAS_PERMITIDAS)}")
        return v

    @field_validator('localidad')
    @classmethod
    def validate_localidad(cls, v):
        if v not in LOCALIDADES_PERMITIDAS:
            raise ValueError(f"Localidad inválida. Las localidades permitidas son: {', '.join(LOCALIDADES_PERMITIDAS)}")
        return v

    model_config = ConfigDict(
        extra='forbid',
        title="Datos para Crear Solicitud con Imagen",
        description="Datos requeridos para crear una nueva solicitud de donación con imagen de la mascota",
        json_schema_extra={
            "example": {
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
                "urgencia": "Alta"
            }
        }
    )

# Esquemas específicos para parámetros de entrada
class SolicitudCreateInput(BaseModel):
    nombre_veterinaria: str = Field(..., description="Nombre de la veterinaria o clínica")
    nombre_mascota: str = Field(..., description="Nombre de la mascota que necesita la donación")
    especie: str = Field(..., description="Especie de la mascota (Perro, Gato, etc.)")
    localidad: str = Field(..., description="Localidad donde se encuentra la veterinaria")
    descripcion_solicitud: str = Field(..., description="Descripción detallada de la solicitud y situación de la mascota")
    direccion: str = Field(..., description="Dirección física de la veterinaria")
    ubicacion: str = Field(..., description="Ubicación específica (barrio, ciudad)")
    contacto: str = Field(..., description="Número de teléfono o contacto de la veterinaria")
    peso_minimo: float = Field(..., description="Peso mínimo requerido para el donante (en kg)")
    tipo_sangre: str = Field(..., description="Tipo de sangre requerido para la donación")
    urgencia: str = Field(..., description="Nivel de urgencia (Alta, Media, Baja)")

    @field_validator('especie')
    @classmethod
    def validate_especie(cls, v):
        if v not in ESPECIES_PERMITIDAS:
            raise ValueError(f"Especie inválida. Las especies permitidas son: {', '.join(ESPECIES_PERMITIDAS)}")
        return v

    @field_validator('tipo_sangre')
    @classmethod
    def validate_tipo_sangre(cls, v):
        if v not in TIPOS_SANGRE_PERMITIDOS:
            raise ValueError(f"Tipo de sangre inválido. Los tipos permitidos son: {', '.join(TIPOS_SANGRE_PERMITIDOS)}")
        return v

    @field_validator('urgencia')
    @classmethod
    def validate_urgencia(cls, v):
        if v not in URGENCIAS_PERMITIDAS:
            raise ValueError(f"Urgencia inválida. Los niveles permitidos son: {', '.join(URGENCIAS_PERMITIDAS)}")
        return v

    @field_validator('localidad')
    @classmethod
    def validate_localidad(cls, v):
        if v not in LOCALIDADES_PERMITIDAS:
            raise ValueError(f"Localidad inválida. Las localidades permitidas son: {', '.join(LOCALIDADES_PERMITIDAS)}")
        return v

    model_config = ConfigDict(
        title="Datos de Entrada para Crear Solicitud",
        description="Parámetros requeridos para crear una nueva solicitud de donación",
        json_schema_extra={
            "example": {
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
                "urgencia": "Alta"
            }
        }
    )

class SolicitudUpdateInput(BaseModel):
    especie: Optional[str] = Field(None, description="Nueva especie de la mascota")
    tipo_sangre: Optional[str] = Field(None, description="Nuevo tipo de sangre requerido")
    urgencia: Optional[str] = Field(None, description="Nuevo nivel de urgencia")
    peso_minimo: Optional[float] = Field(None, description="Nuevo peso mínimo requerido (en kg)")
    descripcion_solicitud: Optional[str] = Field(None, description="Nueva descripción de la solicitud")
    direccion: Optional[str] = Field(None, description="Nueva dirección de la veterinaria")
    estado: Optional[str] = Field(None, description="Nuevo estado de la solicitud")

    @field_validator('especie')
    @classmethod
    def validate_especie(cls, v):
        if v is not None and v not in ESPECIES_PERMITIDAS:
            raise ValueError(f"Especie inválida. Las especies permitidas son: {', '.join(ESPECIES_PERMITIDAS)}")
        return v

    @field_validator('tipo_sangre')
    @classmethod
    def validate_tipo_sangre(cls, v):
        if v is not None and v not in TIPOS_SANGRE_PERMITIDOS:
            raise ValueError(f"Tipo de sangre inválido. Los tipos permitidos son: {', '.join(TIPOS_SANGRE_PERMITIDOS)}")
        return v

    @field_validator('urgencia')
    @classmethod
    def validate_urgencia(cls, v):
        if v is not None and v not in URGENCIAS_PERMITIDAS:
            raise ValueError(f"Urgencia inválida. Los niveles permitidos son: {', '.join(URGENCIAS_PERMITIDAS)}")
        return v

    @field_validator('estado')
    @classmethod
    def validate_estado(cls, v):
        if v is not None and v not in ESTADOS_PERMITIDOS:
            raise ValueError(f"Estado inválido. Los estados permitidos son: {', '.join(ESTADOS_PERMITIDOS)}")
        return v

    model_config = ConfigDict(
        title="Datos de Entrada para Actualizar Solicitud",
        description="Parámetros opcionales para actualizar una solicitud existente",
        json_schema_extra={
            "example": {
                "especie": "Gato",
                "tipo_sangre": "A",
                "urgencia": "Media",
                "peso_minimo": 4.5,
                "descripcion_solicitud": "Actualización de la descripción de la solicitud",
                "direccion": "Nueva dirección de la veterinaria",
                "estado": "Revision"
            }
        }
    )

class SolicitudEstadoUpdate(BaseModel):
    estado: str = Field(..., description="Nuevo estado de la solicitud")

    @field_validator('estado')
    @classmethod
    def validate_estado(cls, v):
        if v not in ESTADOS_PERMITIDOS:
            raise ValueError(f'Estado no válido. Valores permitidos: {", ".join(ESTADOS_PERMITIDOS)}')
        return v

    model_config = ConfigDict(
        title="Actualización de Estado",
        description="Datos para actualizar el estado de una solicitud",
        json_schema_extra={
            "example": {
                "estado": "Completada"
            }
        }
    )

class SolicitudUpdate(BaseModel):
    especie: Optional[str] = None
    tipo_sangre: Optional[str] = None
    urgencia: Optional[str] = None
    peso_minimo: Optional[float] = None
    descripcion_solicitud: Optional[str] = None
    direccion: Optional[str] = None
    estado: Optional[str] = None
    foto_mascota: Optional[str] = None

    @field_validator('especie')
    @classmethod
    def validate_especie(cls, v):
        if v is not None and v not in ESPECIES_PERMITIDAS:
            raise ValueError(f"Especie inválida. Las especies permitidas son: {', '.join(ESPECIES_PERMITIDAS)}")
        return v

    @field_validator('tipo_sangre')
    @classmethod
    def validate_tipo_sangre(cls, v):
        if v is not None and v not in TIPOS_SANGRE_PERMITIDOS:
            raise ValueError(f"Tipo de sangre inválido. Los tipos permitidos son: {', '.join(TIPOS_SANGRE_PERMITIDOS)}")
        return v

    @field_validator('urgencia')
    @classmethod
    def validate_urgencia(cls, v):
        if v is not None and v not in URGENCIAS_PERMITIDAS:
            raise ValueError(f"Urgencia inválida. Los niveles permitidos son: {', '.join(URGENCIAS_PERMITIDAS)}")
        return v

    @field_validator('estado')
    @classmethod
    def validate_estado(cls, v):
        if v is not None and v not in ESTADOS_PERMITIDOS:
            raise ValueError(f"Estado inválido. Los estados permitidos son: {', '.join(ESTADOS_PERMITIDOS)}")
        return v

    model_config = ConfigDict(
        title="Datos para Actualizar Solicitud",
        description="Datos opcionales para actualizar una solicitud existente",
        json_schema_extra={
            "example": {
                "especie": "Gato",
                "tipo_sangre": "A",
                "urgencia": "Media",
                "peso_minimo": 4.5,
                "descripcion_solicitud": "Actualización de la descripción de la solicitud",
                "direccion": "Nueva dirección de la veterinaria",
                "estado": "Revision",
                "foto_mascota": "https://ejemplo.com/nueva-foto.jpg"
            }
        }
    ) 