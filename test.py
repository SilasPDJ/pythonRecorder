from PyPDF2 import PdfFileMerger

# pdfs = ['file1.pdf', 'file2.pdf', 'file3.pdf', 'file4.pdf'][:2]
# pdfs = ['pt0.pdf', 'pt1.pdf', 'pt2.pdf', 'pt3.pdf']
pdfs = ['Requerimento.pdf', 'CNH.pdf', 'ArquivosJuntos.pdf']
merger = PdfFileMerger()


pdfs = [f'C:\\OESK_CONTABIL\\Natan\\Outra empresa Rodrigo\\ABERTURA DE EMPRESA EM SUZANO\\MEI\\inverti o cnae\\{pdf}' for pdf in pdfs]


for pdf in pdfs:
    merger.append(pdf)

merger.write("ArquivosJuntos-requerimento-cnh.pdf")
merger.close()