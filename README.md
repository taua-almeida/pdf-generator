# PDFGenerator

PDFGenerator is a versatile Python package for generating PDF files from HTML and Jinja templates. It's designed to be simple yet powerful, providing a range of functionalities to create customized PDF documents.

## Features

- **From HTML to PDF:** Easily convert HTML content into PDF files.
- **Jinja Template Support:** Generate PDFs from Jinja templates with dynamic data.
- **Styling with CSS:** Apply CSS stylesheets for custom layout and design.
- **Flexible Configuration:** Customize page configurations like size, margin, and orientation.

## Installation

To install PDFGenerator, simply run:

```bash
pip install pdf-generator
```

## Usage

### Generating PDF from HTML

```py
from pdf_generator import PDFGenerator

simple_html = """
<!DOCTYPE html>
<html>
... [Your HTML content here] ...
</html>
"""

pdf = PDFGenerator.from_html(simple_html)
pdf.generate_pdf("output/html_to_pdf.pdf")
```

### Generating PDF from Jinja Template

```py
from pdf_generator import PDFGenerator

data = {
    "title": "Sample PDF",
    "content": "This is a sample PDF from Jinja template",
    ... [Other data] ...
}

pdf = PDFGenerator.from_jinja(
    "./path/to/templates",
    data=data,
    template_name="your_template.html",
)
pdf.generate_pdf("output/jinja_to_pdf.pdf")
```

_More examples at: [examples](https://github.com/taua-almeida/pdf-generator/tree/main/examples)_

## Advanced Usage

You can also use advanced features like custom page configuration, ignoring certain templates, and mapping different data to different templates. Refer to the class documentation and examples for more details.
