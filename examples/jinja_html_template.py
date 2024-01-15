from pdf_generator import PDFGenerator

if __name__ == "__main__":
    data = {
        "title": "Sample PDF From Jinja",
        "content": "Jinja PDF Generated Content",
        "people": [
            {"name": "Alice", "value": 123},
            {"name": "Bob", "value": 456},
            {"name": "Charlie", "value": 789},
        ],
    }

    pdf = PDFGenerator.from_jinja(
        "./examples/templates/simple_page.html",
        data=data,
    )
    pdf.generate_pdf("examples/jinja_pdf.pdf")
