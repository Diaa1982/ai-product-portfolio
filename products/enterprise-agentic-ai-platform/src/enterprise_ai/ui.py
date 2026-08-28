from __future__ import annotations

import json

import gradio as gr

from .config import get_settings
from .schemas import UseCaseRequest
from .workflow_langgraph import EnterpriseLangGraphWorkflow


def run_analysis(
    title: str,
    challenge: str,
    objective: str,
    business_area: str,
    use_case_type: str,
    data_sources: str,
    outcomes: str,
    authorized: bool,
) -> str:
    request = UseCaseRequest(
        title=title,
        challenge=challenge,
        objective=objective,
        business_area=business_area,
        use_case_type=use_case_type,
        data_sources=[item.strip() for item in data_sources.split(",") if item.strip()],
        expected_outcomes=[item.strip() for item in outcomes.split(",") if item.strip()],
        authorized_to_execute=authorized,
    )
    result = EnterpriseLangGraphWorkflow(get_settings()).run(request)
    return json.dumps(result.to_dict(), indent=2, ensure_ascii=False, default=str)


def build_ui():
    with gr.Blocks(title="Enterprise Agentic AI") as demo:
        gr.Markdown(
            "# Enterprise Agentic AI Transformation Studio\n"
            "Governed RAG, multimodal analysis, specialist collaboration, value assessment, and controlled execution."
        )
        with gr.Row():
            with gr.Column():
                title = gr.Textbox(label="Use-case title")
                challenge = gr.Textbox(label="Enterprise challenge", lines=4)
                objective = gr.Textbox(label="Target outcome", lines=2)
                business_area = gr.Textbox(label="Business area", value="Enterprise Transformation")
                use_case_type = gr.Dropdown(
                    ["ai_transformation", "process_intelligence", "public_finance"],
                    value="ai_transformation",
                    label="Operating profile",
                )
                data_sources = gr.Textbox(label="Approved data sources (comma separated)")
                outcomes = gr.Textbox(label="Expected measurable outcomes (comma separated)")
                authorized = gr.Checkbox(label="Authorized to execute approved actions", value=False)
                run = gr.Button("Run governed workflow", variant="primary")
            output = gr.Code(label="Decision package", language="json")
        run.click(
            run_analysis,
            [title, challenge, objective, business_area, use_case_type, data_sources, outcomes, authorized],
            output,
        )
    return demo


if __name__ == "__main__":
    build_ui().launch(server_name="0.0.0.0", server_port=7860)
