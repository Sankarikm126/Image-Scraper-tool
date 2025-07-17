# app.py
from flask import Flask, render_template, request, jsonify
import os
from utils.image_scraper import scrape_images_from_site
from utils.csv_generator import generate_csv
from utils.dropbox_utils import upload_to_dropbox, create_dropbox_folder
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    parent_url = request.form['parent_url']
    session_id = str(uuid.uuid4())
    local_image_dir = f"temp/{session_id}/Images"
    local_csv_path = f"temp/{session_id}/metadata.csv"

    os.makedirs(local_image_dir, exist_ok=True)

    metadata = scrape_images_from_site(parent_url, local_image_dir)
    generate_csv(metadata, local_csv_path)

    dropbox_path = f"/ImageExtraction/{session_id}"
    create_dropbox_folder(dropbox_path)
    for entry in metadata:
        upload_to_dropbox(entry['local_path'], f"{dropbox_path}/Images/{entry['image_name']}")
    upload_to_dropbox(local_csv_path, f"{dropbox_path}/metadata.csv")

    return jsonify({
        "status": "success",
        "image_count": len(metadata),
        "csv_link": f"https://www.dropbox.com/home{dropbox_path}/metadata.csv",
        "images_link": f"https://www.dropbox.com/home{dropbox_path}/Images"
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
