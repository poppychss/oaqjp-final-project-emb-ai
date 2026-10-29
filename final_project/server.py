
"""Flask server for the emotion detection application."""

from pathlib import Path

import requests
from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector

# Locate the parent directory containing templates/ and static/
BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)


@app.route("/")
def render_index_page():
    """Render the home page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze text and handle invalid input."""
    text_to_analyze = request.args.get("textToAnalyze")

    try:
        result = emotion_detector(text_to_analyze)

        if not result or result.get("dominant_emotion") is None:
            return "Invalid text! Please try again!"

        return jsonify(result), 200

    except requests.exceptions.RequestException:
        app.logger.exception("Emotion detection API request failed")
        return jsonify(
            {"error": "Emotion detection service unavailable."}
        ), 502
    except (KeyError, ValueError, TypeError):
        app.logger.exception("Invalid emotion detection response")
        return jsonify(
            {"error": "Unable to process emotion results."}
        ), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
