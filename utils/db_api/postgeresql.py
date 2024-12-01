import asyncpg
from typing import Union
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config
class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None
    async def create(self):
        self.pool = await asyncpg.create_pool(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASS,
            database=config.DB_NAME
        )
    async def execute(self, sql_command, *args,
                      fatch: bool=False,
                      fetchrows: bool=False,
                      execute: bool=False,
                      fetchvall: bool=False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            if fatch:
                result = await connection.fetch(sql_command, *args)
            elif fetchrows:
                result = await connection.fetchrow(sql_command, *args)
            elif fetchvall:
                result = await connection.fetchval(sql_command, *args)
            elif execute:
                result = await connection.execute(sql_command, *args)
            return result

    @staticmethod
    def format_kwargs(sql_command, parameters: dict):
        sql_command += " AND ".join([f"{key}='{value}'" for key, value in parameters.items()])
        return sql_command

    async def create_table_users(self):
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                fullname VARCHAR(255) NOT NULL,
                telegram_id BIGINT NOT NULL UNIQUE
                )
        """
        return await self.execute(sql, execute=True)