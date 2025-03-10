from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class ContentHashtag(BaseModel):
    __tablename__ = "content_hashtags"

    content_id = Column(Integer, ForeignKey("review_contents.id"))
    hashtag_id = Column(Integer, ForeignKey("hashtags.id"))

    # Relationships
    content = relationship("ReviewContent", back_populates="hashtags")
    hashtag = relationship("Hashtag", back_populates="contents") 