from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class BaseSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(populate_by_name=True) 