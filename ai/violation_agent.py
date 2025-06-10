from ai.gpt import gpt_call

def violation_agent(incident_details):
    prompt = f"""
    Analyze the following security incident and determine if it constitutes a legal violation under Geneva (Swiss) law:
    
    Incident Details:
    {incident_details}
    
    Provide your analysis with:
    1. A clear determination (Violation/No Violation)
    2. Relevant Swiss legal references
    3. Explanation of how the law applies to this case
    4. Potential legal consequences if applicable
    
    Focus specifically on:
    - Swiss Criminal Code
    - Geneva cantonal laws
    - Data protection laws (if applicable)
    - Employment laws (if applicable)
    """
    
    messages = [{"role": "user", "content": prompt}]
    response = gpt_call(messages, model="gpt-4", temperature=0.3)
    return response.choices[0].message.content