from flask import Flask, request, jsonify

from src.classifier import classify_file
app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/classify_file', methods=['POST'])
def classify_file_route():

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": f"File type not allowed"}), 400

    file_class = classify_file(file)
    return jsonify({"file_class": file_class}), 200

@app.route("/bulk_classify_files", methods=["POST"])
def bulk_classify_files_route():
    files = request.files.getlist("file")

    if not files:
        return jsonify({"error": "No file part in the request"}), 400

    errors = []
    for file in files:
        file = request.files["file"]
        if file.filename == "":
            errors.append({"error": "No selected file"})

        if not allowed_file(file.filename):
            errors.append({"error": "File type not allowed"})

    if errors:
        return jsonify(errors), 400

    response_data = []
    for file in files:
        response_data.append(classify_file(file))

    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(debug=True)
