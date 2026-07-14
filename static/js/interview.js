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

            const response = await fetch("/api/start-interview", {
                method: "POST",
                body: formData
            });

            if (!response.ok)
                throw new Error("Server communication failed.");

            const data = await response.json();

            generatedGuide = data.guide;

            results.innerHTML =
                generatedGuide.replace(/\n/g, "<br>");

            actions.style.display = "flex";

        }

        catch (err) {

            results.innerHTML =
                `<span style="color:#ff5555;">${err.message}</span>`;

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

    copyBtn.addEventListener("click", async () => {

        try {

            await navigator.clipboard.writeText(
                generatedGuide
            );

            copyBtn.innerText = "✓ Copied";

            setTimeout(() => {

                copyBtn.innerText = "📋 Copy";

            }, 1500);

        }

        catch {

            alert("Clipboard access failed.");

        }

    });

    // ==========================================
    // DOCX Download
    // ==========================================

    docxBtn.addEventListener("click", async () => {

        const response = await fetch(
            "/api/download-interview-docx",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    guide: generatedGuide

                })

            }
        );

        const blob = await response.blob();

        const url =
            window.URL.createObjectURL(blob);

        const a =
            document.createElement("a");

        a.href = url;

        a.download = "Interview_Guide.docx";

        a.click();

        URL.revokeObjectURL(url);

    });

    // ==========================================
    // PDF Download
    // ==========================================

    pdfBtn.addEventListener("click", async () => {

        const response = await fetch(
            "/api/download-interview-pdf",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    guide: generatedGuide

                })

            }
        );

        const blob = await response.blob();

        const url =
            window.URL.createObjectURL(blob);

        const a =
            document.createElement("a");

        a.href = url;

        a.download = "Interview_Guide.pdf";

        a.click();

        URL.revokeObjectURL(url);

    });

}

document.addEventListener(
    "DOMContentLoaded",
    initInterviewPrep
);