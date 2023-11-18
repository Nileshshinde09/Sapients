import pandas as pd
from fpdf import FPDF
import pandas as pd
def convert_df_to_pdf(df=pd.read_csv('df.csv')):
    pdf_filename = "group_members_report.pdf"

    # Create a PDF document
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add DataFrame content to PDF
    col_widths = [max(pdf.get_string_width(str(x)), 40) for x in df.columns]  # Adjust column widths

    # Add headers
    pdf.set_font("Arial", "B", 12)
    for j, header in enumerate(df.columns):
        pdf.cell(col_widths[j], 10, header, border=1)

    # Add data
    pdf.ln()
    pdf.set_font("Arial", "", 12)
    for row in df.itertuples(index=False):
        for j, data in enumerate(row):
            pdf.cell(col_widths[j], 10, str(data), border=1)
        pdf.ln()

    # Save the PDF
    pdf.output(pdf_filename)

    return pdf_filename