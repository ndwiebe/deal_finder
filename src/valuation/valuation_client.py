# GPT valuation client stub
import os
import json
import openai

class DealAssessment:
    def __init__(self, is_good_deal, estimated_value, comment):
        self.is_good_deal = is_good_deal
        self.estimated_value = estimated_value
        self.comment = comment

class ValuationClient:
    """
    Uses OpenAI ChatCompletion to assess if a listing is a good deal.
    """
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def assess_deal(self, card_data: dict) -> DealAssessment:
        prompt = (
            "You are a sports card valuation assistant.\n"
            f"Card Details:\n"
            f"- Year: {card_data.get('year')}\n"
            f"- Player: {card_data.get('player')}\n"
            f"- Set: {card_data.get('set')}\n"
            f"- Grade: {card_data.get('grade')}\n"
            f"Asking Price: ${card_data.get('price')}\n"
            "Provide a JSON response with fields: deal (true/false), est_value (number), comment (string)."
        )
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful valuation assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            content = resp.choices[0].message.content
            data = json.loads(content)
            return DealAssessment(
                is_good_deal=data.get('deal', False),
                estimated_value=data.get('est_value'),
                comment=data.get('comment')
            )
        except Exception as e:
            print(f"Valuation error: {e}")
            return DealAssessment(False, None, "Valuation failed")
