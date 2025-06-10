import openai

# openai.api_key = "add key"

def gpt_tool_call(messages, tools, model="gpt-4o", temperature=0.7):
    """
    Calls the OpenAI GPT API with the provided messages and tools.

    Args:
        messages (list): List of messages to send to the model.
        tools (list): List of tools to be used by the model.
        model (str): The model to use for the API call.
        temperature (float): Sampling temperature for the model.

    Returns:
        The response from the model.
    """
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        tools=tools,
        tool_choice="required"
    )
    return response


def gpt_call(messages, model="gpt-4o", temperature=0.7):
    """
    Calls the OpenAI GPT API with the provided messages.

    Args:
        messages (list): List of messages to send to the model.
        model (str): The model to use for the API call.
        temperature (float): Sampling temperature for the model.

    Returns:
        The response from the model.
    """

    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response