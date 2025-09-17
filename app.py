import google.generativeai as genai
import os
from flask import Flask, render_template, request

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash-latest")


@app.route("/", methods=["GET", "POST"])
def home():
    response_text = None
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        if user_input:
            try:
                response = model.generate_content(user_input)
                response_text = response.text
            except Exception as e:
                print(f"An error occurred: {e}")
                response_text = "Sorry, an error occurred while generating the response."

    return render_template("index.html", response=response_text)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
