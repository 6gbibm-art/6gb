function initAboutPage() {

    console.log("About page initialized");

    const cards =
        document.querySelectorAll(".team-card");

    const modal =
        document.getElementById("team-modal");

    const closeBtn =
        document.getElementById("close-modal");

    const modalPhoto =
        document.getElementById("modal-photo");

    const modalName =
        document.getElementById("modal-name");

    const modalRole =
        document.getElementById("modal-role");

    const modalContributions =
        document.getElementById("modal-contributions");

    const modalLinks =
        document.getElementById("modal-links");

    if (!cards.length || !modal) return;

    // ==========================================
    // Open Modal
    // ==========================================

    function openModal(card) {

        modalPhoto.src =
            "/static/images/team/" +
            card.dataset.photo;

        modalPhoto.alt =
            card.dataset.name;

        modalName.textContent =
            card.dataset.name;

        modalRole.textContent =
            card.dataset.role;

        // ==========================
        // Contributions
        // ==========================

        modalContributions.innerHTML = "";

        const contributions =
            JSON.parse(card.dataset.contributions);

        contributions.forEach(item => {

            const li =
                document.createElement("li");

            li.textContent = item;

            modalContributions.appendChild(li);

        });

        // ==========================
        // Links
        // ==========================

        modalLinks.innerHTML = "";

        // Email

        // Email

    if (card.dataset.email) {

        const email =
            document.createElement("button");

        email.type = "button";

        email.className = "modal-copy-btn";

        email.innerHTML = "📧 Copy Email";

        email.addEventListener("click", async () => {

            try {

                await navigator.clipboard.writeText(
                    card.dataset.email
                );

                showCopyToast("Email copied to clipboard!");

            }

            catch {

                showCopyToast("Clipboard access failed.");

            }

        });

        modalLinks.appendChild(email);

    }

        // GitHub

        // GitHub

        if (card.dataset.github) {

            const github =
                document.createElement("a");

            github.href =
                card.dataset.github;

            github.target = "_blank";

            github.innerHTML = `
                <img
                    src="/static/images/favicon/github.png"
                    class="member-icon"
                    alt="GitHub">

                GitHub
            `;

            modalLinks.appendChild(github);

        }

        // LinkedIn

        if (card.dataset.linkedin) {

            const linkedin =
                document.createElement("a");

            linkedin.href =
                card.dataset.linkedin;

            linkedin.target = "_blank";

            linkedin.innerHTML = `
                <img
                    src="/static/images/favicon/linkedin.png"
                    class="member-icon"
                    alt="LinkedIn">

                LinkedIn
            `;

            modalLinks.appendChild(linkedin);

}

        // Portfolio

        if (card.dataset.portfolio) {

            const portfolio =
                document.createElement("a");

            portfolio.href =
                card.dataset.portfolio;

            portfolio.target = "_blank";

            portfolio.innerHTML =
                "🌐 Portfolio";

            modalLinks.appendChild(portfolio);

        }

        modal.classList.add("show");

        document.body.style.overflow = "hidden";

    }

    // ==========================================
    // Close Modal
    // ==========================================

    function closeModal() {

        modal.classList.remove("show");

        document.body.style.overflow = "";

    }

    // ==========================================
    // Card Click
    // ==========================================

    cards.forEach(card => {

        const button =
            card.querySelector(".view-details-btn");

        button.addEventListener(
            "click",
            function (e) {

                e.stopPropagation();

                openModal(card);

            }
        );

        card.addEventListener(
            "click",
            function () {

                openModal(card);

            }
        );

    });

    // ==========================================
    // Close Button
    // ==========================================

    closeBtn.addEventListener(
        "click",
        closeModal
    );

    // ==========================================
    // Click Outside Modal
    // ==========================================

    modal.addEventListener(
        "click",
        function (e) {

            if (e.target === modal) {

                closeModal();

            }

        }
    );

    // ==========================================
    // ESC Key
    // ==========================================

    document.addEventListener(
        "keydown",
        function (e) {

            if (
                e.key === "Escape" &&
                modal.classList.contains("show")
            ) {

                closeModal();

            }

        }
    );

}
function showCopyToast(message) {

    const toast =
        document.getElementById("copy-toast");

    if (!toast) return;

    toast.textContent = message;

    toast.classList.add("show");

    clearTimeout(toast.hideTimer);

    toast.hideTimer = setTimeout(() => {

        toast.classList.remove("show");

    }, 2000);

}
document.addEventListener(
    "DOMContentLoaded",
    initAboutPage
);