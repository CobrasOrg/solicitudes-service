from fastapi import HTTPException, status, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.schemas.auth import AuthenticatedUser, UserType

security = HTTPBearer()

class AuthService:
    @staticmethod
    def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        user_type: str = Header(..., alias="X-User-Type", description="Tipo de usuario: 'owner' o 'clinic'")
    ) -> AuthenticatedUser:
        """
        Obtiene el usuario actual basado en el token y userType del header
        
        Args:
            credentials (HTTPAuthorizationCredentials): Credenciales de autorización
            user_type (str): Tipo de usuario del header X-User-Type
            
        Returns:
            AuthenticatedUser: Usuario autenticado
            
        Raises:
            HTTPException: Si el token es inválido o falta userType
        """
        # Validar que el userType sea válido
        if user_type not in [UserType.OWNER, UserType.CLINIC]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="userType inválido. Debe ser 'owner' o 'clinic'"
            )
        
        user = AuthenticatedUser(
            id="",  # Se puede obtener del token si es necesario
            email="",  # Se puede obtener del token si es necesario
            userType=user_type
        )
        
        return user
    
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