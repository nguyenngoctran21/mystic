from typing import TypedDict
from astrology_calculator import AstrologyCalculator
from numerology_calculator import NumerologyCalculator

class Profile(TypedDict):
    name: str
    birth_date: str  # dd/mm/yyyy
    birth_time: str  # HH:MM
    birth_place: str

def run(profile: Profile) -> str:
    # ----- THẦN SỐ HỌC -----
    try:
        numerology = NumerologyCalculator(profile['name'], profile['birth_date'])
        numerology_result = numerology.get_all()
        numerology_text = "\n".join([
            f"- Life Path: {numerology_result['life_path']}",
            f"- Expression: {numerology_result['expression']}",
            f"- Soul Urge: {numerology_result['soul_urge']}",
            f"- Personality: {numerology_result['personality']}",
            f"- Birthday: {numerology_result['birthday']}",
            f"- Maturity: {numerology_result['maturity']}",
            f"- Balance: {numerology_result['balance']}",
            f"- Hidden Passion: {numerology_result['hidden_passion']}"
        ])
    except Exception as e:
        numerology_text = f"Lỗi khi tính thần số học: {e}"

    # ----- CHIÊM TINH -----
    try:
        astrology = AstrologyCalculator(
            name=profile['name'],
            birthdate=profile['birth_date'],
            birthtime=profile['birth_time'],
            birthplace=profile['birth_place']
        )
        astrology_text = astrology.get_birth_chart_text()
    except Exception as e:
        astrology_text = f"Lỗi khi tính chiêm tinh: {e}"

    return (
        f"🌟 THẦN SỐ HỌC:\n{numerology_text}\n\n"
        f"🌭️ CHIÊM TINH:\n{astrology_text}"
    )