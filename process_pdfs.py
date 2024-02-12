import os
import PyPDF2
import pandas as pd
import pytesseract
from PIL import Image
import pyodbc


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
    return text


def perform_ocr(image_path):
    return pytesseract.image_to_string(Image.open(image_path))


def process_pdfs_and_save_to_csv(pdf_folder, csv_output_path):
    data = []

    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            text = extract_text_from_pdf(pdf_path)
            

            data.append({"File": pdf_file, "Text": text})

    df = pd.DataFrame(data)
    df.to_csv(csv_output_path, index=False)


def insert_into_access_database(csv_path, connection_string):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    df = pd.read_csv(csv_path)
    for index, row in df.iterrows():
        cursor.execute("INSERT INTO YourTable (FileName, Text) VALUES (?, ?)", row['File'], row['Text'])

    conn.commit()
    conn.close()

if __name__ == "__main__":

    pdf_folder = "/app/pdf_folder"
    csv_output_path = "/app/output.csv"

    process_pdfs_and_save_to_csv(pdf_folder, csv_output_path)

    access_db_connection_string = os.getenv("ACCESS_DB_CONNECTION_STRING")

    insert_into_access_database(csv_output_path, access_db_connection_string)
