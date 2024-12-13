import os
import anthropic
def returnLLMResponse(review):
    os.environ["ANTHROPIC_API_KEY"] = "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"
    client = anthropic.Anthropic()
    prompt = """
        You are a review analyzer. Return only the JSON object without any additional notes or explanations. Your task is to:
        1. Extract and summarize details specifically about the **food quality** and **service quality** from the given review.
        2. Ensure no hallucinations occur: only use the information present in the review. Do not fabricate or add any data that is not explicitly mentioned.
        3. Ignore any personal information, unrelated content, or data not relevant to the categories of food and service.
        4. If the review does not mention either **service quality** or **food quality**, return an empty string for the respective category.
        5. Determine the sentiment (positive, negative, or neutral) of the overall text instead of assigning sentiments to food and service individually.
        6. Respond with a JSON object containing:
        - food_quality: string
        - service_quality: string
        - overall_sentiment: 'positive', 'negative', or 'neutral'
    """

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        system = prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{review}"
                    }
                ]
            }
        ]
    )    
    return message.content[0].text
