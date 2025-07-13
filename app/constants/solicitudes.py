from typing import List

# Estados permitidos
ESTADOS_PERMITIDOS: List[str] = [
    'Activa',
    'Completada',
    'Cancelada',
    'Revision'
]

# Especies permitidas
ESPECIES_PERMITIDAS: List[str] = [
    'Perro',
    'Gato'
]

# Tipos de sangre permitidos
TIPOS_SANGRE_PERMITIDOS: List[str] = [
    'DEA 1.1+',
    'DEA 1.1-',
    'A',
    'B',
    'AB'
]

# Niveles de urgencia permitidos
URGENCIAS_PERMITIDAS: List[str] = [
    'Alta',
    'Media'
]

# Localidades permitidas (ejemplo para Bogotá)
LOCALIDADES_PERMITIDAS: List[str] = [
    'Suba',
    'Chapinero',
    'Usaquén',
    'Bosa',
    'Kennedy',
    'Engativá',
    'Fontibón',
    'Barrios Unidos',
    'Teusaquillo',
    'Los Mártires',
    'Antonio Nariño',
    'Puente Aranda',
    'La Candelaria',
    'Rafael Uribe Uribe',
    'Ciudad Bolívar',
    'San Cristóbal',
    'Usme',
    'Sumapaz',
    'Santa Fe',
    'Tunjuelito'
]

# Campos permitidos para actualización
CAMPOS_ACTUALIZABLES: List[str] = [
    'especie',
    'tipo_sangre',
    'urgencia',
    'peso_minimo',
    'descripcion_solicitud',
    'direccion',
    'ubicacion'
] 