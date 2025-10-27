"""Document processing using Docling."""
import os
from pathlib import Path
from typing import List, Union
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions
from docling_core.types.doc import DoclingDocument

# Disable symlinks warning on Windows
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


class DocumentProcessor:
    """Process documents using Docling."""

    def __init__(self, artifacts_path: Path = None, enable_ocr: bool = True):
        """Initialize document processor.

        Args:
            artifacts_path: Path to store Docling models (optional, uses default if None)
            enable_ocr: Enable OCR for images and scanned documents
        """
        pipeline_options = PdfPipelineOptions()

        # Don't set custom artifacts_path - use Docling's default cache
        # This avoids model download issues

        # Configure pipeline - full feature support
        pipeline_options.do_table_structure = True  # Enable table extraction
        pipeline_options.do_ocr = enable_ocr  # Enable OCR for images
        pipeline_options.generate_page_images = True  # Enable page images
        pipeline_options.generate_picture_images = True  # Enable picture extraction
        
        # Enable all enrichments for better extraction
        pipeline_options.do_code_enrichment = False  # Disable to avoid errors
        pipeline_options.do_formula_enrichment = False  # Disable to avoid errors

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

    def process_document(self, file_path: Union[str, Path]) -> DoclingDocument:
        """Process a single document.

        Args:
            file_path: Path to document file

        Returns:
            DoclingDocument object
        """
        file_path = Path(file_path)
        print(f"\n{'='*70}")
        print(f"📄 Processing: {file_path.name}")
        print(f"   Format: {file_path.suffix}")
        print(f"   Size: {file_path.stat().st_size / 1024:.2f} KB")
        
        result = self.converter.convert(file_path)
        doc = result.document
        
        # Show extraction statistics
        print(f"\n📊 Extraction Results:")
        print(f"   ✓ Text elements: {len(doc.texts)}")
        print(f"   ✓ Tables: {len(doc.tables)}")
        print(f"   ✓ Pictures: {len(doc.pictures)}")
        print(f"   ✓ Pages: {len(doc.pages) if hasattr(doc, 'pages') else 'N/A'}")
        
        # Show sample text
        if doc.texts:
            sample_text = doc.texts[0].text[:200] if hasattr(doc.texts[0], 'text') else str(doc.texts[0])[:200]
            print(f"\n📝 Sample Text:")
            print(f"   {sample_text}...")
        
        print(f"{'='*70}\n")
        
        return doc

    def process_documents(
        self, file_paths: List[Union[str, Path]]
    ) -> List[DoclingDocument]:
        """Process multiple documents.

        Args:
            file_paths: List of document file paths

        Returns:
            List of DoclingDocument objects
        """
        documents = []
        for file_path in file_paths:
            doc = self.process_document(file_path)
            documents.append(doc)
        return documents
