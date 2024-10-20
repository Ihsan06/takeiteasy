import openai

def generate_quote():
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Generate an inspirational quote",
        max_tokens=50
    )
    return response.choices[0].text.strip()
