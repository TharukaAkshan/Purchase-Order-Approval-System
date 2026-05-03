import asyncpg
import json
import os
from dotenv import load_dotenv
load_dotenv()

from python.knowledgebase.vector import create_vector_embeddings

user = os.getenv("POSTGRE_USER")
password = os.getenv("POSTGRE_PASSWORD")
database = os.getenv("POSTGRE_DATABASE")
host = os.getenv("POSTGRE_HOST")
port = os.getenv("POSTGRE_PORT")

schema = os.getenv("SCHEMA")
table_name = os.getenv("TABLE_NAME")




async def get_async_connection():
    try:
        # ssl_context = ssl.create_default_context()

        conn = await asyncpg.create_pool(
            user=user,
            password=password,
            database=database,
            host=host,
            port=port,
            ssl="prefer",
            min_size=5,
            max_size=20
        )
        
        if conn is not None:
            print("Connected")
            return conn
    except Exception as ex:
        print(ex)
        
        
        
async def vector_save_to_db(content, embedding):
    try:
        conn = await get_async_connection()
        if conn:
            try:
                query = f"""
                    INSERT INTO {schema}.{table_name} (
                        content, embedding
                    )
                    VALUES ($1, $2::vector);
                """

                await conn.execute(
                    query,
                    json.dumps(content),
                    str(embedding)
                )

                print("Insert successful")
                return True

            finally:
                await conn.close()

    except Exception as ex:
        print(f"Inserting failed: {ex}")
        return False
    
    


async def vector_search(response):
    try:
        embedding = await create_vector_embeddings(json.dumps(response))
        conn = await get_async_connection()

        if embedding is None :
            return None

        select_query = f"""
                SELECT content, 1 - (embedding <=> $1) AS similarity
                FROM {schema}.{table_name}
                WHERE 1 - (embedding <=> $1) >= 0.95
                ORDER BY embedding <=> $1
            """

        if select_query:
            
            try:
                rows = await conn.fetch (select_query, embedding)
                if rows:
                    print("vector search successfull")
                    return [dict(row) for row in rows]
                else:
                    return None
                
            finally:
                await conn.close()

    except Exception as ex:
        print(f"vector search failed: {ex}")
        return None

    
    
async def save_results_to_db(extractions: dict, approval: dict):

    try:
        conn = await get_async_connection()
        if conn:
            approval_status = approval.get("approval_status")
            reason = approval.get("reason")

            query = """
                INSERT INTO po.approved_purchase_orders(
                    extractions, approval_status, reason
                )
                VALUES ($1::jsonb, $2, $3);
            """

            await conn.execute(
                query,
                json.dumps(extractions),
                approval_status,
                reason
            )

            print("All results saved in DB")
            return {"status": "success"}

    except Exception as e:
        print("Results saving failed:", e)
