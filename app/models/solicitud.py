from datetime import datetime
from typing import List, Optional, Dict
from app.schemas.solicitud import Solicitud, SolicitudCreate, SolicitudUpdate, SolicitudEstadoUpdate
import uuid
import json
import os
from app.constants.solicitudes import ESTADOS_PERMITIDOS

# Cargar datos mock desde el archivo JSON
def load_mock_data() -> List[Dict]:
    """
    Carga los datos mock desde el archivo JSON
    Returns:
        List[Dict]: Lista de solicitudes
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(os.path.dirname(current_dir), 'data', 'mock_data.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('solicitudes', [])
    except Exception as e:
        print(f"Error cargando datos mock: {str(e)}")
        return []

# Cargar datos mock
MOCK_SOLICITUDES = load_mock_data()

class SolicitudModel:
    @staticmethod
    def get_active_solicitudes() -> List[Solicitud]:
        """
        Get all active solicitations
        Returns:
            List[Solicitud]: List of active solicitations
        """
        return [Solicitud(**solicitud) for solicitud in MOCK_SOLICITUDES if solicitud["estado"] == "Activa"]

    @staticmethod
    def get_all_solicitudes() -> List[Solicitud]:
        """
        Get all solicitations
        Returns:
            List[Solicitud]: List of all solicitations
        """
        return [Solicitud(**solicitud) for solicitud in MOCK_SOLICITUDES]

    @staticmethod
    def get_solicitudes_by_status(estado: Optional[str] = None) -> List[Solicitud]:
        """
        Get solicitations filtered by status
        Args:
            estado (Optional[str]): Status to filter by ('Activa', 'Completada', 'Cancelada', 'Revision')
        Returns:
            List[Solicitud]: List of solicitations matching the status
        """
        if estado:
            return [Solicitud(**solicitud) for solicitud in MOCK_SOLICITUDES if solicitud["estado"] == estado]
        return SolicitudModel.get_all_solicitudes()

    @staticmethod
    def filter_active_solicitudes(
        especie: Optional[str] = None,
        tipo_sangre: Optional[str] = None,
        urgencia: Optional[str] = None,
        localidad: Optional[str] = None
    ) -> List[Solicitud]:
        """
        Filter active solicitations by multiple parameters
        Args:
            especie (Optional[str]): Especie to filter by
            tipo_sangre (Optional[str]): Tipo de sangre to filter by
            urgencia (Optional[str]): Urgencia to filter by
            localidad (Optional[str]): Localidad to filter by
        Returns:
            List[Solicitud]: List of active solicitations matching all provided filters
        """
        # Primero obtenemos las solicitudes activas
        solicitudes_activas = [solicitud for solicitud in MOCK_SOLICITUDES if solicitud["estado"] == "Activa"]
        
        # Aplicamos los filtros si están presentes
        if especie:
            solicitudes_activas = [
                solicitud for solicitud in solicitudes_activas 
                if solicitud["especie"].lower() == especie.lower()
            ]
        
        if tipo_sangre:
            solicitudes_activas = [
                solicitud for solicitud in solicitudes_activas 
                if solicitud["tipo_sangre"].lower() == tipo_sangre.lower()
            ]
        
        if urgencia:
            solicitudes_activas = [
                solicitud for solicitud in solicitudes_activas 
                if solicitud["urgencia"].lower() == urgencia.lower()
            ]
        
        if localidad:
            solicitudes_activas = [
                solicitud for solicitud in solicitudes_activas 
                if solicitud["localidad"].lower() == localidad.lower()
            ]
        
        return [Solicitud(**solicitud) for solicitud in solicitudes_activas]

    @staticmethod
    def create_solicitud(solicitud_data: Dict) -> Solicitud:
        """
        Create a new solicitation
        Args:
            solicitud_data (Dict): Solicitation data with ID and creation date
        Returns:
            Solicitud: Created solicitation
        """
        MOCK_SOLICITUDES.append(solicitud_data)
        return Solicitud(**solicitud_data)

    @staticmethod
    def delete_solicitud(solicitud_id: str) -> bool:
        """
        Delete a solicitation by ID
        Args:
            solicitud_id (str): ID of the solicitation to delete
        Returns:
            bool: True if deleted, False if not found
        """
        for i, solicitud in enumerate(MOCK_SOLICITUDES):
            if solicitud["id"] == solicitud_id:
                MOCK_SOLICITUDES.pop(i)
                return True
        return False

    @staticmethod
    def update_solicitud_estado(solicitud_id: str, estado: str) -> Optional[Solicitud]:
        """
        Update solicitation status
        Args:
            solicitud_id (str): ID of the solicitation
            estado (str): New status
        Returns:
            Optional[Solicitud]: Updated solicitation if found, None otherwise
        """
        for solicitud in MOCK_SOLICITUDES:
            if solicitud["id"] == solicitud_id:
                solicitud["estado"] = estado
                return Solicitud(**solicitud)
        return None

    @staticmethod
    def update_solicitud_datos(solicitud_id: str, solicitud_update: SolicitudUpdate) -> Optional[Solicitud]:
        """
        Update solicitation data
        Args:
            solicitud_id (str): ID of the solicitation
            solicitud_update (SolicitudUpdate): Updated solicitation data
        Returns:
            Optional[Solicitud]: Updated solicitation if found, None otherwise
        """
        for solicitud in MOCK_SOLICITUDES:
            if solicitud["id"] == solicitud_id:
                update_data = solicitud_update.model_dump(exclude_unset=True)
                solicitud.update(update_data)
                return Solicitud(**solicitud)
        return None

    @staticmethod
    def filter_solicitudes_by_status(
        estado: Optional[str] = None,
        especie: Optional[str] = None,
        tipo_sangre: Optional[str] = None,
        urgencia: Optional[str] = None,
        localidad: Optional[str] = None
    ) -> List[Solicitud]:
        """
        Get solicitations filtered by multiple criteria
        Args:
            estado (Optional[str]): Status to filter by ('Activa', 'Completada', 'Cancelada', 'Revision')
            especie (Optional[str]): Species to filter by
            tipo_sangre (Optional[str]): Blood type to filter by
            urgencia (Optional[str]): Urgency level to filter by
            localidad (Optional[str]): Location to filter by
        Returns:
            List[Solicitud]: List of solicitations matching the filters
        """
        # Iniciamos con todas las solicitudes
        filtered_solicitudes = MOCK_SOLICITUDES
        
        # Aplicamos los filtros si están presentes
        if estado:
            filtered_solicitudes = [s for s in filtered_solicitudes if s["estado"] == estado]
        if especie:
            filtered_solicitudes = [s for s in filtered_solicitudes if s["especie"] == especie]
        if tipo_sangre:
            filtered_solicitudes = [s for s in filtered_solicitudes if s["tipo_sangre"] == tipo_sangre]
        if urgencia:
            filtered_solicitudes = [s for s in filtered_solicitudes if s["urgencia"] == urgencia]
        if localidad:
            filtered_solicitudes = [s for s in filtered_solicitudes if s["localidad"] == localidad]
        
        return [Solicitud(**solicitud) for solicitud in filtered_solicitudes]

    @staticmethod
    def get_solicitud_by_id(solicitud_id: str) -> Optional[Solicitud]:
        """
        Get a specific solicitation by ID
        Args:
            solicitud_id (str): ID of the solicitation to get
        Returns:
            Optional[Solicitud]: Solicitation if found, None otherwise
        """
        for solicitud in MOCK_SOLICITUDES:
            if solicitud["id"] == solicitud_id:
                return Solicitud(**solicitud)
        return None 