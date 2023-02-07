from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, DateTime

Base = declarative_base()


class ApplicationAccessLog(Base):
    __tablename__ = "access_log"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    ip_address = Column(String(255), nullable=False)
    user_agent = Column(String(255), nullable=False)
    method = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False)
    status_code = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class WikiAccessLog(Base):
    __tablename__ = "wiki_access_log"

    id = Column(Integer, primary_key=True)

    site_name = Column(String(50), nullable=False)
    path = Column(String(255), nullable=False)

    user_id = Column(Integer, nullable=False)
    user_unix_name = Column(String(255), nullable=False)

    ip_address = Column(String(255), nullable=True)
    user_agent = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class UserApplicationPassword(Base):
    __tablename__ = "user_application_password"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    password = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class UserApplicationKey(Base):
    __tablename__ = "user_application_key"

    id = Column(Integer, primary_key=True)
    key = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

# class Example(Base):
#     __tablename__ = "examples"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=True)
#     data = Column(JSON(), nullable=True)
#
#     created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
#
#
# class ExampleResponseSchema(Schema):
#     id = ma_fields.Integer()
#     name = ma_fields.String()
#     data = ma_fields.Dict()
#
#     created_at = ma_fields.DateTime()
#     updated_at = ma_fields.DateTime()
