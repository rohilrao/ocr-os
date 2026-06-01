from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions

MODEL_DIR = Path("~/.cache/docling/models").expanduser()
PDF_PATH = Path("sample.pdf")

pipeline_options = PdfPipelineOptions()
pipeline_options.artifacts_path = MODEL_DIR
pipeline_options.do_ocr = True
pipeline_options.ocr_options = EasyOcrOptions(
    lang=["de"],                # or ["en"], ["de", "en"]
    force_full_page_ocr=True,
)

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options
        )
    }
)

result = converter.convert(PDF_PATH)
print(result.document.export_to_markdown())
