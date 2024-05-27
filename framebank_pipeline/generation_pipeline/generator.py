from openai import OpenAI


openai_api_key = 'YOUR_API_KEY'

def query_model(prompt, model="gpt-4o", temperature=0.5, top_p=0.5, seed=42):
    client = OpenAI(
    api_key=openai_api_key,
)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        top_p=top_p,
        seed=seed
    )

    message_content = response.choices[0].message.content
    return message_content
