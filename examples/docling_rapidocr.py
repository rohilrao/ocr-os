from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

MODEL_DIR = Path("~/.cache/docling/models").expanduser()
PDF_PATH = Path("sample.pdf")

pipeline_options = PdfPipelineOptions()
pipeline_options.artifacts_path = MODEL_DIR

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options
        )
    }
)

result = converter.convert(PDF_PATH)
print(result.document.export_to_markdown())
