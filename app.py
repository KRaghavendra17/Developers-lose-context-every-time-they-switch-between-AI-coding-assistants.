from flask import Flask, render_template, request, jsonify
import os, re
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
UPLOADS = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOADS, exist_ok=True)

def read_notes(path, ext):
    if ext == "txt":
        with open(path, encoding="utf-8", errors="ignore") as f:
            return f.read()
    import fitz
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)

def build_cards(text):
    text = re.sub(r"\s+", " ", text).strip()
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 25]
    cards = [{"front": "What is an important point to remember?", "back": s[:500]} for s in sentences[:20]]
    if not cards and text:
        cards = [{"front": f"Key point {i+1}", "back": text[i:i+250]} for i in range(0, min(len(text), 2500), 250)]
    quiz = [{"question": f"Which statement matches key point {i+1} from your notes?",
             "options": [c["back"], "This is not stated in the notes.", "The opposite is always true.", "None of these."],
             "answer": c["back"], "explanation": "Check the matching passage in your original notes."}
            for i, c in enumerate(cards[:10])]
    return cards, quiz

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/generate", methods=["POST"])
def generate():
    if "notes" not in request.files or not request.files["notes"].filename:
        return jsonify(error="Choose a PDF or TXT file first."), 400
    f = request.files["notes"]
    filename = secure_filename(f.filename)
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ("pdf", "txt"):
        return jsonify(error="Only PDF and TXT files are supported."), 400
    path = os.path.join(UPLOADS, filename)
    f.save(path)
    try:
        text = read_notes(path, ext)
        if not text.strip():
            return jsonify(error="No readable text found. Scanned PDFs need OCR; try TXT."), 400
        cards, quiz = build_cards(text)
        return jsonify(title=os.path.splitext(filename)[0], cards=cards, quiz=quiz,
                       summary=" ".join(text.split()[:120]),
                       note="This MVP uses a basic offline generator. Connect an AI API for richer study material.")
    except ImportError:
        return jsonify(error="PDF support is missing. Run: pip install PyMuPDF"), 400
    except Exception as e:
        return jsonify(error="Could not read this file: " + str(e)), 400
    finally:
        try: os.remove(path)
        except OSError: pass

if __name__ == "__main__":
    app.run(debug=True)
