from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class ReviewImage(BaseModel):
    __tablename__ = "review_images"

    content_id = Column(Integer, ForeignKey("review_contents.id"))
    image_url = Column(String)
    order = Column(Integer)

    # Relationships
    content = relationship("ReviewContent", back_populates="images") 