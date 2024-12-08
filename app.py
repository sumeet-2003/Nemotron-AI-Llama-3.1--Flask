from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

# Configure OpenAI/NVIDIA API
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/generate', methods=['POST'])
def generate_response():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        # Call the model API
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=False
        )
        # Extract response content
        response = completion.choices[0].message.content

        # Format the response
        formatted_response = format_response(response)
        return jsonify({"response": formatted_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def format_response(text):
    """Formats the response into readable subpoints."""
    # Split the text into sentences or meaningful parts
    sentences = text.split(". ")
    formatted = "<ul>"
    for sentence in sentences:
        formatted += f"<li>{sentence.strip()}.</li>"
    formatted += "</ul>"
    return formatted


if __name__ == '__main__':
    app.run(debug=True)
