# actions/actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionRecommendTourism(Action):
def run(self, dispatcher: CollectingDispatcher,
tracker: Tracker,
domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


city = tracker.get_slot("ciudad")
tipo = tracker.get_slot("tipo_turismo")
activity = tracker.get_slot("actividad")


# Base de datos simple en memoria (puedes convertirla a JSON/BD externa)
destinos = {
"Quito": [
{"name": "Centro Histórico", "type": "cultura", "details": "Iglesias, museos, plazas"},
{"name": "Mitad del Mundo", "type": "cultura", "details": "Línea ecuatorial, museo"},
{"name": "TelefériQo", "type": "naturaleza", "details": "Vista panorámica de la ciudad"}
],
"Baños": [
{"name": "Pailón del Diablo", "type": "naturaleza", "details": "Cascada imponente"},
{"name": "Casa del Árbol", "type": "aventura", "details": "Balanceo con vista al volcán"},
{"name": "Ruta de las Cascadas", "type": "aventura", "details": "Senderos y cascadas"}
],
"Mindo": [
{"name": "Refugio de Aves", "type": "naturaleza", "details": "Avistamiento de aves"},
{"name": "Canopy Mindo", "type": "aventura", "details": "Canopy y puentes"},
{"name": "Cascadas de Mindo", "type": "naturaleza", "details": "Pequeñas cascadas y senderos"}
]
}


if city:
city_cap = city.title()
if city_cap in destinos:
# Filtrar por tipo o actividad si están definidos
opciones = destinos[city_cap]
if tipo:
opciones = [d for d in opciones if d["type"] == tipo.lower()]
if activity:
opciones = [d for d in opciones if activity.lower() in d["name"].lower() or activity.lower() in d.get("details","").lower()]


if len(opciones) == 0:
dispatcher.utter_message(text=f"En {city_cap} no encontré lugares que coincidan exactamente con tu preferencia, pero puedo darte otras opciones.")
opciones = destinos[city_cap]


msg = f"En {city_cap} te recomiendo: " + ", ".join([o["name"] for o in opciones]) + ". ¿Quieres detalles de alguno?"
dispatcher.utter_message(text=msg)
return []
else:
dispatcher.utter_message(text="Lo siento, todavía no tengo datos para esa ciudad. ¿Te interesa Quito, Baños o Mindo?")
return [SlotSet("ciudad", None)]


# Si no se proporcionó ciudad, dar opciones generales
dispatcher.utter_message(text="Puedo recomendarte destinos en Quito, Baños o Mindo. ¿En cuál estás interesado?")
return []

class ActionProvideDetails(Action):
def name(self) -> Text:
return "action_provide_details"


def run(self, dispatcher: CollectingDispatcher,
tracker: Tracker,
domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


last_recommendation = tracker.latest_message.get('text')
# Ejemplo simple: pedir al usuario que indique el nombre exacto del lugar
dispatcher.utter_message(text="Dime el nombre del lugar sobre el que quieres detalles (por ejemplo: 'Casa del Árbol')")
return []