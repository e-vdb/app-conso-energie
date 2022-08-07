"""Module with constant variables."""


HIDE_STREAMLIT_STYLE = """
                        <style>
                        #MainMenu {visibility: hidden;}
                        footer {
                                visibility: hidden;
                                }
                        footer:after {
                        content:"Contact: "; 
                        visibility: visible;
                        display: block;
                        position: relative;
                        padding: 5px;
                        top: 2px;
                        color: #f02626;
                                    }
                        </style>
                        """

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
              ## Fonctionnalités

              - Visualiser/remplir vos index de consommation
              - Calculer votre consommation totale
              - Visualiser votre consommation annuelle/ mensuelle
              - Comparer vos consomations mensuelles avec celles des années précédentes

              """
