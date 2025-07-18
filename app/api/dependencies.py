from fastapi import Depends, HTTPException, status, Header
from typing import Annotated, Optional
from app.services.auth_service import AuthService
from app.schemas.auth import AuthenticatedUser, UserType

async def get_current_user_owner(
    current_user: Annotated[AuthenticatedUser, Depends(AuthService.get_current_user)]
) -> AuthenticatedUser:
    """
    Dependencia para verificar que el usuario sea de tipo 'owner'
    """
    AuthService.verify_user_type(current_user, [UserType.OWNER])
    return current_user

async def get_current_user_clinic(
    current_user: Annotated[AuthenticatedUser, Depends(AuthService.get_current_user)]
) -> AuthenticatedUser:
    """
    Dependencia para verificar que el usuario sea de tipo 'clinic'
    """
    AuthService.verify_user_type(current_user, [UserType.CLINIC])
    return current_user

async def get_current_user_id_clinic(
    current_user_id: Annotated[str, Depends(AuthService.get_current_user_id)]
) -> str:
    """
    Dependencia para obtener el ID del usuario autenticado de tipo 'clinic'
    """
    # El AuthService.get_current_user_id ya maneja la validación del userType
    return current_user_id

async def get_current_user_id_owner(
    current_user_id: Annotated[str, Depends(AuthService.get_current_user_id)]
) -> str:
    """
    Dependencia para obtener el ID del usuario autenticado de tipo 'owner'
    """
    # El AuthService.get_current_user_id ya maneja la validación del userType
    return current_user_id 