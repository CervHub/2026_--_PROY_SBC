curl -X POST http://127.0.0.1:8000/web/api/v1/google-api/extract-multiple \
  -F "management_form_id=10" \
  -F "files[]=@inputs/toquepala/lesde/toquepala.lesde.v05.eg001.jpeg" \
  -H "Accept: application/json"