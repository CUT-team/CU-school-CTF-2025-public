from pydantic import BaseModel, ConfigDict

class ModelBase(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True, 
        arbitrary_types_allowed=True,
        use_enum_values=True
    )