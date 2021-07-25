from PyPDF2 import PdfFileMerger

pdfs = ['file1.pdf', 'file2.pdf', 'file3.pdf', 'file4.pdf'][:2]

merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("CreioEmTi_merged.pdf")
merger.close()