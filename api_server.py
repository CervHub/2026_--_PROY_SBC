import os
import copy
import json
import cv2
import numpy as np
import threading
import lib.models.ilo_abastecimientos_almacenes_y_trafico_v01 as ilo_aayt_v01
import lib.models.ilo_ferrocarril_industrial_v02 as ilo_fi_v02
import lib.models.ilo_fundicion_v05 as ilo_f_v05
from lib.resolver import Resolver
from lib.debug import Debug
from lib.parallel_task_queue import ParallelTaskQueue
from lib.utils.corporation_handler import CorporationHandler
from lib.utils.management_handler import ManagementHandler
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Reuse align_and_crop and resolve from main.py
from main import align_and_crop, resolve

@app.route('/api/sbc/extract-content/<int:corporation_id>/<int:management_id>/<version>', methods=['POST'])
def extract_content(corporation_id, management_id, version):
    if 'images' not in request.files:
        return jsonify({'error': 'No images part in the request'}), 400
    images = request.files.getlist('images')
    if not images:
        return jsonify({'error': 'No images uploaded'}), 400

    input_dir = "inputs"
    corporation_dir = CorporationHandler.get_by_id(corporation_id)
    management_dir = ManagementHandler.get_by_corporation_and_id(corporation_dir, management_id)
    model = ManagementHandler.get_model_by_corporation_and_id(corporation_dir, management_id, version)

    target_dir = os.path.join(input_dir, corporation_dir, management_dir)
    target_base_path = f"{corporation_dir}.{management_dir}.{version}"
    target_template_path = os.path.join(target_dir, f"{target_base_path}.jpg")
    target_template_mapping_path = os.path.join(target_dir, f"data/{target_base_path}.json")

    # Load template data
    with open(target_template_mapping_path, "r") as f:
        raw_data = json.load(f)
    template_data = model.from_json(raw_data)

    # Save uploaded images to a temp folder
    temp_dir = os.path.join("outputs", "api_uploads")
    os.makedirs(temp_dir, exist_ok=True)
    input_paths = []
    for idx, img in enumerate(images):
        filename = secure_filename(img.filename)
        save_path = os.path.join(temp_dir, f"{idx}_{filename}")
        img.save(save_path)
        input_paths.append(save_path)

    # Step 1: Segment images
    data_list = [copy.deepcopy(template_data) for _ in input_paths]
    align_futures = []
    for input_path, data in zip(input_paths, data_list):
        output_dir = os.path.join(temp_dir, f"output_{os.path.basename(input_path)}")
        future = ParallelTaskQueue.submit(align_and_crop, input_path, target_template_path, data, output_dir)
        align_futures.append(future)
    for future in align_futures:
        future.result()

    # Step 2: Resolve regions
    resolve_threads = []
    for data in data_list:
        t = threading.Thread(target=resolve, args=(data,))
        t.start()
        resolve_threads.append(t)
    for t in resolve_threads:
        t.join()

    # Step 3: Collect results
    results = [data.to_json() for data in data_list]
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234, debug=True)
