function initResumeAnalyzer() {

    console.log("initResumeAnalyzer called");

    let generatedReport = "";

    const dropzone = document.getElementById("dropzone");
    const fileInput = document.getElementById("resume-upload");
    const analyzeBtn = document.getElementById("analyze-btn");
    const resultsContainer = document.getElementById("analysis-results");

    const actions = document.getElementById("analysis-actions");
    const copyBtn = document.getElementById("copy-analysis-btn");
    const pdfBtn = document.getElementById("download-analysis-pdf-btn");
    const regenerateBtn = document.getElementById("regenerate-analysis-btn");

    if (!dropzone || !fileInput) return;

    // ============================
    // File Selection
    // ============================

    fileInput.addEventListener("change", (e) => {

        if (e.target.files.length > 0) {

            const fileName = e.target.files[0].name;

            const textNode =
                document.getElementById("dropzone-text") || dropzone;

            textNode.innerHTML = `> File Loaded: ${fileName}`;

            dropzone.style.borderStyle = "solid";

            analyzeBtn.disabled = false;
        }

    });

    // ============================
    // Drag & Drop
    // ============================

    dropzone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropzone.style.background = "rgba(0,240,255,.3)";
    });

    dropzone.addEventListener("dragleave", () => {
        dropzone.style.background = "var(--neon-cyan-dim)";
    });

    dropzone.addEventListener("drop", (e) => {

        e.preventDefault();

        dropzone.style.background = "var(--neon-cyan-dim)";

        if (e.dataTransfer.files.length > 0) {

            fileInput.files = e.dataTransfer.files;
            fileInput.dispatchEvent(new Event("change"));

        }

    });

    // ============================
    // Resume Analysis
    // ============================

    async function analyzeResume() {

        const file = fileInput.files[0];

        if (!file) return;

        generatedReport = "";

        actions.style.display = "none";

        analyzeBtn.disabled = true;
        analyzeBtn.innerText = "Analyzing...";

        resultsContainer.style.display = "block";
        resultsContainer.innerHTML =
            "> Initializing AI analysis...";

        const formData = new FormData();
        formData.append("file", file);

        try {

            const response = await fetch("/api/analyze-resume", {
                method: "POST",
                body: formData
            });

            if (!response.ok)
                throw new Error("Server communication failed.");

            const data = await response.json();

            generatedReport = data.report;

            resultsContainer.innerHTML =
                generatedReport.replace(/\n/g, "<br>");

            actions.style.display = "flex";

            analyzeBtn.innerText = "Analysis Complete";

        }

        catch (error) {

            resultsContainer.innerHTML =
                `<span style="color:#ff5555;">${error.message}</span>`;

            analyzeBtn.innerText = "Retry Analysis";

        }

        finally {

            analyzeBtn.disabled = false;

        }

    }

    analyzeBtn.addEventListener(
        "click",
        analyzeResume
    );

    regenerateBtn.addEventListener(
        "click",
        analyzeResume
    );

    // ============================
    // Copy
    // ============================

    copyBtn.addEventListener("click", async () => {

        try {

            await navigator.clipboard.writeText(
                generatedReport
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

    // ============================
    // PDF Download
    // ============================

    pdfBtn.addEventListener("click", async () => {

        const response = await fetch(
            "/api/download-analysis-pdf",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    report: generatedReport

                })

            }
        );

        const blob = await response.blob();

        const url =
            window.URL.createObjectURL(blob);

        const a =
            document.createElement("a");

        a.href = url;

        a.download = "ATS_Report.pdf";

        a.click();

        URL.revokeObjectURL(url);

    });

}

document.addEventListener(
    "DOMContentLoaded",
    initResumeAnalyzer
);