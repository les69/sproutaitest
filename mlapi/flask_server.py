from flask import Flask, request, jsonify

app = Flask(__name__)

FOUL_WORDS = ["voldemort", "bad", "evil", "sauron"]


@app.route("/sentences/", methods=["POST"])
def validate_sentence():
    fragment = request.get_json()["fragment"]
    any_match = any(word in fragment for word in FOUL_WORDS)
    return jsonify({"hasFoulLanguage": any_match})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
