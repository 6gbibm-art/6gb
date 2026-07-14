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

    async function generateLetter() {

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

        results.innerHTML =
            "> Connecting to AI...<br><br>";

        const formData = new FormData();

        formData.append("job_description", jobDescription);

        formData.append(
            "skill_set",
            skills.join(", ")
        );

        try {

            const response = await fetch("/api/generate-letter", {

                method: "POST",

                body: formData

            });

            if (!response.ok)
                throw new Error("Server communication failed.");

            const reader = response.body.getReader();

            const decoder = new TextDecoder();

            generatedLetter = "";

            results.innerHTML = "";

            while (true) {
                const { done, value } = await reader.read();
                
                if (done) break;
                
                const chunk = decoder.decode(value, { stream: true });
                
                const lines = chunk.split("\n");
                console.log(JSON.stringify(chunk));
                
                for (const line of lines) {
                    
                    if (!line.startsWith("data: "))
                        continue;

                    const data = line.substring(6);

                    if (data === "[DONE]") {

                        actions.style.display = "flex";

                        generateBtn.disabled = false;

                        generateBtn.innerText = "Generate Cover Letter";

                        return;

                    }

                    generatedLetter += data;

                    results.innerHTML =
                        generatedLetter
                            .replace(/\n/g, "<br>");

                    results.scrollTop = results.scrollHeight;

                }

            }

        }

        catch (err) {

            results.innerHTML =
                `<span style="color:#ff5555;">${err.message}</span>`;

        }

        finally {

            generateBtn.disabled = false;

            generateBtn.innerText = "Generate Cover Letter";

        }

    }

    generateBtn.addEventListener("click", generateLetter);

    regenerateBtn.addEventListener("click", generateLetter);

    copyBtn.addEventListener("click", async () => {

        try {

            await navigator.clipboard.writeText(generatedLetter);

            copyBtn.innerText = "✓ Copied";

            setTimeout(() => {

                copyBtn.innerText = "📋 Copy";

            }, 1500);

        }

        catch {

            alert("Clipboard access failed.");

        }

    });

    docxBtn.addEventListener("click", async () => {

        const response = await fetch("/api/download-docx", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                letter: generatedLetter

            })

        });

        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");

        a.href = url;

        a.download = "Cover_Letter.docx";

        a.click();

        URL.revokeObjectURL(url);

    });

    pdfBtn.addEventListener("click", async () => {

        const response = await fetch("/api/download-pdf", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                letter: generatedLetter

            })

        });

        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");

        a.href = url;

        a.download = "Cover_Letter.pdf";

        a.click();

        URL.revokeObjectURL(url);

    });

}

document.addEventListener("DOMContentLoaded", () => {

    initCoverLetterGenerator();

});