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

        results.innerHTML = "> Connecting to AI...";

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

            const response = await fetch(
                "/api/generate-letter",
                {
                    method: "POST",
                    body: formData
                }
            );

            if (!response.ok)
                throw new Error("Server communication failed.");

            const data = await response.json();

            generatedLetter = data.letter;

            results.innerHTML =
                generatedLetter.replace(/\n/g, "<br>");

            actions.style.display = "flex";

        }

        catch (err) {

            results.innerHTML =
                `<span style="color:#ff5555;">${err.message}</span>`;

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

    copyBtn.addEventListener("click", async () => {

        try {

            await navigator.clipboard.writeText(
                generatedLetter
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
            "/api/download-docx",
            {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    letter: generatedLetter

                })

            }
        );

        const blob = await response.blob();

        const url =
            window.URL.createObjectURL(blob);

        const a =
            document.createElement("a");

        a.href = url;

        a.download = "Cover_Letter.docx";

        a.click();

        URL.revokeObjectURL(url);

    });

    // ==========================================
    // PDF Download
    // ==========================================

    pdfBtn.addEventListener("click", async () => {

        const response = await fetch(
            "/api/download-pdf",
            {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    letter: generatedLetter

                })

            }
        );

        const blob = await response.blob();

        const url =
            window.URL.createObjectURL(blob);

        const a =
            document.createElement("a");

        a.href = url;

        a.download = "Cover_Letter.pdf";

        a.click();

        URL.revokeObjectURL(url);

    });

}

document.addEventListener(
    "DOMContentLoaded",
    initCoverLetterGenerator
);