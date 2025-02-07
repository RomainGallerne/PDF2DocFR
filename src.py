################################################
#                   Auteur
################################################

__authors__ = "Romain Gallerne"
__created__ = "06-02-2025 (dd-mm-yyyy)"

################################################
#                   Imports
################################################

import asyncio
import os
import torch
import re

from googletrans import Translator
from docling.datamodel.base_models import InputFormat
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorDevice, AcceleratorOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

from docx import Document
from htmldocx import HtmlToDocx

################################################
#              Variables globales
################################################

pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.ocr_options.lang = ["en"]
pipeline_options.do_table_structure = True
pipeline_options.table_structure_options.do_cell_matching = True

if torch.cuda.is_available():
    pipeline_options.ocr_options.use_gpu = True
    accelerator_options = AcceleratorOptions(
        num_threads=2, device=AcceleratorDevice.GPU
    )  
else:
    accelerator_options = AcceleratorOptions(
        num_threads=2, device=AcceleratorDevice.CPU
    )    
    
pipeline_options.accelerator_options.device = accelerator_options

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options, backend=PyPdfiumDocumentBackend),
        InputFormat.DOCX: None
    }
)

translator = Translator()
parser = HtmlToDocx()
source = "./docs"

################################################
#                   Fonctions
################################################

def read_OCR(source : str) -> list:
    """
    Prepares document metadata and text chunks for database storage.

    PARAMETERS:
        source (str) : The path to the document to be processed.
        debug (bool) : A boolean indicating whether debug mode is enabled.
    """
    dl_doc = converter.convert(source).document
    text = dl_doc.export_to_html()
    return text
    
async def translate_text(text : str, target_language : str = "fr") -> str:
    """
    Translates a given text from english to the target language using the Google Translate API.
    PARAMETERS:
        text (str) : The text to be translated.
        target_language (str) : The target language for translation.
    """

    traduction = "" 
    for t in text.split("."):
        traduction += (await translator.translate(t+'.', src="en", dest=target_language)).text
    return traduction

def export_docx(title : str, text : str):
    """
    Export a given text to a docx file.
    PARAMETERS:
    	text (str) : The text to be exported to a docx file.
    """
    doc = Document()
    parser.add_html_to_document(text, doc)   
    doc.save(f"{title.replace(".docx","").replace(".pdf","").replace(".txt","")}_translated_FR.docx")

async def main():
    files = [source + "/" + f for f in os.listdir(source)]
    for file in files:
        print("READING doc :", file)
        text = read_OCR(file)
        if text != []:
            text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
            text = re.sub(r"<!-.*?->", "", text, flags=re.DOTALL)
            print("TRANSLATING doc :", file)
            traduction = await translate_text(text, target_language="fr")
            print("EXPORTING doc :", file)
            export_docx(file, traduction)
            print("Word docx created ✅!")
        else:
            print(f"No text found in {file}")

if __name__ == "__main__":
    asyncio.run(main())