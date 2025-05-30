from flask import Flask, render_template, request
from transformers import pipeline
import re

app = Flask(__name__)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route("/", methods=["GET", "POST"])
def index():
    summary_points = []
    original_text = ""
    
    if request.method == "POST":
        original_text = request.form["paragraph"]
        if len(original_text.strip()) >= 20:
            try:
                summary = summarizer(original_text, max_length=60, min_length=30, do_sample=False)
                summary_text = summary[0]['summary_text']
                summary_points = re.split(r'(?<=[.!?])\s+', summary_text)
            except Exception as e:
                summary_points = [f"Error: {e}"]
        else:
            summary_points = ["Please enter a longer paragraph."]
    
    return render_template("index.html", summary=summary_points, original_text=original_text)

if __name__ == "__main__":
    app.run(debug=True)
