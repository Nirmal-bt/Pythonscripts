
import tabula

# List of PDF files to convert
pdf_files = ["F:\\onam-scity\\SCC\\L&T South City & Radiant Clinics Camp\\ABHAY MALIK.pdf"]

for pdf_file in pdf_files:
    # Convert PDF to Excel
    tabula.convert_into(pdf_file, pdf_file.replace(".pdf", ".csv"), output_format="csv",pages="all")
