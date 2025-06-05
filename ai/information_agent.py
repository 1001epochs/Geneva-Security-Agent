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
# GPT Response: ChatCompletion(id='chatcmpl-Bf4KxAg0LcMj5lcJt2C7xfxo8IKrS', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_PdTawnvSLvrFe6kz4LYQGDib', function=Function(arguments='{"chat_response":"Thank you for reaching out. To help us assist you better, could you please provide more details about the incident? Specifically, we need the date, time, and location of the incident, the individuals involved, and a detailed description of what happened.","next_step":"info"}', name='info_agent'), type='function')], annotations=[]))], created=1749127819, model='gpt-4o-2024-08-06', object='chat.completion', service_tier='default', system_fingerprint='fp_a288987b44', usage=CompletionUsage(completion_tokens=68, prompt_tokens=401, total_tokens=469, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))
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