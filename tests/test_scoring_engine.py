"""Tests unitaires pour le moteur de scoring Sentinelle."""

from src.main import CRITICAL_THRESHOLD, ScoringResult, score_data

TEST_DATA_LOW = {"activity_score": 0.2, "suspicion_level": 0.3}
TEST_DATA_MINOR = {"activity_score": 0.6, "suspicion_level": 0.7}
TEST_DATA_CRITICAL = {"activity_score": 0.9, "suspicion_level": 0.95}


def test_score_data_low_risk() -> None:
    """Vérifie le cas où le score est inférieur au seuil mineur."""
    result = score_data(TEST_DATA_LOW)
    assert result.status == "NORMAL"
    assert result.risk_score == 0.25
    assert isinstance(result, ScoringResult)


def test_score_data_minor_warning() -> None:
    """Vérifie le cas où un avertissement mineur est déclenché.

    (Score entre 0.5 et CRITICAL_THRESHOLD).
    """
    result = score_data(TEST_DATA_MINOR)
    assert result.status == "MINOR_WARNING"
    assert round(result.risk_score, 2) == 0.65
    assert result.risk_score < CRITICAL_THRESHOLD


def test_score_data_critical_alert() -> None:
    """Vérifie le cas où l'alerte critique est déclenchée.

    (Score au-dessus de CRITICAL_THRESHOLD).
    """
    result = score_data(TEST_DATA_CRITICAL)
    assert result.status == "CRITICAL_ALERT"
    assert result.risk_score == 0.925
    assert result.risk_score >= CRITICAL_THRESHOLD


def test_score_data_with_missing_keys() -> None:
    """Vérifie que le moteur gère les données d'entrée vides ou incomplètes.

    (robustesse).
    """
    result = score_data({})
    assert result.status == "NORMAL"
    assert result.risk_score == 0.0
