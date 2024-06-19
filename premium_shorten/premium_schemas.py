from pydantic import BaseModel

class CreateDomainSchema(BaseModel):
    user_name :str
    custom_domain :str


class CreateCodeSchema(BaseModel):
    user_name : str
    code: str
    original_url: str