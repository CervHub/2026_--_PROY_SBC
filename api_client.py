import requests

# Configura la URL base y los parámetros de prueba
def test_extract_content():
    url = "http://127.0.0.1:1234/api/sbc/extract-content/3/2/v02"
    files = [
        # Imagen de ejemplo
        # ("images", ("test1.jpeg", open("inputs/ilo/fundicion/ilo.fundicion.v05.eg001.jpeg", "rb"), "image/jpeg")),
        # PDF de ejemplo
        # ("images", ("test1.pdf", open("inputs/ilo/abastecimientos_almacenes_y_trafico/ilo.abastecimientos_almacenes_y_trafico.v01.eg001.pdf", "rb"), "application/pdf")),
        ("images", ("test1.pdf", open("inputs/ilo/ferrocarril_industrial/ilo.ferrocarril_industrial.v02.eg001.pdf", "rb"), "application/pdf")),
    ]
    response = requests.post(url, files=files)
    print("Status code:", response.status_code)
    # Guardar la respuesta en un archivo .json en la carpeta outputs
    import os
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "response.json")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.text)

if __name__ == "__main__":
    test_extract_content()
