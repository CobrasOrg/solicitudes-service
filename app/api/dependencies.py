from fastapi import Depends, HTTPException, status
from typing import Annotated
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