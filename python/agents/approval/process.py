from python.agents.approval.llm import gpt_model
import json

async def approval_prompts(current_po_json, matched_result_json):
    
    system_prompt = """
        You are a Purchase Order Approval Agent.

        Your task is to evaluate whether a newly processed purchase order (PO) can be automatically approved or should be flagged for manual review.

        You will receive:

        1. Extracted data from the current purchase order (JSON format)
        2. A matched result from a vector similarity search (may contain similar past POs)

        Decision Rules:

        * Approve ("pass") ONLY if currant data and vector result are not matched.
        * Reject ("fail") if:
            -- The PO appears to be a duplicate or near-duplicate of an existing PO
            -- Both json results contains same data

        Output format MUST be strictly valid JSON:
        {
        "approval_status": "pass" or "fail",
        "reason": "clear and concise explanation"
        }

        Do NOT include any extra text outside the JSON.
    """


    user_prompt = f"""
        Evaluate the following purchase order for automatic approval.

        Current Purchase Order (Extracted Data):
        {current_po_json}

        Matched Similar Record (Vector Search Result):
        {matched_result_json}

        Instructions:

        - Compare the current PO with the matched result
        - Identify duplicates, anomalies, or inconsistencies
        - Decide whether it should be automatically approved or sent for manual review
        - how ever if there is no any Vector Search Result, always pass the PO
        """ + """
        Return ONLY valid JSON in this format:
        {
        "approval_status": "pass" or "fail",
        "reason": "brief explanation"
        }
    """
    
    return system_prompt, user_prompt



async def approval_agent_process(current_po_json, matched_result_json= None):
    
    if matched_result_json == None:
        matched_result_json = "No matched vector, PO can be passed"
    system_prompt, user_prompt = await approval_prompts(json.dumps(current_po_json), json.dumps(matched_result_json))
    response = await gpt_model(system_prompt, user_prompt)
    if response is not None:
        merged = {
                    **current_po_json,
                    **response
                }
        with open("test.json", "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=4, ensure_ascii=False)
        
        return merged