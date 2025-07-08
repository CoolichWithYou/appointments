from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from psycopg_pool import AsyncConnectionPool
from server.settings import Settings

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.async_pool = AsyncConnectionPool(conninfo=settings.get_db_connection())
    yield
    await app.async_pool.close()


app = FastAPI(lifespan=lifespan)


@app.post("/appointments")
async def get_appointments(request: Request):
    # async with request.app.async_pool.connection() as conn:
    #     async with conn.cursor() as cur:
    #         await cur.execute("""
    #
    #         """)
    #         results = await cur.fetchall()
    #         return results
    pass


@app.get("/appointments/{id}")
async def say_hello(request: Request):
    # async with request.app.async_pool.connection() as conn:
    #     async with conn.cursor() as cur:
    #         await cur.execute("""
    #
    #         """)
    #         results = await cur.fetchall()
    #         return results
    pass
