# Proposal: Using Cursor as an Agent for Consistent, Accessible Website Generation in Schools

## Original Thought (User’s Concept)
The niche idea explored here is:
- Use **Cursor** (AI IDE coder) as the main environment for creating websites for schools.
- Websites must be structured with **consistency in reading level and accessibility**, ensuring suitability for children.
- Each website should have the ability to **export PDF versions** for printing when needed.
- Workflow:
  - Cursor acts as the builder for the website structure.
  - Sub-agents (outside Cursor or via API calls) handle **topic research, readability analysis, and accessibility adjustments**.
  - AI ensures that generated content matches the intended audience.
  - Cursor integrates these results into consistent, code-ready templates.

The ambition is to transform Cursor from a coding-only IDE into a **broader orchestration hub** for education-friendly websites, by extending it with rules and workflows tailored to schools.

---

## Required Code Base & Components

### 1. Python Integration with LLM APIs
- Use the **OpenAI Python library** (or similar) inside Cursor projects.
- Code Example (simplified):
```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "You are an assistant generating text for primary school students. Maintain grade 5 readability and accessibility."},
    {"role": "user", "content": "Write an article on the Amazon Rainforest for Year 5 students."}
  ],
  temperature=0.7
)

text = response.choices[0].message.content
```
- Output (`text`) is passed into website templates.

### 2. Readability & Accessibility Validation
- Integrate readability checks (e.g. **Flesch-Kincaid**, or Python libraries like `textstat`).
- Use accessibility testing libraries (e.g. **axe-core** via Puppeteer/Playwright in Node, or Python equivalents) to validate HTML output.
- Workflow: AI generates → validation scripts check → flagged issues returned to developer.

### 3. Website Generation
- Cursor writes structured websites:
  - Consistent HTML/CSS templates.
  - Semantic HTML tags for accessibility.
  - Integration of alternative text for images, proper ARIA roles.
- Reusable template system ensures uniform structure across all sites.

### 4. PDF Export
- Use Python libraries such as **WeasyPrint** or **ReportLab** to convert HTML → PDF.
- Example:
```python
import weasyprint

weasyprint.HTML('index.html').write_pdf('lesson_output.pdf')
```
- Export step can be triggered as part of the build workflow inside Cursor.

### 5. Workflow & Rules in Cursor
- Define **rules inside Cursor’s workspace** (tasks.json or similar) to:
  - Trigger AI text generation with correct prompts.
  - Run validation checks.
  - Ensure code consistency across projects.
  - Automate export pipeline.
- Sub-agents handle content generation/research, Cursor handles **assembly and structure**.

---

## Cautionary Feedback & Identified Holes

1. **Cursor’s System Prompt Limitation**
   - Cursor is optimized for code, not educational content. Using it directly for readability-controlled text may be a mismatch.
   - **Solution:** Offload content generation to external Python scripts using LLM APIs, then feed results back into Cursor.

2. **Need for Middleware**
   - Cursor alone cannot orchestrate research, readability checks, and PDF exports seamlessly.
   - **Solution:** Introduce lightweight middleware scripts (Python/Node) for orchestration while keeping Cursor as the IDE hub.

3. **Validation Step Critical**
   - AI output may miss readability or accessibility requirements without explicit checks.
   - **Solution:** Add automated readability and accessibility validation in the pipeline before publishing.

4. **Over-Reliance on Sub-Agents**
   - If multiple agents (for research, writing, validating) are introduced, complexity rises quickly.
   - **Solution:** Start with a simple workflow (AI generation + readability check + Cursor templates) before scaling.

5. **Export Fidelity**
   - HTML → PDF conversion often introduces formatting issues.
   - **Solution:** Test multiple libraries (WeasyPrint, ReportLab, wkhtmltopdf) and define school-standard templates for exports.

---

## Conclusion
Cursor is a strong candidate for the **structural and coding side** of this vision. However, to fully realize the niche element—AI-driven, accessible, school-ready websites with PDF exports—Cursor should be paired with:
- External Python scripts for AI content generation and validation.
- Defined rules/workflows inside Cursor to maintain consistency.
- A middleware layer to ensure readability and accessibility gates are passed.

This hybrid approach balances Cursor’s strengths (code consistency, IDE workflows) with AI’s flexibility (content generation, adaptation), while guarding against potential pitfalls (system prompt mismatch, validation gaps, export issues).

