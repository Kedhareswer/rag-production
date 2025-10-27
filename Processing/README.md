# Processing Module

This module handles document conversion using Docling.

## File: document_processor.py

### Purpose
Converts various document formats (PDF, DOCX, HTML, etc.) into Docling's unified document representation.

### Key Features
- Multi-format support (PDF, DOCX, XLSX, PPTX, Markdown, HTML, Images)
- Layout analysis (detects headings, paragraphs, tables)
- Table extraction with structure preservation
- Text extraction with coordinates
- Metadata preservation

### Class: DocumentProcessor

#### Initialization
```python
from Processing.document_processor import DocumentProcessor

processor = DocumentProcessor()
```

#### Methods

**process_document(file_path)**
```python
document = processor.process_document("document.pdf")
```
Process a single document file.

**process_documents(file_paths)**
```python
documents = processor.process_documents([
    "doc1.pdf",
    "doc2.docx",
    "doc3.html"
])
```
Process multiple documents in batch.

### Supported Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| PDF | .pdf | Portable Document Format |
| Word | .docx | Microsoft Word documents |
| Excel | .xlsx | Microsoft Excel spreadsheets |
| PowerPoint | .pptx | Microsoft PowerPoint |
| Markdown | .md | Markdown files |
| HTML | .html, .htm | Web pages |
| Images | .png, .jpg, .tiff | Image files |

### Pipeline Configuration

The processor is configured with:
```python
pipeline_options = PdfPipelineOptions()
pipeline_options.do_table_structure = True   # Extract tables
pipeline_options.do_ocr = False              # Disable OCR
pipeline_options.generate_page_images = False
pipeline_options.generate_picture_images = False
```

### Document Structure

Processed documents contain:
```python
document.texts          # Text elements
document.tables         # Table elements
document.pictures       # Image elements
document.body           # Document structure tree
document.groups         # Grouped elements (lists, etc.)
```

### Export Options

```python
# Export to different formats
markdown = document.export_to_markdown()
html = document.export_to_html()
text = document.export_to_text()
json_data = document.export_to_dict()
```

### Example Usage

**Basic Processing:**
```python
from Processing.document_processor import DocumentProcessor

processor = DocumentProcessor()

# Process single document
doc = processor.process_document("research_paper.pdf")

# Access document content
print(doc.export_to_markdown())
```

**Batch Processing:**
```python
from pathlib import Path

processor = DocumentProcessor()

# Get all PDFs in a directory
pdf_files = list(Path("./documents").glob("*.pdf"))

# Process all at once
documents = processor.process_documents(pdf_files)

print(f"Processed {len(documents)} documents")
```

**Extract Tables:**
```python
doc = processor.process_document("document.pdf")

for table in doc.tables:
    print(table.export_to_markdown())
```

### Performance

- **Processing Speed**: ~2-5 seconds per page
- **First Run**: Downloads models (~500MB, one-time)
- **Subsequent Runs**: Uses cached models (fast)

### Troubleshooting

**Issue: Slow processing**
- First run downloads models (normal)
- For faster processing, disable unused features

**Issue: Memory errors**
- Process documents one at a time for large files

**Issue: OCR errors**
- OCR is disabled by default to avoid errors
- Enable only if needed for scanned documents
