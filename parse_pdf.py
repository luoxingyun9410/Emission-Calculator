import pdfplumber

pdf_path = "C:/Users/steven.luo/Downloads/national-greenhouse-account-factors-2023.pdf"
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        # Process the table data as necessary