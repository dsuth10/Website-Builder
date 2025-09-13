A robust techstack for building consistent, accessible school websites with AI-generated content in Cursor should use recent and reliable Python libraries for each workflow stage and OpenRouter for LLM API calls.[^1][^2][^3][^4]

## Core Techstack

### Web Development and Structure

- **Django** (or Flask for simpler setups): Reliable, well-documented, and secure full-stack web development framework enabling rapid development, admin integration, and ORM support for scalable site management.[^2][^1]
- **Jinja2** (templating engine): Used with Flask or Django for flexible, maintainable HTML/CSS templates that enforce accessibility guidelines.


### Content Generation

- **OpenRouter API**: For calling LLMs like GPT-4o (or other OpenRouter models), using `openrouter` Python client or raw HTTP calls. Ensures modular AI content that matches specified readability and child-friendliness.


### Readability and Accessibility Validation

- **textstat**: Simplest, most robust readability analysis for Python, including Flesch-Kincaid, grade level, and other scores.
- **axe-core** (Node.js, called via Python subprocess or Playwright): Industry-standard accessibility auditing library for HTML output. Can be triggered as a CLI or within Python using Playwright bindings.
- **BeautifulSoup4**: Useful for HTML parsing, validation, and accessibility checks within Python workflows.


### PDF Export

- **WeasyPrint**: Best for modern HTML + CSS to PDF conversion, with strong support for CSS Grid, Flexbox, @page, and accessibility features.[^5][^3][^4]
- **PDFKit** or **xhtml2pdf**: Additional options for scenarios requiring more control (PDFKit uses wkhtmltopdf CLI, xhtml2pdf is pure Python).[^6][^7]
- **ReportLab**: Advanced solution for custom PDF layouts and graphics, suitable if standard conversion libraries can't match print fidelity.


### Middleware/Agents

- **FastAPI or Flask**: Lightweight Python API layers to orchestrate LLM requests, readability checking, PDF export calls, and communication between Cursor and sub-agents.
- **Playwright** (Python/Node): Used for headless browser accessibility audits and high-fidelity print preview.


## Workflow Automation

- **tasks.json** or **pyproject.toml**: Define rules and automation steps for Cursor to trigger sequential operations (AI writing, readability check, export).


## Recommended Library Versions (2025)

| Workflow | Library | Notes [Citations in table] |
| :-- | :-- | :-- |
| Web Framework | Django, Flask | Django (full-featured) [^1], Flask (lightweight) [^2] |
| Template Engine | Jinja2 | Standard with Flask/Django |
| LLM API | openrouter, requests | OpenRouter for flexible LLMs |
| Readability Stats | textstat | Flesch-Kincaid, CLI/Lib [^8] |
| Accessibility | axe-core, Playwright | For audit, Node.js bridge |
| HTML Parsing | BeautifulSoup4 | Python HTML manipulation |
| PDF Export | WeasyPrint, PDFKit, xhtml2pdf, ReportLab | Modern conversion \& custom layout [^5][^6][^3][^4] |
| Middleware | FastAPI, Flask | API orchestration/security [^1] |

## Integration Notes

- Cursor serves as IDE and orchestration hub; middleware Python APIs manage agent communication, validation, and export.
- Modular design allows adding custom validation, logging, and template enforcement for future scaling.

This stack leverages robust, well-supported Python libraries and OpenRouter LLMs, providing a flexible, future-proof foundation for AI-driven, accessible website generation for schools.