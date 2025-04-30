from pydantic import BaseModel, ConfigDict

class ModelBase(BaseModel):
    """Base schema with common configuration"""
    model_config = ConfigDict(
        from_attributes=True,  # Previously 'orm_mode'
        arbitrary_types_allowed=True,
        use_enum_values=True
    )