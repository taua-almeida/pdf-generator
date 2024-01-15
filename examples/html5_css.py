from pdf_generator import PDFGenerator

raw_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Sample Page</title>
</head>
<body>
    <div class="centered">
        <h1>Sample Table</h1>
        <table class="colorful">
            <tr>
                <th>Name</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Alice</td>
                <td>123</td>
            </tr>
            <tr>
                <td>Bob</td>
                <td>456</td>
            </tr>
            <tr>
                <td>Charlie</td>
                <td>789</td>
            </tr>
        </table>
    </div>
</body>
</html>
"""

css1 = """
    .centered {
        text-align: center;
    }
    .centered table {
        margin-left: auto;
        margin-right: auto;
    }
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
    th, td {
        padding: 5px;
        text-align: left;
    }
"""

css2 = """
    .colorful {
        background-color: red;
        color: white;
    }
"""

if __name__ == "__main__":
    pdf = PDFGenerator.from_html(raw_html, stylesheets=[css1, css2])
    pdf.generate_pdf("examples/html5_css.pdf")
