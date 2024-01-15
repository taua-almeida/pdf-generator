from pdf_generator import PDFGenerator

simple_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Sample Page</title>
    <style>
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
    </style>
</head>
<body>
    <div class="centered">
        <h1>Sample Table</h1>
        <table>
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


if __name__ == "__main__":
    pdf = PDFGenerator.from_html(simple_html)
    pdf.generate_pdf("examples/html5.pdf")
