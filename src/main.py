"""Moteur de scoring de base pour le projet Sentinelle."""

from typing import Any, Dict, NamedTuple

CRITICAL_THRESHOLD = 0.85


class ScoringResult(NamedTuple):
    """Résultat structuré du moteur de scoring.

    Attributes:
        risk_score: Le score de risque calculé (0.0 à 1.0).
        status: La décision métier ('NORMAL', 'MINOR_WARNING', 'CRITICAL_ALERT').
        message: Description détaillée du résultat.
    """

    risk_score: float
    status: str
    message: str


def calculate_risk(data: Dict[str, Any]) -> float:
    """Calcule un score de risque simple basé sur les données d'entrée.

    Args:
        data: Un dictionnaire contenant les facteurs de risque.
              Exemple : {"activity_score": 0.9, "suspicion_level": 0.5}

    Returns:
        Un score de risque agrégé (float).
    """
    factor_a = float(data.get("activity_score", 0.0))
    factor_b = float(data.get("suspicion_level", 0.0))

    return (factor_a + factor_b) / 2.0


def score_data(data: Dict[str, Any]) -> ScoringResult:
    """Fonction principale : applique la logique de seuil sur le risque calculé.

    Args:
        data: Les données brutes ou nettoyées à évaluer.

    Returns:
        Un objet ScoringResult contenant le score et la décision.
    """
    risk = calculate_risk(data)

    if risk >= CRITICAL_THRESHOLD:
        status = "CRITICAL_ALERT"
        message = (
            f"Risk score ({risk:.2f}) exceeds critical threshold "
            f"({CRITICAL_THRESHOLD})."
        )
    elif risk >= 0.5:
        status = "MINOR_WARNING"
        message = f"Risk score ({risk:.2f}) indicates potential issue."
    else:
        status = "NORMAL"
        message = f"Risk score ({risk:.2f}) is low."

    return ScoringResult(risk_score=risk, status=status, message=message)


if __name__ == "__main__":  # pragma: no cover
    critical_case = {"activity_score": 0.9, "suspicion_level": 0.95}
    result = score_data(critical_case)
    print(f"Scoring Result: {result.status} (Score: {result.risk_score:.2f})")
