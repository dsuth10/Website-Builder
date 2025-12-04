from __future__ import annotations
from io import BytesIO
from xhtml2pdf import pisa


def html_to_pdf_bytes(html_body: str, title: str) -> bytes:
    # Wrap body in minimal HTML structure for conversion
    html = f"""
    <html>
      <head>
        <meta charset='utf-8' />
        <title>{title}</title>
        <style>
          @page {{ size: A4; margin: 1in; }}
          body {{ font-family: Arial, Helvetica, sans-serif; font-size: 12pt; }}
          h1, h2, h3 {{ color: #333; }}
        </style>
      </head>
      <body>
        {html_body}
      </body>
    </html>
    """
    out = BytesIO()
    try:
        pisa_status = pisa.CreatePDF(src=html, dest=out)
        if pisa_status.err:
            error_msg = f"PDF generation failed: {pisa_status.err}"
            raise RuntimeError(error_msg)
        return out.getvalue()
    except Exception as e:
        if isinstance(e, RuntimeError):
            raise
        raise RuntimeError(f"PDF generation error: {str(e)}") from e

