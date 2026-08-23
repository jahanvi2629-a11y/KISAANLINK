import json
import os


def load_market_data():
    """
    Loads market information from our local JSON dataset.
    """

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "market_data.json")

    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_market_score(market, farmer_location):
    """
    Calculates a simple recommendation score.

    Higher price, stronger demand, better buyer reliability,
    rising trend and lower transport cost increase the score.
    """

    score = 0

    # Price contribution
    score += market["price_per_kg"] * 2

    # Demand contribution
    demand_scores = {
        "High": 20,
        "Medium": 12,
        "Low": 5
    }

    score += demand_scores.get(market["demand"], 5)

    # Price trend contribution
    if market["trend"] == "Rising":
        score += 15
    elif market["trend"] == "Stable":
        score += 8

    # Buyer reliability
    score += market["buyer_reliability"] * 0.2

    # Transport penalty
    score -= market["transport_per_kg"] * 3

    # Distance penalty
    score -= market["distance_km"] * 0.05

    return round(score, 2)


def get_recommendations(crop, quantity, farmer_location):
    """
    Finds suitable markets for the selected crop
    and ranks them according to the recommendation score.
    """

    all_markets = load_market_data()

    crop = crop.strip().lower()

    matching_markets = [
        market
        for market in all_markets
        if market["crop"].lower() == crop
    ]

    if not matching_markets:
        return {
            "success": False,
            "message": "No market data available for this crop.",
            "recommendations": []
        }

    results = []

    for market in matching_markets:

        score = calculate_market_score(
            market,
            farmer_location
        )

        gross_value = market["price_per_kg"] * quantity

        transport_cost = (
            market["transport_per_kg"] * quantity
        )

        estimated_net_value = gross_value - transport_cost

        results.append({
            "market": market["market"],
            "city": market["city"],
            "crop": market["crop"],
            "price_per_kg": market["price_per_kg"],
            "trend": market["trend"],
            "demand": market["demand"],
            "buyer_reliability": market["buyer_reliability"],
            "quality_requirement": market["quality_requirement"],
            "distance_km": market["distance_km"],
            "transport_cost": transport_cost,
            "estimated_gross_value": gross_value,
            "estimated_net_value": estimated_net_value,
            "score": score
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    best = results[0]

    return {
        "success": True,
        "message": "Market recommendations generated successfully.",
        "best_market": best,
        "recommendations": results
    }