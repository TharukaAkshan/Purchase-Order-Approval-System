import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


async def gpt_model(sysPrompt, usrPrompt):
    try:
        
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        
        chat_prompt = [
            {
                "role": "system",
                "content": f"{sysPrompt}"
            },
            {
                "role": "user",
                "content": f"{usrPrompt}"
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
                    "name": "po_approval",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "approval_status": {
                                "type": "string",
                                "enum": ["pass", "fail"]
                            },
                            "reason": {
                                "type": "string"
                            }
                        },
                        "required": ["approval_status", "reason"],
                        "additionalProperties": False
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
