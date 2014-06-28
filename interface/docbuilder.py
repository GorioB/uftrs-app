from docx import Document
from docx.shared import Inches

# for testing with pyinstaller
def createDummyDocument():
	document = Document()

	document.add_heading('Document Title', 0)

	p = document.add_paragraph('A plain paragraph having some ')
	p.add_run('bold').bold = True
	p.add_run(' and some ')
	p.add_run('italic.').italic = True

	document.add_heading('Heading, level 1', level=1)
	document.add_paragraph('Intense quote', style='IntenseQuote')

	document.add_paragraph(
	    'first item in unordered list', style='ListBullet'
	)
	document.add_paragraph(
	    'first item in ordered list', style='ListNumber'
	)

	# document.add_picture('monty-truth.png', width=Inches(1.25))

	table = document.add_table(rows=1, cols=0, style='LightShading-Accent1')
	column0 = table.add_column()
	column0.width = 5000000
	column1 = table.add_column()
	column2 = table.add_column()
	# print table.columns.cells
	table.columns.width = 200000

	hdr_cells = table.rows[0].cells
	hdr_cells[0].text = 'Qty'
	hdr_cells[1].text = 'Id'
	hdr_cells[2].text = 'Desc'

	tableData = [["5", "Apples", "yummy"], ["6", "Oranges", "they're orange"]]

	for row in tableData:
		row_cells = table.add_row().cells
		row_cells[0].text = row[0]
		row_cells[1].text = row[1]
		row_cells[2].text = row[2]


	document.add_page_break()

	document.save('demo.docx')

if __name__ == "__main__":
	createDummyDocument()