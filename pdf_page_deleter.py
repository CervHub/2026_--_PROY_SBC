import sys
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path


# Ruta del PDF de entrada (modifica esta variable)
input_pdf = "inputs/toquepala/operaciones_mina/toquepala.operaciones_mina.v03.eg007.pdf"

# Lista de páginas a conservar (comienza en 1)
pages_to_keep = [1, 7, 17, 21, 23, 27, 31, 35, 37]
# pages_to_keep = [1, 3, 5, 7, 23, 27, 35, 43]
# pages_to_keep = [1, 3, 7, 11, 15, 17, 23, 25, 27]
# pages_to_keep = [1, 3, 13, 15, 25, 29]
# pages_to_keep = [1, 3, 5, 7, 15, 19, 25, 27, 31]
# pages_to_keep = [5, 25, 39, 47]
# pages_to_keep = [7]

# pages_to_keep = [3, 5, 9, 11, 13, 15, 19, 25, 29, 33, 39, 41, 43, 45, 47]
# pages_to_keep = [9, 11, 13, 15, 19, 21, 25, 29, 31, 33, 37, 39, 41]
# pages_to_keep = [5, 9, 13, 19, 21]
# pages_to_keep = [5, 7, 9, 11, 19, 21, 27, 29, 31]
# pages_to_keep = [9, 11, 13, 17, 21, 23, 29, 33, 35, 37, 39]
# pages_to_keep = [1, 3, 9, 11, 13, 15, 17, 19, 21, 23, 27, 29, 31, 33, 35, 37, 41, 43, 45]
# pages_to_keep = [1, 3, 5, 9, 11, 13, 15, 17, 19, 21]


def delete_pdf_pages(input_pdf_path, output_pdf_path, pages_list, keep_mode=True):
    """
    Si keep_mode es True, conserva solo las páginas en pages_list.
    Si keep_mode es False, elimina las páginas en pages_list y conserva las demás.
    """
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    num_pages = len(reader.pages)
    all_indices = set(range(num_pages))
    indices = set(p - 1 for p in pages_list if 1 <= p <= num_pages)
    if keep_mode:
        final_indices = sorted(indices)
    else:
        final_indices = sorted(all_indices - indices)
    for i in final_indices:
        writer.add_page(reader.pages[i])
    with open(output_pdf_path, "wb") as f:
        writer.write(f)
    print(f"Archivo guardado en: {output_pdf_path}")

if __name__ == "__main__":
    # Cambia keep_mode a False para eliminar las páginas de la lista y conservar las demás
    input_name = Path(input_pdf).stem
    output_pdf = f"outputs/{input_name}.pdf"
    delete_pdf_pages(input_pdf, output_pdf, pages_to_keep)
