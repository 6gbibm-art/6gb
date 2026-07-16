let generatedLetter = "";

function initCoverLetterGenerator() {

    console.log("Cover Letter Generator initialized");

    const jobTextarea = document.getElementById("job-description");

    const generateBtn = document.getElementById("generate-letter-btn");

    const results = document.getElementById("cover-letter-results");

    const actions = document.getElementById("letter-actions");

    const copyBtn = document.getElementById("copy-letter-btn");

    const docxBtn = document.getElementById("download-docx-btn");

    const pdfBtn = document.getElementById("download-pdf-btn");

    const regenerateBtn = document.getElementById("regenerate-btn");

    if (!jobTextarea || !generateBtn || !results) return;

    // ==========================================
    // Auto-growing Job Description textarea
    // ==========================================

    const MAX_HEIGHT = 260;

    function resizeTextarea() {

        jobTextarea.style.height = "auto";

        jobTextarea.style.height =
            Math.min(jobTextarea.scrollHeight, MAX_HEIGHT) + "px";

        jobTextarea.style.overflowY =
            jobTextarea.scrollHeight > MAX_HEIGHT
                ? "auto"
                : "hidden";
    }

    resizeTextarea();

    jobTextarea.addEventListener("input", resizeTextarea);

    // ==========================================
    // Generate Cover Letter
    // ==========================================

    async function generateLetter() {
        hideRateLimit();
        const applicantDetails = {

            name: document.getElementById("user-name").value.trim(),

            email: document.getElementById("user-email").value.trim(),

            phone: document.getElementById("user-phone").value.trim(),

            linkedin: document.getElementById("user-linkedin").value.trim(),

            github: document.getElementById("user-github").value.trim(),

            website: document.getElementById("user-website").value.trim()

        };

        const jobDescription = jobTextarea.value.trim();

        const skills = getSelectedSkills();

        if (!jobDescription) {

            results.style.display = "block";

            results.innerHTML =
                "<span style='color:#ff5555;'>Please enter a job description.</span>";

            return;

        }

        if (skills.length === 0) {

            results.style.display = "block";

            results.innerHTML =
                "<span style='color:#ff5555;'>Please select at least one skill.</span>";

            return;

        }

        generatedLetter = "";

        actions.style.display = "none";

        generateBtn.disabled = true;

        generateBtn.innerText = "Generating...";

        results.style.display = "block";

        results.innerHTML = "> Generating Cover Letter...";

        const formData = new FormData();

        formData.append(
            "job_description",
            jobDescription
        );

        formData.append(
            "skill_set",
            skills.join(", ")
        );

        formData.append(
            "applicant_details",
            JSON.stringify(applicantDetails)
        );

        try {

            const response = await apiFetch(
                "/api/generate-letter",
                {
                    method: "POST",
                    body: formData
                }
            );

            hideRateLimit();

            generatedLetter = "";

            results.className = "terminal-text results-panel";
            results.innerHTML = "";

            const reader = response.body.getReader();

            const decoder = new TextDecoder();

            while (true) {

                const { done, value } = await reader.read();

                if (done) break;

                const chunk = decoder.decode(
                    value,
                    { stream: true }
                );

                // Typewriter effect
                for (const char of chunk) {

                    generatedLetter += char;

                    results.innerHTML =
                        generatedLetter.replace(/\n/g, "<br>");

                    results.scrollTop =
                        results.scrollHeight;

                    await new Promise(resolve =>
                        setTimeout(resolve, 1)
                    );

                }

            }

            actions.style.display = "flex";

        }

        catch (err) {

            if (err.message === "RATE_LIMIT") {

                results.style.display = "none";

                generateBtn.innerText = "Generate Cover Letter";

                return;
            }

            showError(
                resultsContainer,
                error.message
            );

        }

        finally {

            generateBtn.disabled = false;

            generateBtn.innerText =
                "Generate Cover Letter";

        }

    }

    // ==========================================
    // Buttons
    // ==========================================

    generateBtn.addEventListener(
        "click",
        generateLetter
    );

    regenerateBtn.addEventListener(
        "click",
        generateLetter
    );

    // ==========================================
    // Copy
    // ==========================================

    copyBtn.addEventListener("click", () =>
    copyToClipboard(
        generatedLetter,
        copyBtn,
        "📋 Copy"
        )
    );

    // ==========================================
    // DOCX Download
    // ==========================================

    docxBtn.addEventListener("click", () => {

    downloadFromApi(

        "/api/download-docx",

        {
            letter: generatedLetter
        },

        "Cover_Letter.docx"

    );

    });

    // ==========================================
    // PDF Download
    // ==========================================
    pdfBtn.addEventListener("click", () => {

    downloadFromApi(

        "/api/download-pdf",

        {
            letter: generatedLetter
        },

        "Cover_Letter.pdf"

    );

    });

}

document.addEventListener(
    "DOMContentLoaded",
    initCoverLetterGenerator
);