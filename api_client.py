import requests

# Configura la URL base y los parámetros de prueba
def test_extract_content():
    url = "http://127.0.0.1:1234/api/sbc/extract-content/2/3/v05"
    files = [
        ("images", ("test1.jpeg", open("inputs/ilo/fundicion/ilo.fundicion.v05.eg001.jpeg", "rb"), "image/jpeg")),
        # Puedes agregar más imágenes aquí si lo deseas
    ]
    response = requests.post(url, files=files)
    print("Status code:", response.status_code)
    print("Response:", response.text)

if __name__ == "__main__":
    test_extract_content()
