import os
import re
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def get_text_pdf(pdf_file):
    """parse and get text from pdf file"""
    output_string = StringIO()
    with open(pdf_file, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    return output_string.getvalue()


def get_files(folder_name, file_type='.pdf'):
    """get list of files in directory with specified type (PDF by default)"""
    files = [f for f in os.listdir(folder_name) if
             (os.path.isfile(os.path.join(folder_name, f)) and file_type in f)]
    return files


def make_parse(folder_name, field_list):
    """make parse all PDF files with rules in fields list with patterns"""
    files_list = get_files(folder_name)
    fields_number = len(field_list)
    results = []
    # for each pdf file
    for file in files_list:
        file_forms = {'file': file, 'parts': []}
        pdf_file = os.path.join(folder_name, file)
        with open(pdf_file, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            # for each page
            for page in PDFPage.create_pages(doc):
                output_string = StringIO()
                device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                interpreter.process_page(page)
                text = output_string.getvalue()
                # make parse for all fields
                fields = {parse_field[0]: '' for parse_field in field_list}
                if text:
                    for parse_field in field_list:
                        field, pattern, group = parse_field
                        result = re.search(pattern, text)
                        # result put in file
                        if result:
                            fields[field] = result.group(int(group))
                        else:
                            fields[field] = ''
                file_forms['parts'].append(fields)
        results.append(file_forms)
    return results
