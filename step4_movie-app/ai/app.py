import os
from flask import Flask, jsonify, request
from transformers import pipeline

app = Flask(__name__)
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-0.5B-Instruct")
# Load once per container and keep model files in the mounted HF_HOME volume.
generator = pipeline(
    "text-generation",
    model=MODEL_NAME,
    tokenizer=MODEL_NAME,
)

@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}

@app.post("/recommend")
def recommend():
    payload = request.get_json(silent=True) or {}
    category = str(payload.get("category", "")).strip().lower()
    titles = payload.get("titles", [])
    if not category or not isinstance(titles, list):
        return jsonify({"error": "category and titles are required"}), 400
    if not titles:
        return jsonify({"category": category, "recommendation": "No hay películas disponibles en esta categoría."}), 200

    title_list = ", ".join(str(title) for title in titles[:10])
    messages = [
        {"role": "system", "content": "Eres un asistente que recomienda películas en español. Elige únicamente una película de la lista proporcionada. No inventes títulos. Explica brevemente por qué puede gustarle al usuario. Responde en una o dos frases."},
        {"role": "user", "content": f"Recomienda una película de categoría {category}. Títulos disponibles: {title_list}"},
    ]
    prompt = generator.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    result = generator(
        prompt,
        max_new_tokens=100,
        do_sample=False,
        repetition_penalty=1.15,
        no_repeat_ngram_size=3,
        return_full_text=False,
        pad_token_id=generator.tokenizer.eos_token_id,
    )
    recommendation = result[0]["generated_text"].strip()
    return jsonify({"category": category, "recommendation": recommendation, "model": MODEL_NAME})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
