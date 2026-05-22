
import os
import requests
import time

# Configura la URL base y los parámetros de prueba
def test_extract_content():
    url = "http://127.0.0.1:1234/api/sbc/extract-content"
    # files = [
    #     ("reference_form", ("template.jpg", open("templates/toquepala/lesde/toquepala.lesde.v05.jpg", "rb"), "image/jpg")),
    #     ("bounding_boxes", ("template.json", open("templates/toquepala/lesde/toquepala.lesde.v05.json", "rb"), "application/json")),
    #     ("images", ("img1.png", open("inputs/toquepala/lesde/toquepala.lesde.v05.eg001.jpeg", "rb"), "image/png")),
    # ]
    # files = [
    #     ("reference_form", ("template.jpg", open("templates/toquepala/operaciones_mina/toquepala.operaciones_mina.v03.jpg", "rb"), "image/jpg")),
    #     ("bounding_boxes", ("template.json", open("templates/toquepala/operaciones_mina/toquepala.operaciones_mina.v03.json", "rb"), "application/json")),
    #     ("images", ("doc1.pdf", open("inputs/toquepala/operaciones_mina/toquepala.operaciones_mina.v03.eg001.pdf", "rb"), "application/pdf")),
    #     ("images", ("doc2.pdf", open("inputs/toquepala/operaciones_mina/toquepala.operaciones_mina.v03.eg002.pdf", "rb"), "application/pdf")),
    #     ("images", ("doc3.pdf", open("inputs/toquepala/operaciones_mina/toquepala.operaciones_mina.v03.eg003.pdf", "rb"), "application/pdf")),
    #     ("images", ("doc4.pdf", open("inputs/toquepala/operaciones_mina/toquepala.operaciones_mina.v03.eg004.pdf", "rb"), "application/pdf")),
    #     ("images", ("doc5.pdf", open("inputs/toquepala/operaciones_mina/toquepala.operaciones_mina.v03.eg005.pdf", "rb"), "application/pdf")),
    #     ("images", ("doc6.pdf", open("inputs/toquepala/operaciones_mina/toquepala.operaciones_mina.v03.eg006.pdf", "rb"), "application/pdf")),
    #     ("images", ("doc7.pdf", open("inputs/toquepala/operaciones_mina/toquepala.operaciones_mina.v03.eg007.pdf", "rb"), "application/pdf")),
    # ]
    # files = [
    #     ("reference_form", ("template.jpg", open("templates/toquepala/operaciones_mina_volquetes/toquepala.operaciones_mina_volquetes.v04.jpg", "rb"), "image/jpg")),
    #     ("bounding_boxes", ("template.json", open("templates/toquepala/operaciones_mina_volquetes/toquepala.operaciones_mina_volquetes.v04.json", "rb"), "application/json")),
    #     ("images", ("doc1.pdf", open("inputs/toquepala/operaciones_mina_volquetes/toquepala.operaciones_mina_volquetes.v04.eg001.pdf", "rb"), "application/pdf")),
    #     ("images", ("doc2.pdf", open("inputs/toquepala/operaciones_mina_volquetes/toquepala.operaciones_mina_volquetes.v04.eg002.pdf", "rb"), "application/pdf")),
    #     ("images", ("doc3.pdf", open("inputs/toquepala/operaciones_mina_volquetes/toquepala.operaciones_mina_volquetes.v04.eg003.pdf", "rb"), "application/pdf")),
    #     ("images", ("doc4.pdf", open("inputs/toquepala/operaciones_mina_volquetes/toquepala.operaciones_mina_volquetes.v04.eg004.pdf", "rb"), "application/pdf")),
    #     ("images", ("doc5.pdf", open("inputs/toquepala/operaciones_mina_volquetes/toquepala.operaciones_mina_volquetes.v04.eg005.pdf", "rb"), "application/pdf")),
    #     ("images", ("doc6.pdf", open("inputs/toquepala/operaciones_mina_volquetes/toquepala.operaciones_mina_volquetes.v04.eg006.pdf", "rb"), "application/pdf")),
    #     ("images", ("doc7.pdf", open("inputs/toquepala/operaciones_mina_volquetes/toquepala.operaciones_mina_volquetes.v04.eg007.pdf", "rb"), "application/pdf")),
    # ]
    files = [
        ("reference_form", ("template.jpg", open("templates/toquepala/operaciones_mina/toquepala.operaciones_mina.v03.jpg", "rb"), "image/jpg")),
        ("bounding_boxes", ("template.json", open("templates/toquepala/operaciones_mina/toquepala.operaciones_mina.v03.json", "rb"), "application/json")),
        ("images", ("doc7.pdf", open("inputs/toquepala/operaciones_mina/toquepala.operaciones_mina.v03.eg007.pdf", "rb"), "application/pdf")),
    ]

    start_time = time.time()
    response = requests.post(url, files=files)
    elapsed = time.time() - start_time
    print(f"Status code: {response.status_code}  |  Tiempo transcurrido: {elapsed:.2f} segundos")
    for i in range(2):
        os.system('afplay /System/Library/Sounds/Glass.aiff')
    
    # DEBUG: Guardar la respuesta en un archivo .json en la carpeta outputs
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "response.json")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.text)

if __name__ == "__main__":
    test_extract_content()