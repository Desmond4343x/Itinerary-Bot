# Define headings in order
canonical_headings = [
    "Booking Summary",
    "Flights",
    "Hotel",
    "Airport Transfers",
    "Activities & Vouchers",
    "Traveler Documents (for check-in)",
    "Airline Baggage Policy (Summary)",
    "Hotel Policies (Bayview Resort Goa)",
    "Key Facts for Q&A (Findable by the Mini-Bot)",
    "Contact & Escalation"
]

import os
from dotenv import load_dotenv

load_dotenv()

FILE_PATH = os.getenv("FILE_PATH")

# Initialize
section_map = {}
current_heading = None
current_lines = []

with open(FILE_PATH, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        # Check if this line is a canonical heading
        if line in canonical_headings:
            if current_heading:
                # Save previous section (without duplicating the heading)
                section_map[current_heading] = current_lines
            # Start new section
            current_heading = line
            current_lines = []
        else:
            # Add line to current section
            current_lines.append(line)

# Save the last section
if current_heading:
    section_map[current_heading] = current_lines



heading_tags_map = {
    "Booking Summary": [
        "booking", "summary", "itinerary", "reservation", "trip", "plan", "travel",
        "booking sheet", "trip sheet", "travel summary", "reservation sheet",
        "trip plan", "trip overview", "travel breakdown", "travel itinerary",
        "plan summary", "confirmed plan", "booking overview", "booking breakdown",
        "trip details", "travel details", "travel record", "trip record",
        "booking note", "trip info", "reservation note", "travel plan",
        "trip document", "reservation details", "plan details", "trip listing",
        "travel list", "itinerary summary", "trip booking", "reservation record",
        "itinerary file", "travel log", "plan extract", "reservation extract",
        "itinerary document", "booking status", "trip snapshot", "booking extract",
        "trip schedule", "plan log", "summary page", "booking confirmation",
        "travel confirmation", "confirmation sheet", "travel extract", "plan record"
    ],
    "Flights": [
        "flight", "flights", "airline", "plane", "ticket", "boarding", "departure", "arrival",
        "flight schedule", "boarding pass", "flight detail", "flight info",
        "airline schedule", "plane ticket", "airline info", "flight segment","land","take off","takeoff",
        "air travel", "departure time", "arrival time", "boarding info",
        "airline ticket", "flight number", "flight record", "flight booking",
        "boarding document", "departure flight", "arrival flight", "flight pass",
        "plane pass", "plane info", "flight slip", "boarding slip",
        "domestic flight", "international flight", "plane journey", "flight journey",
        "flight listing", "flight time", "flight seat", "passenger list",
        "boarding gate", "airline code", "flight timing", "airline record",
        "flight page", "flight listing sheet", "departure detail", "arrival detail",
        "flight terminal", "airline boarding", "plane schedule", "flight allocation"
    ],
    "Hotel": [
        "hotel", "room", "stay", "accommodation", "property", "lodging", "residence", "guesthouse","stay","staying","checkin","checkout","check-in","check-out",
        "hotel room", "room booking", "room info", "hotel booking","house","home",
        "hotel detail", "room details", "guest room", "stay info",
        "hotel sheet", "property info", "hotel listing", "residence info",
        "stay record", "room sheet", "lodging info", "accommodation detail",
        "room allocation", "hotel contact", "stay detail", "hotel plan",
        "room category", "room plan", "hotel page", "hotel reference",
        "accommodation plan", "guest record", "room type", "hotel info",
        "residence sheet", "room listing", "property record", "guest stay",
        "hotel slip", "accommodation record", "room detail", "hotel entry",
        "stay sheet", "hotel summary", "guesthouse detail", "hotel description",
        "residence plan", "room guide"
    ],
    "Airport Transfers": [
        "transfer", "pickup", "cab", "shuttle", "ride", "transport", "taxi", "driver",
        "airport pickup", "airport drop", "cab pickup", "cab drop","pickup","pick-up",
        "hotel pickup", "hotel drop", "ride schedule", "cab timing",
        "pickup timing", "pickup detail", "cab detail", "airport ride",
        "transport service", "cab service", "pickup service", "driver detail",
        "airport cab", "arrival cab", "departure cab", "airport shuttle",
        "transfer detail", "pickup record", "cab record", "airport taxi",
        "shuttle service", "cab sheet", "ride info", "transport info",
        "transfer info", "transfer sheet", "cab trip", "ride trip",
        "transfer ride", "pickup time", "cab time", "ride summary",
        "driver info", "airport transfer", "hotel cab", "shuttle info",
        "driver contact", "shuttle record"
    ],
    "Activities & Vouchers": [
        "activity", "activities", "voucher", "vouchers", "event", "excursion", "tour", "ticket", "pass", "sightseeing",
        "event list", "tour list", "trip event", "activity sheet","cruise","beach","hike","hiking","cycling","rent","tasting",
        "voucher sheet", "event schedule", "activity plan", "tour pass",
        "tour schedule", "excursion sheet", "trip voucher", "trip pass",
        "tour plan", "activity listing", "voucher listing", "tour ticket",
        "event ticket", "excursion detail", "event detail", "holiday ticket","tour","meeting point","group",
        "sightseeing plan", "included activity", "voucher detail", "activity detail",
        "activity pass", "tour record", "excursion record", "event record",
        "holiday pass", "entry pass", "activity entry", "trip fun",
        "voucher page", "activity record", "fun plan", "event guide",
        "trip entertainment", "included voucher", "fun event", "excursion pass",
        "ticket voucher", "excursion ticket"
    ],
    "Traveler Documents (for check-in)": [
        "document", "documents", "passport", "visa", "id", "paper", "proof", "identity", "boarding",
        "id proof", "passport copy", "boarding pass", "travel document","carry",
        "guest id", "photo id", "entry paper", "passport page",
        "checkin paper", "boarding paper", "identity proof", "traveler id",
        "guest document", "boarding document", "document list", "entry document",
        "official document", "required document", "travel paper", "checkin id",
        "checkin document", "paperwork", "entry id", "visa page",
        "passport info", "boarding record", "travel id", "guest record",
        "entry sheet", "document pack", "passport detail", "document proof",
        "identity sheet", "document checklist", "passport data", "entry form",
        "document file", "entry info", "travel proof", "document page",
        "boarding file", "id page"
    ],
    "Airline Baggage Policy (Summary)": [
        "baggage", "luggage", "bag", "suitcase", "carry-on", "check-in", "allowance", "weight",
        "baggage info", "luggage policy", "bag policy", "baggage rule","bag","bags",
        "luggage rule", "baggage limit", "baggage sheet", "luggage sheet",
        "baggage allowance", "free baggage", "included baggage", "excess baggage",
        "bag charge", "bag info", "bag guideline", "luggage detail",
        "carry-on rule", "carry-on bag", "checked bag", "checked luggage","carry",
        "cabin bag", "luggage charge", "airline baggage", "bag limit",
        "carry baggage", "check-in bag", "baggage weight", "bag weight",
        "baggage chart", "baggage note", "luggage checklist", "luggage record",
        "baggage pass", "bag checklist", "baggage document", "airline luggage",
        "luggage allocation", "bag instruction", "luggage info", "bag document"
    ],
    "Hotel Policies (Bayview Resort Goa)": [
        "policy", "policies", "rule", "regulation", "condition", "guideline", "instruction", "timing",
        "hotel policy", "resort policy", "stay policy", "guest policy","checkin","checkout","check-in","check-out",
        "house rule", "house policy", "hotel rule", "room rule",
        "guest rule", "hotel instruction", "check-in time", "checkout time",
        "stay rule", "check-in policy", "resort rule", "resort regulation",
        "property policy", "room policy", "hotel condition", "room condition",
        "stay condition", "guest instruction", "check-in window", "stay timing",
        "guest condition", "property rule", "house guideline", "guest guideline",
        "hotel regulation", "room guideline", "check-in rule", "resort guideline",
        "hotel timing", "property timing", "room timing", "room instruction",
        "guest timing", "hotel rulesheet", "property rulesheet", "house constraints",
        "house terms", "resort rulesheet"
    ],
    "Contact & Escalation": [
        "contact", "support", "help", "assistance", "helpline", "hotline", "escalation", "complaint",
        "support team", "support contact", "emergency contact", "travel support","emergency","emergencies","call",
        "helpdesk contact", "support number", "help number", "support info",
        "escalation team", "emergency help", "issue support", "customer support",
        "customer help", "email support", "support sheet", "travel contact",
        "whatsapp support", "phone support", "complaint contact", "contact info",
        "support desk", "helpdesk number", "emergency number", "assistance number",
        "service contact", "service number", "support listing", "help listing","issues","query",
        "hotline number", "emergency listing", "helpline number", "contact team",
        "call center", "issue contact", "trip contact", "travel helpline",
        "customer complaint", "escalation sheet", "report issue", "support record",
        "assistance contact", "contact channel"
    ]
}

def get_maps():
    return heading_tags_map, section_map