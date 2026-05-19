import os
import requests
import base64
import json

# Archivos y campos igual que en api_client.py
def generate_lambda_event():
    files = [
        ("reference_form", ("template.jpg", open("templates/toquepala/lesde/toquepala.lesde.v05.jpg", "rb"), "image/jpg")),
        ("bounding_boxes", ("template.json", open("templates/toquepala/lesde/toquepala.lesde.v05.json", "rb"), "application/json")),
        ("images", ("img1.png", open("inputs/toquepala/lesde/toquepala.lesde.v05.eg001.jpeg", "rb"), "image/png")),
    ]

    # Prepara la petición (no la envía)
    req = requests.Request('POST', 'http://localhost', files=files).prepare()
    body_bytes = req.body
    content_type = req.headers['Content-Type']
    body_b64 = base64.b64encode(body_bytes).decode()

    # Extrae el boundary del Content-Type
    boundary = content_type.split("boundary=")[-1] if "boundary=" in content_type else ""

    event = {
        "resource": "/api/sbc/extract-content",
        "path": "/api/sbc/extract-content",
        "httpMethod": "POST",
        "headers": {
            "Content-Type": content_type
        },
        "multiValueHeaders": {
            "Content-Type": [content_type]
        },
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "pathParameters": None,
        "stageVariables": None,
        "requestContext": {
            "resourcePath": "/api/sbc/extract-content",
            "httpMethod": "POST",
            "path": "/api/sbc/extract-content"
        },
        "body": body_b64,
        "isBase64Encoded": True
    }

    # Guarda el JSON en outputs/lambda_event.json
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "lambda_event.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(event, f, ensure_ascii=False, indent=2)
    print(f"Evento Lambda guardado en {output_path}")

if __name__ == "__main__":
    generate_lambda_event()

# aws lambda invoke   --function-name arn:aws:lambda:us-east-1:101968849956:function:SBC-ContentExtractor   --payload fileb://outputs/lambda_event.json   outputs/lambda_response.json