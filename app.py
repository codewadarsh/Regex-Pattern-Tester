from flask import Flask, render_template, request, jsonify
import re
import json
import time

app = Flask(__name__)
DATA_FILE = "test_cases.json"


def explain_pattern(pattern):
    parts = {
        r"\d": "digit (0-9)",
        r"\w": "word character",
        r"\s": "whitespace",
        "^": "start of text",
        "$": "end of text",
        "+": "one or more",
        "*": "zero or more",
        "?": "zero or one",
        ".": "any character"
    }

    explanation = []

    for item in parts:
        if item in pattern:
            explanation.append(item + " = " + parts[item])

    return ", ".join(explanation) if explanation else "Basic regex pattern."


def test_pattern(pattern, text):
    try:
        matches = [m.group() for m in re.finditer(pattern, text)]
        return matches, None
    except re.error as error:
        return [], str(error)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/test", methods=["POST"])
def test():
    data = request.get_json()
    pattern = data.get("pattern", "")
    text = data.get("text", "")

    matches, error = test_pattern(pattern, text)

    return jsonify({
        "matches": matches,
        "count": len(matches),
        "explanation": explain_pattern(pattern),
        "error": error
    })


@app.route("/compare", methods=["POST"])
def compare():
    data = request.get_json()
    patterns = data.get("patterns", [])
    text = data.get("text", "")
    result = []

    for pattern in patterns:
        start = time.perf_counter()

        try:
            count = len(re.findall(pattern, text))
            error = None
        except re.error as e:
            count = 0
            error = str(e)

        elapsed = (time.perf_counter() - start) * 1000

        result.append({
            "pattern": pattern,
            "matches": count,
            "time_ms": round(elapsed, 4),
            "error": error
        })

    return jsonify(result)


@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()

    try:
        with open(DATA_FILE, "r") as file:
            cases = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        cases = []

    cases.append({
        "pattern": data.get("pattern", ""),
        "text": data.get("text", "")
    })

    with open(DATA_FILE, "w") as file:
        json.dump(cases, file, indent=2)

    return jsonify({"message": "Test case saved successfully."})


if __name__ == "__main__":
    app.run(debug=True)
