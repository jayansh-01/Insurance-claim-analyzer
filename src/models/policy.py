from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base

class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary key=True, index=True)
    policy_number = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    max_coverage_amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)

    user = relationship("User", back_populates="policies")
    claims = relationship("Claim", back_populates="policy", cascade="all, delete-orphan")
