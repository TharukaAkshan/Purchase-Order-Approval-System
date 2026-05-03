from python.agents.extraction.llm import gpt_model
from python.preprocess import pdf_to_base64_images

system_prompt = """
    You are an expert document parsing AI specialized in extracting structured data from Purchase Order (PO) documents.

    Your task is to extract all relevant information from the provided PDF and return ONLY a valid JSON object that strictly follows the given schema.

    Rules:
    1. Do NOT return any explanation, only JSON.
    2. If a field is missing, return:
    - "" for strings
    - 0 for numbers
    - false for booleans
    3. Do NOT hallucinate values.
    4. Extract all line items accurately.
    5. Ensure numeric fields (prices, totals, quantities) are numbers, not strings.
    6. Preserve currency as found; default to "LKR" if unclear.
    7. Combine multi-line addresses into a single string.
    8. Extract raw visible text into "text".
    9. Maintain correct nesting and structure.

    Output must strictly follow the schema provided.
"""


user_prompt = """
    Extract structured Purchase Order data from the attached PDF.

    Return the result in the following JSON schema:

        {
        "po_metadata": {
            "po_number": "",
            "order_date": "",
            "delivery_date": "",
            "reference_number": ""
        },
        "vendor": {
            "name": "",
            "address": "",
            "contact": {
            "phone": "",
            "email": ""
            },
            "vendor_id": ""
        },
        "buyer": {
            "company_name": "",
            "billing_address": "",
            "shipping_address": "",
            "contact_person": "",
            "contact": {
            "phone": "",
            "email": ""
            }
        },
        "items": [
            {
            "line_number": 1,
            "product_code": "",
            "description": "",
            "quantity": 0,
            "unit_price": 0.0,
            "total_price": 0.0
            }
        ],
        "pricing": {
            "subtotal": 0.0,
            "tax": 0.0,
            "discount": 0.0,
            "shipping_cost": 0.0,
            "grand_total": 0.0,
            "currency": "LKR"
        },
        "shipping": {
            "method": "",
            "delivery_instructions": "",
            "delivery_address": ""
        },
        "payment": {
            "payment_terms": "",
            "payment_method": "",
            "due_date": ""
        },
        "additional_info": {
            "notes": "",
            "terms_and_conditions": "",
            "authorized_signature": false
        },
        "text": ""
        }

    Important:
    - Extract ALL items in the table.
    - Ensure totals are correct if clearly present.
    - Do not include any text outside JSON.

"""


async def extration_agent_process(pdf_bytes):
    
    base64_img_list = await pdf_to_base64_images(pdf_bytes)
    response = await gpt_model(system_prompt, user_prompt, base64_img_list)
    if response is not None:
        return response