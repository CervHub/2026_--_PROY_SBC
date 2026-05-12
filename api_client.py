import os
import requests

# Configura la URL base y los parámetros de prueba
def test_extract_content():
    url = "http://127.0.0.1:1234/api/sbc/extract-content"
    # files = [
    #     ("reference_form", ("template.jpg", open("templates/ilo/abastecimientos/ilo.abastecimientos.v01.jpg", "rb"), "image/jpg")),
    #     ("bounding_boxes", ("template.json", open("templates/ilo/abastecimientos/ilo.abastecimientos.v01.json", "rb"), "application/json")),
    #     ("images", ("img1.png", open("inputs/ilo/abastecimientos/ilo.abastecimientos.v01.eg001.png", "rb"), "image/png")),
    #     ("images", ("img2.jpeg", open("inputs/ilo/abastecimientos/ilo.abastecimientos.v01.eg002.jpeg", "rb"), "image/jpeg")),
    #     ("images", ("img3.jpeg", open("inputs/ilo/abastecimientos/ilo.abastecimientos.v01.eg003.jpeg", "rb"), "image/jpeg")),
    #     ("images", ("img4.jpeg", open("inputs/ilo/abastecimientos/ilo.abastecimientos.v01.eg004.jpeg", "rb"), "image/jpeg")),
    # ]
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