from __future__ import annotations

import os

from .agents import RecommendationCrew
from .models import Dietary, PriceBand, UserPreferences
from .retrieval import MultimodalRetriever
from .store import KnowledgeBase


def build_app():
    try:
        import gradio as gr
    except ImportError as exc:
        raise RuntimeError("Install UI dependencies: pip install -e '.[ui]'") from exc

    data_path = os.getenv("RESTAURANT_AI_DATA", "data/restaurants.json")
    audit_path = os.getenv("RESTAURANT_AI_AUDIT", "audit/events.jsonl")

    def recommend(message, history, dietary, max_price, neighborhood, image):
        del history
        kb = KnowledgeBase(data_path, audit_path)
        prefs = UserPreferences(query=message, dietary=[Dietary(x) for x in dietary],
                                max_price_band=PriceBand(max_price) if max_price else None,
                                neighborhood=neighborhood or None)
        results, trace = RecommendationCrew(MultimodalRetriever(kb.load())).recommend(
            prefs, image_path=image, top_k=3)
        if not results:
            return "I found no restaurant satisfying every hard filter. Relax one constraint and try again."
        lines = []
        for i, item in enumerate(results, 1):
            evidence = "; ".join(e.excerpt for e in item.evidence)
            lines.append(f"### {i}. {item.restaurant_name} — {item.score:.0%}\n{item.rationale}\n\nEvidence: {evidence}\n\nTrade-off: {', '.join(item.tradeoffs)}")
        lines.append("<details><summary>Agent trace</summary>\n\n" + "\n\n".join(f"**{t.agent}:** {t.output}" for t in trace) + "\n</details>")
        return "\n\n".join(lines)

    with gr.Blocks(title="TableScout AI") as demo:
        gr.Markdown("# TableScout AI\nEvidence-grounded multimodal restaurant recommendations")
        with gr.Row():
            with gr.Column(scale=1):
                dietary = gr.CheckboxGroup([x.value for x in Dietary], label="Dietary requirements")
                max_price = gr.Dropdown([x.value for x in PriceBand], label="Maximum price band")
                neighborhood = gr.Textbox(label="Neighborhood")
                image = gr.Image(type="filepath", label="Optional food-image reference")
            with gr.Column(scale=3):
                gr.ChatInterface(
                    fn=recommend,
                    additional_inputs=[dietary, max_price, neighborhood, image],
                    examples=["Quiet romantic halal dinner", "Family pizza with good value",
                              "Vegan lunch near Business Bay"],
                )
    return demo


def main():
    build_app().launch()


if __name__ == "__main__":
    main()
