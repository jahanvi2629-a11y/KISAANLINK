async function getRecommendation() {

    const crop =
        document.getElementById("crop").value;

    const quantity =
        document.getElementById("quantity").value;

    const location =
        document.getElementById("location").value;


    const loading =
        document.getElementById("loading");

    const results =
        document.getElementById("results");

    const error =
        document.getElementById("error");

    const button =
        document.getElementById("recommendButton");


    results.classList.add("hidden");

    error.classList.add("hidden");

    loading.classList.remove("hidden");

    button.disabled = true;


    try {

        const response =
            await fetch(
                "/api/recommend",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        crop: crop,
                        quantity: quantity,
                        location: location
                    })
                }
            );


        const data =
            await response.json();


        loading.classList.add("hidden");

        button.disabled = false;


        if (!data.success) {

            error.textContent =
                data.message;

            error.classList.remove("hidden");

            return;
        }


        displayResults(data);

        results.classList.remove("hidden");

    }

    catch (err) {

        loading.classList.add("hidden");

        button.disabled = false;

        error.textContent =
            "Unable to connect to CIVICSYNC backend.";

        error.classList.remove("hidden");

        console.error(err);
    }

}


function displayResults(data) {

    const best =
        data.best_market;


    const bestMarket =
        document.getElementById("bestMarket");


    const estimatedValue =
        Math.round(
            best.estimated_net_value
        );


    bestMarket.innerHTML = `

        <div>

            <p class="recommendation-label">
                ⭐ TOP RECOMMENDATION
            </p>

            <h3>
                ${best.market}
            </h3>

            <p>
                ${best.city}
            </p>

        </div>


        <div class="metric">

            <p class="recommendation-label">
                MARKET PRICE
            </p>

            <p class="metric-value">
                ₹${best.price_per_kg}/kg
            </p>

            <p>
                ${best.trend} trend
            </p>

        </div>


        <div class="metric">

            <p class="recommendation-label">
                ESTIMATED NET VALUE
            </p>

            <p class="metric-value">
                ₹${estimatedValue.toLocaleString()}
            </p>

            <p>
                After estimated transport
            </p>

        </div>

    `;


    const marketCards =
        document.getElementById("marketCards");


    marketCards.innerHTML = "";


    data.recommendations.forEach(
        (market, index) => {

            const card =
                document.createElement("div");

            card.className =
                "market-card";


            card.innerHTML = `

                <h4>
                    ${index === 0 ? "⭐ " : ""}
                    ${market.market}
                </h4>

                <p class="market-city">
                    ${market.city}
                </p>


                <p class="market-price">
                    ₹${market.price_per_kg}/kg
                </p>


                <div class="market-info">
                    <span>Demand</span>
                    <strong>
                        ${market.demand}
                    </strong>
                </div>


                <div class="market-info">
                    <span>Trend</span>
                    <strong>
                        ${market.trend}
                    </strong>
                </div>


                <div class="market-info">
                    <span>Distance</span>
                    <strong>
                        ${market.distance_km} km
                    </strong>
                </div>


                <div class="market-info">
                    <span>Transport</span>
                    <strong>
                        ₹${market.transport_cost.toLocaleString()}
                    </strong>
                </div>


                <div class="market-info">
                    <span>Buyer reliability</span>
                    <strong>
                        ${market.buyer_reliability}%
                    </strong>
                </div>

            `;


            marketCards.appendChild(card);

        }
    );

}