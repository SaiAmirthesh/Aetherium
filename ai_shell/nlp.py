from transformers import pipeline
from .config import MODEL_NAME, MAX_NEW_TOKENS

# Load transformer model at module level for efficiency
generator = pipeline("text-generation", model=MODEL_NAME)

def nlp_to_command(user_prompt):
    """
    Uses a local LLM to convert natural language user input to a Windows shell command.
    Returns the command as a string.
    """
    hf_prompt = (
        "You are a helpful assistant that converts user requests into safe Windows shell commands. "
        "Reply ONLY with the command. User request: " + user_prompt
    )
    result = generator(hf_prompt, max_new_tokens=MAX_NEW_TOKENS)
    # Extract the command from the result
    command = result[0]['generated_text'].split("User request:")[-1].strip()
    return command