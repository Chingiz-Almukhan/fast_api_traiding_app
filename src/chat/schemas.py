from pydantic import BaseModel, ConfigDict


class MessagesModel(BaseModel):
    id: int
    message: str

    model_config = ConfigDict(from_attributes=True)

