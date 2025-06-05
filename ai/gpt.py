import openai

openai.api_key = "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"

def gpt_call(messages, tools, model="gpt-4o", temperature=0.7):
    """
    Calls the OpenAI GPT API with the provided messages.

    Args:
        messages (list): List of messages to send to the model.
        model (str): The model to use for the API call.
        temperature (float): Sampling temperature for the model.

    Returns:
        str: The response from the model.
    """
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        tools=tools,
        tool_choice="required"
    )
    return response