from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai
import os

# Init Flask + load .env
app = Flask(__name__)
load_dotenv()

# Set up OpenAI client (new v1.x syntax)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-name", methods=["POST"])
def generate_name():
    data = request.json
    tags = data.get("tags", [])
    vibe = data.get("vibe", "")

    tag_descriptions = {
    "Baby Boy": "realistic and culturally appropriate names for baby boys",
    "Baby Girl": "realistic and culturally appropriate names for baby girls",
    "Startup": "modern, brandable, short and catchy names for businesses or products",
    "Pet": "cute and fun names for animals like dogs, cats, or exotic pets",
    "Fantasy/Game character": "mythical, fantasy, or game-style names with flair",
    "Gamertag": "original and catchy gamer usernames, sometimes with edgy or creative spelling",
    "Asian": "authentic or inspired names from Asian cultures",
    "Toy": "playful and marketable names suitable for toys or kids’ products",
    "Polish": "realistic Polish names respecting Polish culture and language",
    "French": "elegant or traditional names from French culture",
    "German": "strong or classic names from German-speaking regions",
    "European": "names that are common across Europe, or have European flair",
    "Nordic": "names inspired by Scandinavian mythology and culture",
    "American": "popular or classic names from the United States",
    "South America": "names reflecting South American language and culture",
    "North America": "names common in the US and Canada"
}


    # Build prompt
    base = "You are a name generator."
    tag_contexts = [tag_descriptions.get(tag, tag) for tag in tags]
    context = f"Tags: {', '.join(tag_contexts)}." if tag_contexts else ""

    user_input = f"Vibe: {vibe}." if vibe else ""
    prompt = f"""{base} {context} {user_input}

You are a highly specialized AI with one purpose: generating names that perfectly match the user's intent. Your suggestions are creative, relevant, and never random or repetitive. You understand tone, cultural context, current trends, and niche vibes.

Your output must follow these strict rules:
- Return **exactly 4 names**, one per line.
- **Do not** include numbers, dashes, dots, or special characters.
- **No explanations, intros, or formatting** — just the 4 names.
- **No repetition**, even across multiple generations with the same prompt.
- Every name must feel **fresh, intentional, and purpose-built**.

Behavior rules:
- For human names, give realistic, culturally appropriate, and usable first names. Avoid fictional or gimmicky styles. NO double names
- For **gamertags**, follow modern trends: originality, memorability, clean fusion of words, creative spelling if needed — but always readable and cool.
- If **no type is specified**, infer the tone from tags or vibe. If no context is given, return a diverse, balanced set of unique names.
- If tags or vibes are provided (e.g., “mystical,” “futuristic,” “Nordic,” “urban”), fully integrate their essence into the names — not just as inspiration, but as the **core identity** of each name.

You must internally track previously used names to avoid duplicates. Prioritize freshness and novelty while staying aligned with the user’s intent.

Output format:
<Name1>  
<Name2>  
<Name3>  
<Name4>
"""

    print("Prompt used:", prompt)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": base},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=50
        )

        raw_output = response.choices[0].message.content.strip()
        import re
        names = [re.sub(r'^[-•\d\s.]+', '', name).strip() for name in raw_output.split("\n") if name.strip()]


        print("AI responded with:", names)
        result = names

    except Exception as e:
        result = [f"Error: {str(e)}"]

    return jsonify({"names": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
