from models.recommendation_engine import get_recommendations


def generate_market_recommendation(
    crop,
    quantity,
    farmer_location
):
    """
    Backend function that passes farmer information
    to the recommendation engine.
    """

    return get_recommendations(
        crop=crop,
        quantity=quantity,
        farmer_location=farmer_location
    )