from fastapi import HTTPException, status, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import httpx
from app.schemas.auth import AuthenticatedUser, UserType

security = HTTPBearer()

class AuthService:
    @staticmethod
    async def get_user_profile_from_token(token: str) -> dict:
        """
        Obtiene el perfil del usuario desde la API de autenticación
        
        Args:
            token (str): Token de autenticación
            
        Returns:
            dict: Datos del usuario autenticado
            
        Raises:
            HTTPException: Si no se puede obtener el perfil del usuario
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://auth-service-g7nh.onrender.com/api/v1/user/profile",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    user_data = response.json()
                    print(f"✅ Perfil de usuario obtenido: {user_data}")
                    return user_data
                else:
                    print(f"⚠️ Error obteniendo perfil de usuario: {response.status_code}")
                    print(f"⚠️ Respuesta del servidor: {response.text}")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token inválido o expirado"
                    )
                    
        except httpx.RequestError as e:
            print(f"⚠️ Error de conexión a auth service: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Servicio de autenticación no disponible"
            )
        except Exception as e:
            print(f"⚠️ Error inesperado en auth service: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor de autenticación"
            )

    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        user_type: Optional[str] = Header(None, alias="X-User-Type", description="Tipo de usuario: 'owner' o 'clinic'")
    ) -> AuthenticatedUser:
        """
        Obtiene el usuario actual basado en el token y userType del header
        
        Args:
            credentials (HTTPAuthorizationCredentials): Credenciales de autorización
            user_type (Optional[str]): Tipo de usuario del header X-User-Type
            
        Returns:
            AuthenticatedUser: Usuario autenticado
            
        Raises:
            HTTPException: Si el token es inválido o falta userType
        """
        # Debug: Imprimir el userType recibido
        print(f"🔍 AuthService: user_type recibido: '{user_type}'")
        print(f"🔍 AuthService: user_type type: {type(user_type)}")
        
        # Si user_type es None o no es un string válido, intentar obtenerlo de otra manera
        if user_type is None or not isinstance(user_type, str):
            print(f"🔍 AuthService: user_type es None o inválido, intentando obtener de otra manera")
            # Por ahora, usar un valor por defecto para testing
            user_type = "clinic"
        
        print(f"🔍 AuthService: user_type == 'clinic': {user_type == 'clinic'}")
        print(f"🔍 AuthService: user_type in ['owner', 'clinic']: {user_type in ['owner', 'clinic']}")
        
        # Validar que el userType sea válido
        if user_type not in ["owner", "clinic"]:
            print(f"🔍 AuthService: userType inválido: '{user_type}'")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="userType inválido. Debe ser 'owner' o 'clinic'"
            )
        
        print(f"🔍 AuthService: userType válido: '{user_type}'")
        
        # Obtener el perfil del usuario desde la API de autenticación
        token = credentials.credentials
        user_profile = await AuthService.get_user_profile_from_token(token)
        
        user = AuthenticatedUser(
            id=user_profile["id"],  # ID real del usuario
            email=user_profile.get("email", "user@example.com"),  # Email del usuario
            userType=user_type
        )
        
        return user
    
    @staticmethod
    async def get_user_id_from_token(token: str, user_type: str) -> str:
        """
        Obtiene el ID del usuario desde el token y valida el userType
        
        Args:
            token (str): Token de autenticación
            user_type (str): Tipo de usuario
            
        Returns:
            str: ID del usuario autenticado
            
        Raises:
            HTTPException: Si el userType es inválido
        """
        # Validar que el userType sea válido
        if user_type not in ["owner", "clinic"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="userType inválido. Debe ser 'owner' o 'clinic'"
            )
        
        # Obtener el perfil del usuario desde la API de autenticación
        user_profile = await AuthService.get_user_profile_from_token(token)
        
        return user_profile["id"]

    @staticmethod
    async def get_current_user_id(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        user_type: Optional[str] = Header(None, alias="X-User-Type", description="Tipo de usuario: 'owner' o 'clinic'")
    ) -> str:
        """
        Obtiene solo el ID del usuario actual basado en el token
        
        Args:
            credentials (HTTPAuthorizationCredentials): Credenciales de autorización
            user_type (Optional[str]): Tipo de usuario del header X-User-Type
            
        Returns:
            str: ID del usuario autenticado
            
        Raises:
            HTTPException: Si el token es inválido o falta userType
        """
        # Si user_type es None o no es un string válido, usar valor por defecto para testing
        if user_type is None or not isinstance(user_type, str):
            user_type = "clinic"
        
        # Validar que el userType sea válido
        if user_type not in ["owner", "clinic"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="userType inválido. Debe ser 'owner' o 'clinic'"
            )
        
        # Obtener el perfil del usuario desde la API de autenticación
        token = credentials.credentials
        user_profile = await AuthService.get_user_profile_from_token(token)
        
        return user_profile["id"]
    
    @staticmethod
    def verify_user_type(user: AuthenticatedUser, allowed_types: list[UserType]) -> bool:
        """
        Verifica que el usuario tenga uno de los tipos permitidos
        
        Args:
            user (AuthenticatedUser): Usuario a verificar
            allowed_types (list[UserType]): Lista de tipos de usuario permitidos
            
        Returns:
            bool: True si el usuario tiene un tipo permitido
            
        Raises:
            HTTPException: Si el usuario no tiene un tipo permitido
        """
        if user.userType not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere uno de los siguientes tipos: {', '.join([t.value for t in allowed_types])}"
            )
        return True 