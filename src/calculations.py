from __future__ import annotations
from typing import Any
from .config import BONUS_CONFIG, FORM_SECTIONS, WEIGHTS


def score_status(score: float | int | None) -> tuple[str, str]:
    if score is None:
        return "Não avaliado", "#9FA0A3"
    try:
        val = float(score)
    except (TypeError, ValueError):
        return "Não avaliado", "#9FA0A3"
    if val <= 4:
        return "Crítico", "#9E3F45"
    if val <= 6:
        return "Atenção", "#B8875D"
    if val == 7:
        return "Regular", "#B7A86A"
    if val <= 9:
        return "Forte", "#6D6E71"
    return "Excelência Charth", "#C9A0A0"


def mean(values: list[float]) -> float:
    vals = [float(v) for v in values if v is not None]
    return round(sum(vals) / len(vals), 2) if vals else 0.0


def compute_section_scores(scores: dict[str, float]) -> dict[str, float]:
    result: dict[str, float] = {}
    for section in FORM_SECTIONS:
        vals = []
        for q in section["questions"]:
            if q["key"] in scores:
                vals.append(float(scores[q["key"]]))
        result[section["name"]] = mean(vals)
    return result


def compute_weighted_score(section_scores: dict[str, float]) -> float:
    total_weight = sum(WEIGHTS.values())
    total = 0.0
    for section, weight in WEIGHTS.items():
        total += float(section_scores.get(section, 0.0)) * weight
    return round(total / total_weight, 2) if total_weight else 0.0


def status_from_weighted(score: float) -> str:
    """Status operacional oficial da avaliação.

    Regra equivalente à fórmula da planilha:
    SE(MÉDIA GERAL>=9; "Excelência CHARTH";
      SE(MÉDIA GERAL>=8; "Loja Forte";
        SE(MÉDIA GERAL>=7; "Loja em Atenção";
          "Plano de Ação Imediato")))

    Observação: bonificação trimestral é calculada separadamente em compute_bonus().
    """
    if score >= 9.0:
        return "Excelência CHARTH"
    if score >= 8.0:
        return "Loja Forte"
    if score >= 7.0:
        return "Loja em Atenção"
    return "Plano de Ação Imediato"


def result_meta_reference(result_score: float) -> str:
    if result_score >= 10:
        return "105% ou mais da meta"
    if result_score >= 9:
        return "100% da meta"
    if result_score >= 8.5:
        return "mínimo de 95% da meta"
    if result_score >= 8.3:
        return "mínimo de 90% da meta"
    return "abaixo dos critérios mínimos de meta"


def manager_gold_value(weighted_score: float) -> float:
    if weighted_score >= 9.5:
        return 5000.0
    if weighted_score >= 9.0:
        return 4200.0
    if weighted_score >= 8.5:
        return 3500.0
    return 0.0


def compute_bonus(section_scores: dict[str, float], weighted_score: float, grave_issue: bool) -> dict[str, Any]:
    cfg = BONUS_CONFIG
    result_score = section_scores.get("Resultados e Indicadores", 0.0)
    management_score = section_scores.get("Gestão da Gerente", 0.0)
    weighted_blocks = [section_scores.get(section, 0.0) for section in WEIGHTS.keys()]
    min_block = min(weighted_blocks) if weighted_blocks else 0.0

    gold = cfg["gold"]
    qualifies_gold = (
        weighted_score >= gold["min_weighted_score"]
        and result_score >= gold["min_results"]
        and management_score >= gold["min_management"]
        and min_block >= gold["min_block"]
        and (not gold["requires_no_grave_disciplinary_issue"] or not grave_issue)
    )
    if qualifies_gold:
        return {
            "level": "Ouro",
            "manager_bonus": manager_gold_value(weighted_score),
            "team_fund_enabled": True,
            "reason": "Critérios Ouro atendidos: média, resultado, gestão, blocos mínimos e sem falta grave.",
        }

    silver = cfg["silver"]
    qualifies_silver = (
        weighted_score >= silver["min_weighted_score"]
        and result_score >= silver["min_results"]
        and management_score >= silver["min_management"]
        and min_block >= silver["min_block"]
    )
    if qualifies_silver:
        return {
            "level": "Prata",
            "manager_bonus": float(silver["manager_value"]),
            "team_fund_enabled": False,
            "reason": "Critérios Prata atendidos. Equipe sem premiação financeira nesta regra.",
        }

    if weighted_score >= cfg["bronze_min_weighted_score"]:
        return {
            "level": "Bronze",
            "manager_bonus": float(cfg["bronze_manager_value_option"]),
            "team_fund_enabled": False,
            "reason": "Bronze aplicado por critério configurável; briefing não definiu critérios completos de Bronze.",
        }

    return {
        "level": "Sem bônus",
        "manager_bonus": 0.0,
        "team_fund_enabled": False,
        "reason": "Critérios mínimos de bonificação não atingidos.",
    }


def action_priority(score: float, is_binary: bool = False) -> str:
    if score <= 4 or (is_binary and score == 0):
        return "Alta"
    if score <= 6:
        return "Média"
    if score <= 7:
        return "Baixa"
    return "Monitoramento"


def default_action_deadline_days(score: float, is_binary: bool = False) -> int:
    if score <= 4 or (is_binary and score == 0):
        return 2
    if score <= 6:
        return 7
    return 14
