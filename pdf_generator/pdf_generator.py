import os
from typing import List, Optional, Type

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from pydantic import BaseModel
from weasyprint import CSS, HTML

from .config import PageConfig
from .types import SourceTypes


class PDFGenerator:
    def __init__(
        self,
        html_content: str,
        source_types: SourceTypes,
        stylesheets: Optional[List[str]],
        page_config: Type[PageConfig] | str,
    ):
        self.html_content = html_content
        self.source_types = source_types
        self.stylesheets = stylesheets or []
        self.page_config: str | Type[PageConfig] = page_config

    @classmethod
    def from_html(
        cls,
        html: str,
        stylesheets: Optional[List[str]] = [],
        page_config: Type[PageConfig] | str | None = None,
    ) -> "PDFGenerator":
        if page_config is None:
            page_config = PageConfig()
        if os.path.isfile(html):
            with open(html, "r") as f:
                html_string = f.read()
            return cls(html_string, SourceTypes.HTML, stylesheets)

        return cls(html, SourceTypes.HTML, stylesheets, page_config)

    @classmethod
    def from_jinja(
        cls,
        template_source: str,
        data: dict | Type[BaseModel],
        stylesheets: Optional[List[str]] = [],
        env_config: Environment | None = None,
        template_name: str | None = None,
        page_config: Type[PageConfig] | str | None = None,
        ignore_templates: list[str] | None = None,
        data_mapping: dict[str, dict | Type[BaseModel]] | None = None,
    ) -> "PDFGenerator":
        if isinstance(data, BaseModel):
            data = data.model_dump()

        # Initialize Jinja environment
        if os.path.isdir(template_source):
            env = env_config or Environment(
                loader=FileSystemLoader(template_source),
                autoescape=select_autoescape(["html", "xml"]),
            )
            html_content = ""
            templates = (
                env.list_templates() if template_name is None else [template_name]
            )
            for t in templates:
                if ignore_templates and t in ignore_templates:
                    continue
                template = env.get_template(t)
                # Check if specific data is provided for this template in data_mapping
                if data_mapping and t in data_mapping:
                    template_data = data_mapping[t]
                else:
                    template_data = data
                if isinstance(template_data, BaseModel):
                    template_data = template_data.model_dump()
                html_content += template.render(template_data)
        elif os.path.isfile(template_source):
            with open(template_source, "r") as file:
                template = Template(file.read())
                # Check if specific data is provided for this template in data_mapping
                if data_mapping and template_name in data_mapping:
                    template_data = data_mapping[template_name]
                else:
                    template_data = data
                if isinstance(template_data, BaseModel):
                    template_data = template_data.model_dump()
                html_content = template.render(template_data)
        else:
            raise FileNotFoundError(
                "Template source must be either a directory or a file"
            )

        if page_config is None:
            page_config = PageConfig()

        return cls(html_content, SourceTypes.JINJA, stylesheets, page_config)

    def _setup_page(self) -> str:
        if isinstance(self.page_config, PageConfig):
            return f"""
            @page {{
                size: {self.page_config.size};
                margin: {self.page_config.margin};
                orientation: {self.page_config.orientation};
            }}
            """
        else:
            return self.page_config

    def _create_pdf(self, output_file: str | None = None) -> bytes | None:
        html_pdf = HTML(string=self.html_content, base_url="/")
        base_css = self._setup_page()
        css = [CSS(string=base_css)]
        for stylesheet in self.stylesheets:
            if os.path.isfile(stylesheet):
                css.append(CSS(filename=stylesheet))
            elif os.path.isdir(stylesheet):
                for file in os.listdir(stylesheet):
                    if file.endswith(".css"):
                        full_path = os.path.join(stylesheet, file)
                        css.append(CSS(filename=full_path))
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
