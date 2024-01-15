import os
from typing import List, Optional, Type

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from pydantic import BaseModel
from weasyprint import CSS, HTML

from .types import SourceTypes


class PDFGenerator:
    def __init__(
        self,
        html_content: str,
        source_types: SourceTypes,
        stylesheets: Optional[List[str]],
    ):
        self.html_content = html_content
        self.source_types = source_types
        self.stylesheets = stylesheets or []
        self._size: str = "A4"

    @classmethod
    def from_html(
        cls, html: str, stylesheets: Optional[List[str]] = []
    ) -> "PDFGenerator":
        if os.path.isfile(html):
            with open(html, "r") as f:
                html_string = f.read()
            return cls(html_string, SourceTypes.HTML, stylesheets)

        return cls(html, SourceTypes.HTML, stylesheets)

    @classmethod
    def from_jinja(
        cls,
        template_source: str,
        data: dict | Type[BaseModel],
        stylesheets: Optional[List[str]] = [],
        env_config: Environment | None = None,
        template_name: str | None = None,
    ) -> "PDFGenerator":
        if isinstance(data, BaseModel):
            data = data.model_dump()
        # Check if template_source is a directory or a file
        if os.path.isdir(template_source):
            env = env_config or Environment(
                loader=FileSystemLoader(template_source),
                autoescape=select_autoescape(["html", "xml"]),
            )
            if template_name:
                template = env.get_template(template_name)
                html_content = template.render(data)
            else:
                templates = env.list_templates()
                html_content = ""
                for t in templates:
                    template = env.get_template(t)
                    html_content += template.render(data)
        elif os.path.isfile(template_source):
            with open(template_source, "r") as file:
                template = Template(file.read())
                html_content = template.render(data)
        else:
            raise FileNotFoundError(
                "Template source must be either a directory or a file"
            )

        return cls(html_content, SourceTypes.JINJA, stylesheets)

    def _create_pdf(self, output_file: str | None = None) -> bytes | None:
        html_pdf = HTML(string=self.html_content, base_url="/")
        base_css = f"""
        @page {{
            size: {self._size};
            margin: 0;
        }}
        """
        css = [CSS(string=base_css)]
        for stylesheet in self.stylesheets:
            if os.path.isfile(stylesheet):
                css.append(CSS(filename=stylesheet))
            else:
                css.append(CSS(string=stylesheet))
        if output_file is None:
            return html_pdf.write_pdf(stylesheets=css)
        else:
            html_pdf.write_pdf(target=output_file, stylesheets=css)
            return None

    def generate_pdf(self, output_file: str) -> None:
        self._create_pdf(output_file)

    def generate_pdf_bytes(self) -> bytes:
        pdf_bytes = self._create_pdf()
        if pdf_bytes is None:
            raise ValueError("Failed to generate PDF bytes.")
        return pdf_bytes
