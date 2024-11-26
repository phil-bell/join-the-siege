import multiprocessing as mp

from flask import Flask, jsonify, request

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

    file_class = classify_file(file.filename)
    return jsonify({"file_class": file_class}), 200

def validate(filename):
    if filename == "":
        return {"error": "No selected file"}

    if not allowed_file(filename):
        return {"error": "File type not allowed"}

@app.route("/bulk_classify_files", methods=["POST"])
def bulk_classify_files_route():
    files = request.files.getlist("file")

    if not files:
        return jsonify({"error": "No file part in the request"}), 400

    file_names = [file.filename for file in files]

    with mp.Pool(mp.cpu_count()) as pool:
        errors = pool.map(validate, file_names)
        if any(errors):
            return jsonify(errors), 400

    with mp.Pool(mp.cpu_count()) as pool:
        response_data = pool.map(classify_file, file_names)
        return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(debug=True)
