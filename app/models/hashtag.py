from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import BaseModel

class Hashtag(BaseModel):
    __tablename__ = "hashtags"

    tag_name = Column(String, unique=True, index=True)

    # Relationships
    contents = relationship("ContentHashtag", back_populates="hashtag") 