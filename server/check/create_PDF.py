from fpdf import FPDF

def create_pdf(name, code, data):
    pdf = FPDF(orientation="landscape", format="A4")
    pdf.add_page()
    pdf.set_font("Times", size=22)
    with pdf.table() as table:
        for data_row in [[f"{name}", f"F.Y. : 2021"]]:
            row = table.row()
            for datum in data_row:
                row.cell(str(datum))
    pdf.set_font("Times", size=16)
    with pdf.table() as table:
        for data_row in [["Tax", "Opening Stock", "Purchase", "Gross Profit", "Sale", "closing Stock"]]:
            row = table.row()
            for datum in data_row:
                row.cell(str(datum))
    with pdf.table() as table:
        for data_row in data:
            row = table.row()
            for datum in data_row:
                row.cell(str(datum))
    pdf.output("output.pdf")
    print("PDF created")

list = [
      [],
    ]


create_pdf("test", "1", list)
