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
                      fetch: bool=False,
                      fetchrows: bool=False,
                      execute: bool=False,
                      fetchvall: bool=False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            if fetch:
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

    async def select_one_users(self, telegram_id):
        sql = """
            SELECT * FROM users WHERE telegram_id = $1
        """
        return await self.execute(sql, telegram_id, fetchrows=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def add_users(self, fullname:str, telegram_id: int):
        sql = ("INSERT INTO users (fullname, telegram_id) VALUES ($1, $2)")
        return await self.execute(sql, fullname, telegram_id, execute=True)

    async def create_table_xodimlar(self):
        sql = """
            CREATE TABLE IF NOT EXISTS xodimlar (
                id SERIAL PRIMARY KEY,
                ism_familiya VARCHAR(100) NOT NULL,
                lavozimi VARCHAR(100) NOT NULL,
                tel_nomer VARCHAR(13) NOT NULL
                )
        """
        return await self.execute(sql, execute=True)

    async def select_all_xodimlar(self, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        sql = """
            SELECT * FROM xodimlar
            LIMIT $1 OFFSET $2
        """
        return await self.execute(sql, page_size, offset, fetch=True)

    async def select_one_xodimlar(self, id):
        sql = "SELECT * from xodimlar WHERE id=$1"
        return await self.execute(sql, id, fetchrows=True)
    async def update_xodimlar(self, ism_familiya, lavozimi, tel_nomer, id):
        sql = "UPDATE xodimlar SET ism_familiya=$1, lavozimi=$2, tel_nomer=$3 where id = $4"
        await self.execute(sql, ism_familiya, lavozimi, tel_nomer, id, execute=True)
    async def add_xodimlar(self, ism_familiya:str, lavozimi: str, tel_nomer: str):
        sql = ("INSERT INTO xodimlar (ism_familiya, lavozimi, tel_nomer) VALUES ($1, $2, $3)")
        return await self.execute(sql, ism_familiya, lavozimi, tel_nomer, execute=True)
    async def delete_xodimlar(self, id):
        sql = "DELETE FROM xodimlar WHERE id=$1"
        return await self.execute(sql, id, execute=True)

    async def creat_tabe_sorovlar(self):
        sql = """
            CREATE TABLE IF NOT EXISTS sorovlar(
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT NOT NULL,
                sorov VARCHAR(255) NOT NULL,
                vaqti TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                )
        """
        return await self.execute(sql, execute=True)

    async def delete_time_sorovlar(self, vaqti):
        sql = "DELETE FROM sorovlar where vaqti<=$1"
        return await self.execute(sql, vaqti, execute=True)


    async def delete_time_sorovlar1(self, vaqti):
        sql = "DELETE FROM sorovlar where vaqti<URRENT_TIMESTAMP"
        return await self.execute(sql, vaqti, execute=True)

    async def add_sorov(self, telegram_id:int, sorov: str):
        sql = ("INSERT INTO sorovlar (telegram_id, sorov) VALUES ($1, $2)")
        return await self.execute(sql, telegram_id, sorov, execute=True)

    async def delete_sorovlar(self, id):
        sql = "DELETE FROM sorovlar WHERE id = $1"
        return await self.execute(sql, id, execute=True)

    async def select_all_sorovlar(self, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size  # Sahifadagi qatorni hisoblash
        sql = """
            SELECT * FROM sorovlar
            LIMIT $1 OFFSET $2
        """
        return await self.execute(sql, page_size, offset, fetch=True)


    async def create_table_dars_jadvali(self):
        sql = """
            CREATE TABLE IF NOT EXISTS dars_jadvali(
                id SERIAL PRIMARY KEY,
                guruh_nomi VARCHAR(30),
                filename TEXT  NOT NULL,
                filedata BYTEA NOT NULL,
                yuklangan_sana TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                )
        """
        return await self.execute(sql, execute=True)



    async def delete_dars_jadvali(self, id):
        sql = "DELETE FROM dars_jadvali WHERE id = $1"
        return await self.execute(sql, id, execute=True)

    async def update_dars_jadvali(self, filename, filedata, guruh_nomi, id):
        sql = "UPDATE dars_jadvali SET filename=$1, filedata=$2, guruh_nomi=$3, yuklangan_sana=CURRENT_TIMESTAMP WHERE id = $4"
        return await self.execute(sql, filename, filedata, guruh_nomi, id, execute=True)

    async def select_from_dars_jadvali(self):
        sql = "SELECT * FROM dars_jadvali"
        return await self.execute(sql, fetch=True)

    async def select_one_from_dars_jadvali(self, id):
        sql = "SELECT * FROM dars_jadvali WHERE id = $1"
        return await self.execute(sql, id, fetchrows=True)

    async def add_dars_jadvali(self, guruh_nomi, filename, filedata):
        sql = ("INSERT INTO dars_jadvali (guruh_nomi, filename, filedata) VALUES ($1, $2, $3)")
        return await self.execute(sql, guruh_nomi, filename, filedata, execute=True)

