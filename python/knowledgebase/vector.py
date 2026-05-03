import json
from FlagEmbedding import FlagModel
import asyncio
import base64
# from python.agents.extraction.process import extration_agent_process
# from python.knowledgebase.db import vector_save_to_db

model = FlagModel('BAAI/bge-large-en-v1.5', use_fp16=True)


# async def image_to_base64(image_path):
#     with open(image_path, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#         return encoded_string.decode("utf-8")


# async def save_sample_duplicate_imgs(image_path):
    
#     with open(image_path, "rb") as f:
#         pdf_bytes = f.read()
#     if pdf_bytes:
#         response = await extration_agent_process(pdf_bytes)
#         if response:
#             print(response)
#             embedding = model.encode(json.dumps(response))
#             embedding = embedding.tolist()
#             if embedding is not None:
#                 await vector_save_to_db(response, embedding)
    

async def create_vector_embeddings(input: str):
    res = model.encode(input)
    return str(res.tolist())