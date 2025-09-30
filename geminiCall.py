import json
from google import genai
from query_handler import get_relevant_canonical_headings  # your query->heading function
from mapping import get_maps
heading_tags_map, section_map = get_maps()          # your canonical maps
from dotenv import load_dotenv
load_dotenv()
import os

# Set your Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def query_itinerary(user_query: str):
    """
    Main function to process a user query:
    - Finds relevant headings
    - Prepares JSON data
    - Calls Gemini
    - Returns JSON with explanation, heading_index, data_index
    """

    # Step 1: Get matched canonical headings
    matched_headings_set = get_relevant_canonical_headings(user_query)
    if not matched_headings_set:
        return {
            "explanation": "I don’t see this in your itinerary — contact support",
            "heading": "na",
            "data_index": -1
        }

    # Step 2: Filter section_map to only matched headings
    matched_headings_list = list(matched_headings_set)
    matched_section_map = {
        h: section_map.get(h, []) for h in matched_headings_list
    }

    # Step 3: Prepare JSON input for Gemini
    json_input = {
        "query": user_query,
        "data": matched_section_map
    }

    # Step 4: Build prompt for Gemini
    prompt = f"""
You are a hotel itinerary assistant.

Input JSON:
{json.dumps(json_input)}

Instructions:
- Answer like an assistant, use greetings and process the data given to you and respond in lines, not bullet points. Explain the user what is relevant to the query in a human chat-style understandable format.
- Queries can also be only greetings like hi/hello, in that case, return:
  {{
    "explanation":a generic greeting message back, welcoming how may i help you,
    "heading": "na",
    "data_index": -1
  }}
- ONLY use the data in the 'data' field. No assumptions about the data are allowed.
- Even if the query might be one word, or the question might be incomplete, try to match query to data as close as possible. You have the liberty to assume what user might have been asking if question feels incomplete.
- Return EXACTLY a JSON object with keys:
  "explanation": human-readable chat-like explanation
  "heading": heading used from the input 'data' keys
  "data_index": index (0-based) of the line used from that heading, basically the line that tells most about the solving the query that can be cited.
- If the answer cannot be found, and you feel the query is not at all related to the data provided or out of the scope, return:
  {{
    "explanation":"I don’t see this in your itinerary — contact support",
    "heading": "na",
    "data_index": -1
  }}
- Do NOT include any extra text outside the JSON.
"""

    # Step 5: Call Gemini
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("'''json[") and text.endswith("]'''"):
            text = text[len("'''json"):-3].strip()
        elif text.startswith("```json") and text.endswith("```"):
            text = "\n".join(text.splitlines()[1:-1]).strip()
        elif text.startswith("```") and text.endswith("```"):
            text = "\n".join(text.splitlines()[1:-1]).strip()

        return json.loads(text)

    except json.JSONDecodeError:
        return {
            "explanation": "I don’t see this in your itinerary — contact support",
            "heading": "na",
            "data_index": -1
        }
    except Exception as e:
        return {
            "explanation": f"Error: {str(e)}",
            "heading": "na",
            "data_index": -1
        }


# ------------------------------
# Example usage
# ------------------------------
if __name__ == "__main__":
    while True:
        query = input("\nEnter your query (or 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break

        result = query_itinerary(query)

        print("\nResult:")
        print("Explanation:", result.get("explanation"))

        heading = result.get("heading", "na")
        data_idx = result.get("data_index", -1)

        if heading == "na" or data_idx == -1:
            print("Heading: na (no match)")
            print("Data index: -1 (no match)")
        else:
            # Use indices in the filtered matched_section_map
            data_line = section_map[heading][data_idx]

            print(f"Heading : ({heading})")
            print(f"Data : ({data_line})")