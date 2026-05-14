import os
import requests

# Configura la URL base y los parámetros de prueba
def test_extract_content():
    url = "http://127.0.0.1:1234/api/sbc/extract-content"
    # url = "http://50.19.240.57:1234/api/sbc/extract-content"
    files = [
        ("reference_form", ("template.jpg", open("templates/toquepala/lesde/toquepala.lesde.v05.jpg", "rb"), "image/jpg")),
        ("bounding_boxes", ("template.json", open("templates/toquepala/lesde/toquepala.lesde.v05.json", "rb"), "application/json")),
        ("images", ("img1.png", open("inputs/toquepala/lesde/toquepala.lesde.v05.eg001.jpeg", "rb"), "image/png")),
    ]
    response = requests.post(url, files=files)
    print("Status code:", response.status_code)
    
    # DEBUG: Guardar la respuesta en un archivo .json en la carpeta outputs
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "response.json")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.text)

if __name__ == "__main__":
    test_extract_content()