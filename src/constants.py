"""Module with constant variables."""


CHOICES_INDEX = (
    "👁️ Visualiser vos index",
    "🖋️ Remplir vos index",
    "🖍️ Corriger vos relevés d'index",
)


CHOICES_CONSOMMATION = (
    "📊 Consommation totale",
    "📊 Consommation annuelle",
    "🟩 Comparaison consommation 🟥",
)

DESCRIPTION = """
    # Fonctionnalités

    - Visualiser/remplir vos index de consommation
    - Calculer votre consommation totale
    - Visualiser votre consommation annuelle/ mensuelle
    - Comparer vos consomations mensuelles avec celles des années précédentes

            """

MAP_COLS = {
    "elecday": "Electricité Jour",
    "elecnight": "Electricité Nuit",
    "gas": "Gaz",
    "water": "Eau",
    "rainwater": "Eau de pluie",
    "elecday_consumption": "Electricité jour (kWh)",
    "elecnight_consumption": "Electricité nuit (kWh)",
    "gas_consumption": "Gaz (m3)",
    "water_consumption": "Eau (m3)",
    "rainwater_consumption": "Eau de pluie (m3)",
    "year_consumption": "Année",
}

FRENCH_MONTHS = {
    1: "Janvier",
    2: "Février",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Août",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décembre",
}
