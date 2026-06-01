from pathlib import Path
import argparse
import traceback

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions


def build_converter(model_dir: Path, lang: list[str]) -> DocumentConverter:
    pipeline_options = PdfPipelineOptions()
    pipeline_options.artifacts_path = model_dir
    pipeline_options.do_ocr = True
    pipeline_options.ocr_options = EasyOcrOptions(
        lang=lang,
        force_full_page_ocr=True,
    )

    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options
            )
        }
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True, help="Folder containing PDF files")
    parser.add_argument("--output_dir", required=True, help="Folder to save markdown files")
    parser.add_argument("--lang", default="en", help="OCR language, e.g. en or de")
    args = parser.parse_args()

    input_dir = Path(args.input_dir).expanduser()
    output_dir = Path(args.output_dir).expanduser()
    model_dir = Path("~/.cache/docling/models").expanduser()

    output_dir.mkdir(parents=True, exist_ok=True)

    converter = build_converter(
        model_dir=model_dir,
        lang=[args.lang],
    )

    pdf_files = sorted(input_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in: {input_dir}")
        return

    for pdf_path in pdf_files:
        print(f"\nProcessing: {pdf_path.name}")

        try:
            result = converter.convert(pdf_path)
            markdown = result.document.export_to_markdown()

            output_file = output_dir / f"{pdf_path.stem}.md"
            output_file.write_text(markdown, encoding="utf-8")

            print(f"Saved: {output_file}")

        except Exception:
            print(f"Failed: {pdf_path.name}")
            traceback.print_exc()


if __name__ == "__main__":
    main()
