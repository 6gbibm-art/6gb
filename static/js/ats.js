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
        hideRateLimit();
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
        hideRateLimit();
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

            const response = await apiFetch("/api/analyze-resume", {
                method: "POST",
                body: formData
            });

            hideRateLimit();

            resultsContainer.className = "terminal-text results-panel";
            resultsContainer.innerHTML = "";

            generatedReport = "";

            const reader = response.body.getReader();

            const decoder = new TextDecoder();

            while (true) {

                const { done, value } = await reader.read();

                if (done) {
                    break;
                }

                const chunk = decoder.decode(value, { stream: true });

                generatedReport += chunk;

                resultsContainer.innerHTML =
                    generatedReport.replace(/\n/g, "<br>");

                resultsContainer.scrollTop =
                    resultsContainer.scrollHeight;
            }

            actions.style.display = "flex";

            analyzeBtn.innerText = "Analysis Complete";

        }

        catch (error) {
            if (error.message === "RATE_LIMIT") {

                resultsContainer.style.display = "none";
                analyzeBtn.innerText = "Retry Analysis";
                return;
            }
            showError(
                resultsContainer,
                error.message
            );
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
    copyBtn.addEventListener("click", () =>
    copyToClipboard(
        generatedReport,
        copyBtn,
        "📋 Copy"
        )
    );

    // ============================
    // PDF Download
    // ============================
    pdfBtn.addEventListener("click", () => {
    downloadFromApi(

        "/api/download-analysis-pdf",
        {
            report: generatedReport
        },
        "ATS_Report.pdf"
    );
    });
}
document.addEventListener(
    "DOMContentLoaded",
    initResumeAnalyzer
);