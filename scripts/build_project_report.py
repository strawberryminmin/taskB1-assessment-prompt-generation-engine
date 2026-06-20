"""Build the project report DOCX using a reference Word file as a style shell."""

from __future__ import annotations

import json
import shutil
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


REFERENCE_DOCX = Path(r"D:\Downloads\Whatsapp\Task8.docx")
OUTPUT_DOCX = Path("Prompt_Engineering_Assessment_Report.docx")
SAMPLES_PATH = Path("samples/generated_samples.json")

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def attrs(values: dict[str, str]) -> str:
    return " ".join(f'w:{key}="{escape(value)}"' for key, value in values.items())


def text_run(text: str, bold: bool = False, color: str | None = None) -> str:
    rpr = []
    if bold:
        rpr.append("<w:b/>")
    if color:
        rpr.append(f'<w:color w:val="{color}"/>')
    rpr_xml = f"<w:rPr>{''.join(rpr)}</w:rPr>" if rpr else ""
    return f"<w:r>{rpr_xml}<w:t>{escape(text)}</w:t></w:r>"


def paragraph(
    text: str = "",
    style: str | None = None,
    bold: bool = False,
    color: str | None = None,
    before: int | None = None,
    after: int | None = None,
    align: str | None = None,
) -> str:
    props = []
    if style:
        props.append(f'<w:pStyle w:val="{style}"/>')
    spacing = []
    if before is not None:
        spacing.append(f'w:before="{before}"')
    if after is not None:
        spacing.append(f'w:after="{after}"')
    if spacing:
        props.append(f"<w:spacing {' '.join(spacing)}/>")
    if align:
        props.append(f'<w:jc w:val="{align}"/>')
    ppr = f"<w:pPr>{''.join(props)}</w:pPr>" if props else ""
    run = text_run(text, bold=bold, color=color) if text else ""
    return f"<w:p>{ppr}{run}</w:p>"


def cell(text: str, width: int, header: bool = False) -> str:
    shading = '<w:shd w:fill="F2F4F7"/>' if header else ""
    v_align = '<w:vAlign w:val="center"/>'
    margin = (
        "<w:tcMar>"
        '<w:top w:w="80" w:type="dxa"/>'
        '<w:bottom w:w="80" w:type="dxa"/>'
        '<w:start w:w="120" w:type="dxa"/>'
        '<w:end w:w="120" w:type="dxa"/>'
        "</w:tcMar>"
    )
    tcpr = f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shading}{v_align}{margin}</w:tcPr>'
    return f"<w:tc>{tcpr}{paragraph(text, bold=header, after=80)}</w:tc>"


def table(headers: list[str], rows: list[list[str]], widths: list[int]) -> str:
    borders = "".join(
        f'<w:{side} w:val="single" w:sz="4" w:space="0" w:color="D9E2EC"/>'
        for side in ["top", "left", "bottom", "right", "insideH", "insideV"]
    )
    tblpr = (
        '<w:tblPr><w:tblW w:w="9360" w:type="dxa"/>'
        '<w:tblInd w:w="120" w:type="dxa"/>'
        '<w:tblLayout w:type="fixed"/>'
        f"<w:tblBorders>{borders}</w:tblBorders>"
        "</w:tblPr>"
    )
    grid = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{width}"/>' for width in widths) + "</w:tblGrid>"
    header_row = "<w:tr>" + "".join(cell(value, widths[index], header=True) for index, value in enumerate(headers)) + "</w:tr>"
    body_rows = []
    for row in rows:
        body_rows.append("<w:tr>" + "".join(cell(value, widths[index]) for index, value in enumerate(row)) + "</w:tr>")
    return f"<w:tbl>{tblpr}{grid}{header_row}{''.join(body_rows)}</w:tbl>"


def extract_section_properties(reference_docx: Path) -> str:
    with zipfile.ZipFile(reference_docx) as package:
        document_xml = package.read("word/document.xml").decode("utf-8")
    start = document_xml.rfind("<w:sectPr")
    end = document_xml.rfind("</w:sectPr>")
    if start == -1 or end == -1:
        return (
            "<w:sectPr>"
            '<w:pgSz w:w="12240" w:h="15840"/>'
            '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
            'w:header="708" w:footer="708" w:gutter="0"/>'
            "</w:sectPr>"
        )
    return document_xml[start : end + len("</w:sectPr>")]


def load_samples() -> list[dict[str, str]]:
    if not SAMPLES_PATH.exists():
        return []
    return json.loads(SAMPLES_PATH.read_text(encoding="utf-8"))


def build_body() -> str:
    samples = load_samples()
    python_easy = [sample for sample in samples if sample["domain"] == "Python" and sample["difficulty"] == "Easy"]

    parts = [
        paragraph("INTERN TASK REPORT", style="Title", bold=True, color="0B2545", after=80, align="center"),
        paragraph("Prompt Engineering for Assessment Question Generation", style="Subtitle", align="center", after=240),
        table(
            ["Field", "Details"],
            [
                ["Title", "Prompt Engineering for Assessment Question Generation"],
                ["Intern Name", "Jasmine Tripathy"],
                ["Date of Report", "19 June, 2026"],
                ["Supervisor", "Vasudha Tayade"],
                ["Project Type", "Python-based prompt strategy evaluation system"],
                ["Reference Format", "Task8.docx intern task report structure"],
            ],
            [2600, 6760],
        ),
        paragraph("Executive Summary", style="Heading1"),
        paragraph(
            "This report documents the completion of a Python project titled Prompt Engineering for Assessment Question Generation. "
            "The project evaluates how different prompt engineering strategies influence the quality of automatically generated assessment questions across multiple technical domains and difficulty levels.",
        ),
        paragraph(
            "The system implements three strategies: Basic Prompt, Structured Prompt, and Role-Based Prompt. "
            "It supports Python, Data Structures, Database Management Systems, and Machine Learning. "
            "For each selected domain, the generator produces Easy, Medium, and Hard questions, validates the generated output, prevents duplicate questions through a stored history, and creates a comparison report using relevance, clarity, difficulty control, and diversity as evaluation metrics.",
        ),
        paragraph("Task Overview", style="Heading1"),
        paragraph(
            "The task was to build a modular Python system that can accept input in the form of a domain and difficulty level, generate assessment questions through multiple prompt styles, validate outputs, store generated samples, and compare strategy performance. "
            "The expected deliverables included a prompt library, generated question samples, a comparison report, and documentation explaining strategy behavior and findings.",
        ),
        paragraph("Objective", style="Heading2"),
        paragraph(
            "The primary objective was to demonstrate how prompt design affects generated assessment questions. "
            "The project focuses on practical prompt evaluation rather than only static prompt examples. "
            "It shows how different prompt structures can produce questions that vary in relevance, clarity, difficulty alignment, and diversity.",
        ),
        paragraph("Scope", style="Heading2"),
        paragraph(
            "The scope covered modular implementation, prompt storage, domain and difficulty support, duplicate detection, output validation, comparison reporting, and sample generation. "
            "The implementation is intentionally lightweight and deterministic, making it easy to run locally without external API dependencies.",
        ),
        paragraph("Technologies Used", style="Heading1"),
        table(
            ["Technology", "Purpose"],
            [
                ["Python 3", "Core programming language for the generator, validator, CLI, and report logic."],
                ["JSON", "Input format and storage format for generated samples, reports, and question history."],
                ["Dataclasses", "Clean representation of prompt strategy metadata."],
                ["Pathlib", "File path handling for samples, reports, and generated artifacts."],
                ["HTML/CSS", "Simple front-end demonstration page for prompt strategy comparison."],
                ["VS Code", "Development environment used to edit and inspect project files."],
            ],
            [2300, 7060],
        ),
        paragraph("Implementation Details", style="Heading1"),
        paragraph("Project Structure", style="Heading2"),
        table(
            ["Module", "Responsibility"],
            [
                ["prompts/prompt_library.py", "Stores supported domains, difficulties, prompt strategy metadata, and prompt templates."],
                ["generator/question_generator.py", "Generates strategy-specific questions and maintains duplicate detection history."],
                ["validation/validator.py", "Rejects empty, off-topic, overly long, malformed, or difficulty-mismatched questions."],
                ["reports/comparison_report.py", "Builds strategy comparison results and writes JSON and Markdown reports."],
                ["samples/generated_samples.json", "Stores generated sample questions for review and submission."],
                ["main.py", "Command-line entry point that accepts JSON-style input and writes all outputs."],
                ["index.html and style.css", "Browser-based project overview and prompt strategy comparison interface."],
            ],
            [2900, 6460],
        ),
        paragraph("Prompt Strategies", style="Heading2"),
        table(
            ["Strategy", "Description", "Observed Strength"],
            [
                ["Basic", "Direct instruction with minimal constraints.", "Fast to write and useful for quick drafts."],
                ["Structured", "Explicit rules for domain, difficulty, quality, and output format.", "Best overall control and consistency."],
                ["Role-Based", "Persona prompt that frames the model as an expert instructor.", "Strong clarity and learner-friendly wording."],
            ],
            [1900, 4560, 2900],
        ),
        paragraph("Question Generation Workflow", style="Heading2"),
        table(
            ["Step", "Description"],
            [
                ["1. Input", "The user provides a domain and difficulty, for example: domain Python and difficulty Easy."],
                ["2. Prompt Rendering", "Each strategy renders a prompt using the selected domain and difficulty."],
                ["3. Candidate Selection", "The generator selects a candidate question from the strategy and domain question bank."],
                ["4. Duplicate Check", "The normalized question is compared against the stored history file."],
                ["5. Validation", "The validator checks domain relevance, length, non-empty content, punctuation, and difficulty signals."],
                ["6. Output", "Valid questions are saved to generated_samples.json and used for comparison reporting."],
            ],
            [1200, 8160],
        ),
        paragraph("Duplicate Detection and Validation", style="Heading2"),
        paragraph(
            "Duplicate prevention is handled by maintaining a question history in samples/question_history.json. "
            "Before accepting a question, the system normalizes the text by lowercasing and collapsing whitespace, then checks whether it already exists in history. "
            "If a duplicate is found, the generator attempts the next available candidate.",
        ),
        paragraph(
            "Output validation rejects empty questions, excessively long questions, unsupported domains or difficulties, questions without a question mark, questions missing domain-specific keywords, and questions that do not match the expected difficulty signal. "
            "These checks make the generation process more reliable and prevent unsuitable questions from entering the sample set.",
        ),
        paragraph("Testing and Validation", style="Heading1"),
        paragraph(
            "The project was tested through command-line execution and syntax checks. "
            "The main workflow was executed using the sample input domain Python and difficulty Easy. "
            "Additional generation checks were run for Data Structures, Database Management Systems, and Machine Learning to confirm that each supported domain can generate valid questions.",
        ),
        table(
            ["Test Area", "Result"],
            [
                ["CLI execution", "Passed. main.py generated samples and comparison report successfully."],
                ["JSON-style input", "Passed. The parser accepts the required JSON input shape and includes a fallback for shell quote handling."],
                ["Domain coverage", "Passed. All four supported domains generated valid questions."],
                ["Syntax validation", "Passed. Python files compiled successfully with compileall."],
                ["Frontend cleanup", "Passed. index.html was corrected for structure, encoding, strategy names, and script behavior."],
            ],
            [2800, 6560],
        ),
        paragraph("Generated Samples", style="Heading1"),
        table(
            ["Strategy", "Difficulty", "Question"],
            [[sample["strategy"], sample["difficulty"], sample["question"]] for sample in samples[:9]],
            [1800, 1600, 5960],
        ),
        paragraph("Comparison Results", style="Heading1"),
        table(
            ["Strategy", "Relevance", "Clarity", "Difficulty Control", "Diversity", "Average"],
            [
                ["Basic", "7", "7", "6", "6", "6.5"],
                ["Structured", "9", "9", "9", "8", "8.75"],
                ["Role-Based", "8", "9", "8", "9", "8.5"],
            ],
            [1800, 1400, 1400, 2100, 1400, 1260],
        ),
        paragraph(
            "Structured prompting performed best overall because it includes the strongest constraints for topic, format, and difficulty. "
            "Role-Based prompting ranked close behind because it improves natural wording and question diversity. "
            "Basic prompting remains useful for quick drafts, but it benefits most from the validation layer.",
        ),
        paragraph("Results and Outcome", style="Heading1"),
        paragraph(
            "All requested project components were implemented. The final project includes a prompt library, generator module, validation module, comparison report module, generated sample JSON, project documentation, and a corrected browser overview page. "
            "The system can be run from the command line and produces reproducible outputs without requiring paid model API access.",
        ),
        paragraph("Challenges and Solutions", style="Heading1"),
        table(
            ["Challenge", "Solution"],
            [
                ["Preventing duplicates", "Implemented normalized question history and regeneration from candidate lists."],
                ["Validating relevance", "Added domain keyword checks and difficulty signal checks in the validator."],
                ["Keeping modules clean", "Separated prompts, generation, validation, reports, and CLI entry point into independent files."],
                ["Handling PowerShell JSON quoting", "Added a tolerant parser fallback for common stripped-quote input."],
                ["Fixing frontend issues", "Rebuilt index.html with clean text, supported domains, working JavaScript, and matching CSS selectors."],
            ],
            [3100, 6260],
        ),
        paragraph("Conclusion", style="Heading1"),
        paragraph(
            "The Prompt Engineering for Assessment Question Generation project successfully demonstrates how prompt strategy affects generated educational questions. "
            "The implementation is modular, easy to run, and aligned with the required deliverables. "
            "Structured prompting is recommended as the default approach because it provides the best balance of relevance, clarity, and difficulty control, while Role-Based prompting is useful when natural instructor-style phrasing is important.",
        ),
        paragraph(
            "Future enhancements could include connecting the generator to an LLM API, adding automated semantic duplicate detection, supporting answer generation and rubrics, storing outputs in a database, and expanding the front-end into a full interactive dashboard.",
        ),
        paragraph("Learning Experience and Skills Gained", style="Heading1"),
        table(
            ["Skill Area", "Learning"],
            [
                ["Prompt engineering", "Understanding how direct, structured, and persona-based prompts influence output quality."],
                ["Python modular design", "Separating project concerns into prompt, generator, validator, and report modules."],
                ["Validation design", "Creating rule-based safeguards for domain relevance, length, difficulty, and duplicate detection."],
                ["Reporting", "Summarizing strategy performance with metrics and findings."],
                ["Frontend correction", "Fixing HTML structure, JavaScript behavior, encoding problems, and CSS selector mismatches."],
            ],
            [2500, 6860],
        ),
        paragraph("References", style="Heading1"),
        paragraph("Project files: README.md, prompts/prompt_library.py, generator/question_generator.py, validation/validator.py, reports/comparison_report.py, and samples/generated_samples.json."),
        paragraph("Reference document format: Task8.docx intern task report."),
    ]

    if python_easy:
        parts.insert(
            28,
            paragraph(
                f"Example requested output: Strategy {python_easy[-1]['strategy']}, domain Python, difficulty Easy, question: {python_easy[-1]['question']}"
            ),
        )

    return "".join(parts)


def build_document_xml(section_properties: str) -> str:
    namespaces = (
        'xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
        'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:w10="urn:schemas-microsoft-com:office:word" '
        f'xmlns:w="{W_NS}" '
        'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
        'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" '
        'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
        'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
        'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
        'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
        'mc:Ignorable="w14 w15 wp14"'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f"<w:document {namespaces}><w:body>{build_body()}{section_properties}</w:body></w:document>"
    )


def main() -> None:
    if not REFERENCE_DOCX.exists():
        raise FileNotFoundError(f"Reference document not found: {REFERENCE_DOCX}")

    shutil.copyfile(REFERENCE_DOCX, OUTPUT_DOCX)
    section_properties = extract_section_properties(REFERENCE_DOCX)
    document_xml = build_document_xml(section_properties)

    temp_docx = OUTPUT_DOCX.with_suffix(".tmp.docx")
    with zipfile.ZipFile(OUTPUT_DOCX, "r") as source, zipfile.ZipFile(temp_docx, "w", zipfile.ZIP_DEFLATED) as target:
        for item in source.infolist():
            if item.filename == "word/document.xml":
                target.writestr(item, document_xml.encode("utf-8"))
            else:
                target.writestr(item, source.read(item.filename))
    temp_docx.replace(OUTPUT_DOCX)
    print(OUTPUT_DOCX.resolve())


if __name__ == "__main__":
    main()
