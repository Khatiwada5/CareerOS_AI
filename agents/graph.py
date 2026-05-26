from __future__ import annotations

from typing import Any, TypedDict

try:
    from langgraph.graph import END, START, StateGraph
except Exception:  # Keeps the app usable if LangGraph is not installed yet.
    END = START = None
    StateGraph = None

from agents.cover_letter_agent import generate_cover_letter
from agents.fit_score_agent import score_fit
from agents.interview_agent import generate_interview_prep
from agents.job_agent import parse_job_description
from agents.resume_agent import analyze_resume
from agents.skill_gap_agent import create_skill_gap_plan
from agents.tailor_agent import tailor_resume


class CareerState(TypedDict, total=False):
    intent: str
    profile: dict
    resume_text: str
    file_name: str
    job_description: str
    company: str
    role: str
    job: dict
    output: Any
    final_response: Any


def route_intent(state: CareerState) -> str:
    intent = state.get("intent", "")
    if intent in {"resume_analysis", "job_fit", "resume_tailor", "cover_letter", "interview_prep", "skill_gap"}:
        return intent
    if state.get("file_name") and state.get("resume_text"):
        return "resume_analysis"
    if state.get("job_description"):
        return "job_fit"
    return "skill_gap"


def _resume_node(state: CareerState) -> CareerState:
    profile = state.get("profile", {})
    state["output"] = analyze_resume(int(profile.get("id", 1)), state.get("file_name", "resume.txt"), state.get("resume_text", ""))
    return state


def _job_parser_node(state: CareerState) -> CareerState:
    state["job"] = parse_job_description(state.get("job_description", ""), state.get("company", ""), state.get("role", ""))
    return state


def _fit_node(state: CareerState) -> CareerState:
    state["output"] = score_fit(state.get("profile", {}), state.get("resume_text", ""), state.get("job", {}))
    return state


def _tailor_node(state: CareerState) -> CareerState:
    state["output"] = tailor_resume(state.get("profile", {}), state.get("resume_text", ""), state.get("job_description", ""))
    return state


def _cover_letter_node(state: CareerState) -> CareerState:
    state["output"] = generate_cover_letter(state.get("profile", {}), state.get("company", ""), state.get("role", ""), state.get("job_description", ""))
    return state


def _interview_node(state: CareerState) -> CareerState:
    state["output"] = generate_interview_prep(state.get("profile", {}), state.get("role", ""), state.get("job_description", ""))
    return state


def _skill_gap_node(state: CareerState) -> CareerState:
    state["output"] = create_skill_gap_plan(state.get("profile", {}), state.get("job_description", ""))
    return state


def _formatter_node(state: CareerState) -> CareerState:
    state["final_response"] = state.get("output")
    return state


def build_graph():
    if StateGraph is None:
        return None
    graph = StateGraph(CareerState)
    graph.add_node("resume_analyzer", _resume_node)
    graph.add_node("job_parser", _job_parser_node)
    graph.add_node("fit_scorer", _fit_node)
    graph.add_node("resume_tailor", _tailor_node)
    graph.add_node("cover_letter", _cover_letter_node)
    graph.add_node("interview_coach", _interview_node)
    graph.add_node("skill_gap", _skill_gap_node)
    graph.add_node("final_formatter", _formatter_node)
    graph.add_conditional_edges(
        START,
        route_intent,
        {
            "resume_analysis": "resume_analyzer",
            "job_fit": "job_parser",
            "resume_tailor": "resume_tailor",
            "cover_letter": "cover_letter",
            "interview_prep": "interview_coach",
            "skill_gap": "skill_gap",
        },
    )
    graph.add_edge("job_parser", "fit_scorer")
    for node in ["resume_analyzer", "fit_scorer", "resume_tailor", "cover_letter", "interview_coach", "skill_gap"]:
        graph.add_edge(node, "final_formatter")
    graph.add_edge("final_formatter", END)
    return graph.compile()


def run_career_graph(state: CareerState) -> Any:
    graph = build_graph()
    if graph is None:
        intent = route_intent(state)
        if intent == "resume_analysis":
            return _formatter_node(_resume_node(state))["final_response"]
        if intent == "job_fit":
            return _formatter_node(_fit_node(_job_parser_node(state)))["final_response"]
        if intent == "resume_tailor":
            return _formatter_node(_tailor_node(state))["final_response"]
        if intent == "cover_letter":
            return _formatter_node(_cover_letter_node(state))["final_response"]
        if intent == "interview_prep":
            return _formatter_node(_interview_node(state))["final_response"]
        return _formatter_node(_skill_gap_node(state))["final_response"]
    result = graph.invoke(state)
    return result.get("final_response")
