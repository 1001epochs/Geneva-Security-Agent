from ai.gpt import gpt_call
import json

def info_agent(history):
    """
    An Ai agent that fetches information about the security report

    Args: 
    history: [Dict]

    returns:
    Dict
    chat_response: str
    next_step: str
        - "info" if more information is needed
        - "report" if enough information is provided to generate a report
    """
    
    # information to be collected
    # date
    # time
    # location
    # individuals involved and detailed description of what happened

    prompt = """
    You are an AI agent that helps users report security incidents.
    You will be provided with a chat history and you will respond with a message that helps the user provide more information about the incident.
    If the user has provided enough information, you will respond with a message that indicates that the report is ready to be generated.
    If the user has not provided enough information, you will respond with a message that asks the user to provide more information, you need to be specific about what information is needed.
    The chat history will contain messages from the user and the AI agent.
    The information to be collected includes:
    - Date of the incident
    - Time of the incident
    - Location of the incident
    - Individuals involved in the incident
    - Detailed description of what happened
    You will return a dict containing the chat response and the next step.
    The next step will be excplicitly defined as either "info" or "report", and is to be used by the application only. "info" means that the agent needs to extract more information from the user, while "report" means that the agent has enough information to generate a report.
    """

    messages = [
        {"role": "system", "content": prompt}
    ] + history

    tools = [
        {
            "type": "function",
            "function": {
                "name": "info_agent",
                "description": "An AI agent that helps users report security incidents by extracting necessary information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "chat_response": {
                            "type": "string",
                            "description": "The response from the AI agent to the user."
                        },
                        "next_step": {
                            "type": "string",
                            "description": "The next step for the application, either 'info' or 'report'."
                        }
                    },
                    "required": ["chat_response", "next_step"]
                }
            }
        }
    ]

    response = gpt_call(messages, tools, model="gpt-4o", temperature=0.7)
    # sample response 
    response = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    chat_response = response["chat_response"]
    next_step = response["next_step"]
    # Ensure next_step is either "info" or "report"
    if next_step not in ["info", "report"]:
        next_step = "info"

    response = {
        "chat_response": chat_response,
        "next_step": next_step
    }
    print(f"Response from info_agent: {response}")
    return response