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

    # Build prompt
    base = "You are a creative name generator."
    context = f"Tags: {', '.join(tags)}." if tags else ""
    user_input = f"Vibe: {vibe}." if vibe else ""
    prompt = f"""{base} {context} {user_input}

You are an AI specialized in suggesting names that match the user's intent. Your behavior should dynamically adapt to the type of name requested:

- If the user asks for **baby names**, suggest realistic, culturally relevant, and usable names. Avoid overly creative or fictional styles — focus on actual candidates parents might consider.

- If the user asks for a **gamertag**, analyze popular gamertag trends and suggest original, catchy tags based on the user's input or vibe. You may include creative spelling or mashups if appropriate, but keep them usable.

- If no specific type is requested, generate diverse and fitting names using the provided tags and vibe. If no input is given at all, provide a variety of random names from different cultures and categories.

Always ensure your suggestions match the user's tone and purpose. Avoid reusing the same names repeatedly. Deliver names that feel intentional, not random.
"""

    print("Prompt used:", prompt)

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo" to save tokens
            messages=[
                {"role": "system", "content": base},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=30
        )
        result = response.choices[0].message.content.strip()
        print("AI responded with:", result)
    except Exception as e:
        result = f"(Error: {str(e)})"

    return jsonify({"name": result})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
