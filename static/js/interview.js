function initInterviewPrep() {

    console.log("Interview Prep initialized");

    let generatedGuide = "";

    const input = document.getElementById("role-title");
    const button = document.getElementById("start-interview-btn");
    const results = document.getElementById("interview-results");

    const actions = document.getElementById("interview-actions");
    const copyBtn = document.getElementById("copy-interview-btn");
    const docxBtn = document.getElementById("download-interview-docx-btn");
    const pdfBtn = document.getElementById("download-interview-pdf-btn");
    const regenerateBtn = document.getElementById("regenerate-interview-btn");

    if (!input || !button || !results) return;

    async function generateInterviewGuide() {
        hideRateLimit();
        const role = input.value.trim();

        if (!role) {

            results.style.display = "block";

            results.innerHTML =
                "<span style='color:#ff5555;'>Please enter a target role.</span>";

            return;
        }

        generatedGuide = "";

        actions.style.display = "none";

        button.disabled = true;
        button.innerText = "Generating...";

        results.style.display = "block";
        results.innerHTML =
            "> Connecting to AI Interview Engine...";

        const formData = new FormData();
        formData.append("role_title", role);

        try {

            const response = await apiFetch("/api/start-interview", {
                method: "POST",
                body: formData
            });

            const data = await response.json();
            hideRateLimit();
            generatedGuide = data.guide;

            results.innerHTML =
                generatedGuide.replace(/\n/g, "<br>");

            actions.style.display = "flex";

        }

        catch (err) {

            if (err.message === "RATE_LIMIT") {

                results.style.display = "none";
                button.innerText = "Start Simulation";
                return;

            }

            showError(
                resultsContainer,
                error.message
            );

        }

        finally {

            button.disabled = false;
            button.innerText = "Start Simulation";

        }

    }

    button.addEventListener(
        "click",
        generateInterviewGuide
    );

    regenerateBtn.addEventListener(
        "click",
        generateInterviewGuide
    );

    // ==========================================
    // Copy
    // ==========================================

    copyBtn.addEventListener("click", () =>
    copyToClipboard(
        generatedGuide,
        copyBtn,
        "📋 Copy"
        )
    );

    // ==========================================
    // DOCX Download
    // ==========================================

    docxBtn.addEventListener("click", () => {

    downloadFromApi(

        "/api/download-interview-docx",

        {
            guide: generatedGuide
        },

        "Interview_Guide.docx"

    );

    });

// PDF Download
// ==========================================

    pdfBtn.addEventListener("click", () => {

        downloadFromApi(

            "/api/download-interview-pdf",

            {
                guide: generatedGuide
            },

            "Interview_Guide.pdf"

        );

    });

}

document.addEventListener(
    "DOMContentLoaded",
    initInterviewPrep
);