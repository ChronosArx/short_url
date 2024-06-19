from pydantic import BaseModel

class CreateDomainSchema(BaseModel):
    user_name :str
    custom_domain :str