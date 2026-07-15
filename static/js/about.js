function initAboutPage() {

    console.log("About page initialized");

    const cards = document.querySelectorAll(".team-card");

    if (!cards.length) return;

    cards.forEach(card => {

        const button = card.querySelector(".expand-btn");

        // ===========================
        // Toggle Function
        // ===========================

        function toggleCard() {

            const isActive =
                card.classList.contains("active");

            // Close all other cards
            cards.forEach(otherCard => {

                if (otherCard !== card) {

                    otherCard.classList.remove("active");

                    const otherButton =
                        otherCard.querySelector(".expand-btn");

                    if (otherButton) {

                        otherButton.innerText =
                            "View Details";

                    }

                }

            });

            // Toggle current card

            if (isActive) {

                card.classList.remove("active");

                button.innerText =
                    "▼View Details";

            }

            else {

                card.classList.add("active");

                button.innerText =
                    "▲Hide Details";

            }

        }

        // ===========================
        // Clicking card
        // ===========================

        card.addEventListener(
            "click",
            toggleCard
        );

        // ===========================
        // Prevent double firing
        // ===========================

        button.addEventListener(
            "click",
            function (e) {

                e.stopPropagation();

                toggleCard();

            }
        );

    });

}

document.addEventListener(
    "DOMContentLoaded",
    initAboutPage
);