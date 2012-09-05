import pyPdf

class Pdf :

    def __init__(self) :
        pass 

    def getPDFContent(self, path):
        content = ""
        # Load PDF into pyPDF
        pdf = pyPdf.PdfFileReader(file(path, "rb"))
        # Iterate pages
        for i in range(0, pdf.getNumPages()):
            # Extract text from page and add to content
            content += pdf.getPage(i).extractText() + "\n"
            # Collapse whitespace
            content = " ".join(content.replace(u"\xa0", " ").strip().split())
            return content

    def fix_text(self, file, lang_type) :
        process_text = self.getPDFContent(file).encode("ascii", "ignore")
        line = 50 
        return process_text, line

