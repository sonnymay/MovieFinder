import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def recommend_movies(user_input):
    prompt = f"Recommend 5 movies based on this description: {user_input}. \
For each movie, give the title and a short, simple summary in 1-2 sentences. Keep it easy to understand."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful movie recommendation assistant."},
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    mood = input("What kind of movie do you feel like watching? ")
    recommendations = recommend_movies(mood)
    print("\nHere are some movies you might enjoy:\n")
    print(recommendations)
