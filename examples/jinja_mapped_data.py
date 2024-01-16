from pdf_generator import PDFGenerator

if __name__ == "__main__":
    base_layout = {"title": "Sample PDF From Jinja"}
    data_content = {
        "content": "Jinja PDF Generated Content",
    }
    data_table = {
        "people": [
            {"name": "Alice", "value": 123},
            {"name": "Bob", "value": 456},
            {"name": "Charlie", "value": 789},
        ],
    }

    data_mapping = {
        "base_layout.html": base_layout,
        "content.html": data_content,
        "data_table.html": data_table,
    }

    pdf = PDFGenerator.from_jinja(
        "./examples/templates",
        data={},
        ignore_templates=["simple_page.html"],
        data_mapping=data_mapping,
    )
    pdf.generate_pdf("examples/jinja_pdf.pdf")
