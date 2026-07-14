function initResumeAnalyzer() {
    console.log("initResumeAnalyzer called");

    const dropzone = document.getElementById("dropzone");
    const fileInput = document.getElementById("resume-upload");
    const analyzeBtn = document.getElementById("analyze-btn");
    const resultsContainer = document.getElementById("analysis-results");

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
        dropzone.style.background = "rgba(0, 240, 255, 0.3)";
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
    // Analyze Resume
    // ============================

    analyzeBtn.addEventListener("click", async () => {

        const file = fileInput.files[0];

        if (!file) return;

        analyzeBtn.disabled = true;
        analyzeBtn.innerText = "Analyzing...";

        resultsContainer.style.display = "block";
        resultsContainer.innerHTML = "> Initializing AI analysis...";

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

            resultsContainer.innerHTML =
                data.report.replace(/\n/g, "<br>");

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

    });

}

document.addEventListener(
    "DOMContentLoaded",
    initResumeAnalyzer
);