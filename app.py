from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai
import os

app = Flask(__name__)
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-name", methods=["POST"])
def generate_name():
    data = request.json
    tags = data.get("tags", [])
    vibe = data.get("vibe", "")
    count = data.get("count", 4)

    # Use GPT to get names
    base = "You are a creative name generator."
    tag_desc = ", ".join(tags)
    prompt = f"{base} Tags: {tag_desc}. Vibe: {vibe}. Return {count} unique names, one per line, no formatting."

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
        raw = response.choices[0].message.content.strip()
        names = [name.strip("-• 0123456789.").strip() for name in raw.split("\n") if name]
        return jsonify({"names": names})

    except Exception as e:
        return jsonify({"names": [f"Error: {str(e)}"]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
