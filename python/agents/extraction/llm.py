import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


async def gpt_model(sysPrompt, usrPrompt, base64_img_list):
    try:
        
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        
        chat_prompt = [
            {
                "role": "system",
                "content": f"{sysPrompt}"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{usrPrompt}"
                    },
                    *[
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}} 
                        for b64 in base64_img_list
                    ]
                ]
            }
        ]
        
        completion = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_prompt,
            max_tokens=800,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "po_extraction",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "po_metadata": {
                                "type": "object",
                                "properties": {
                                    "po_number": {"type": "string"},
                                    "order_date": {"type": "string"},
                                    "delivery_date": {"type": "string"},
                                    "reference_number": {"type": "string"}
                                }
                            },
                            "vendor": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "address": {"type": "string"},
                                    "contact": {
                                        "type": "object",
                                        "properties": {
                                            "phone": {"type": "string"},
                                            "email": {"type": "string"}
                                        }
                                    },
                                    "vendor_id": {"type": "string"}
                                }
                            },
                            "buyer": {
                                "type": "object",
                                "properties": {
                                    "company_name": {"type": "string"},
                                    "billing_address": {"type": "string"},
                                    "shipping_address": {"type": "string"},
                                    "contact_person": {"type": "string"},
                                    "contact": {
                                        "type": "object",
                                        "properties": {
                                            "phone": {"type": "string"},
                                            "email": {"type": "string"}
                                        }
                                    }
                                }
                            },
                            "items": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "line_number": {"type": "integer"},
                                        "product_code": {"type": "string"},
                                        "description": {"type": "string"},
                                        "quantity": {"type": "number"},
                                        "unit_price": {"type": "number"},
                                        "total_price": {"type": "number"}
                                    }
                                }
                            },
                            "pricing": {
                                "type": "object",
                                "properties": {
                                    "subtotal": {"type": "number"},
                                    "tax": {"type": "number"},
                                    "discount": {"type": "number"},
                                    "shipping_cost": {"type": "number"},
                                    "grand_total": {"type": "number"},
                                    "currency": {"type": "string"}
                                }
                            },
                            "shipping": {
                                "type": "object",
                                "properties": {
                                    "method": {"type": "string"},
                                    "delivery_instructions": {"type": "string"},
                                    "delivery_address": {"type": "string"}
                                }
                            },
                            "payment": {
                                "type": "object",
                                "properties": {
                                    "payment_terms": {"type": "string"},
                                    "payment_method": {"type": "string"},
                                    "due_date": {"type": "string"}
                                }
                            },
                            "additional_info": {
                                "type": "object",
                                "properties": {
                                    "notes": {"type": "string"},
                                    "terms_and_conditions": {"type": "string"},
                                    "authorized_signature": {"type": "boolean"}
                                }
                            },
                            "text": {"type": "string"}
                        }
                    }
                }
            }
            # stop=None
        )

        response = completion.choices[0].message.content
        if response:
            return json.loads(response)
        else:
            return None
    
    except Exception as ex:
        print(ex)
