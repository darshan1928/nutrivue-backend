from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config.config import get_settings
import ssl
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
settings = get_settings()

# DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
DATABASE_URL = settings.DATABASE_URL_ASYNC

print(DATABASE_URL,"this is db")
engine = create_async_engine(
    DATABASE_URL,
    connect_args={"ssl": ssl_context},  # correct way for asyncpg
    echo=True
    )
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with async_session() as session:
        yield session