function initCoverLetterGenerator() {

    console.log("Cover Letter Generator called");

    const jobTextarea = document.getElementById("job-description");
    const button = document.getElementById("generate-letter-btn");
    const results = document.getElementById("cover-letter-results");

    if (!jobTextarea || !button || !results) return;

    button.addEventListener("click", async () => {

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

        button.disabled = true;
        button.innerText = "Generating...";

        results.style.display = "block";
        results.innerHTML = "> Connecting to AI...<br><br>";

        const formData = new FormData();

        formData.append("job_description", jobDescription);
        formData.append("skill_set", skills.join(", "));

        try {

            const response = await fetch("/api/generate-letter", {
                method: "POST",
                body: formData
            });

            if (!response.ok)
                throw new Error("Server communication failed.");

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            results.innerHTML = "";

            while (true) {

                const { done, value } = await reader.read();

                if (done) break;

                const chunk = decoder.decode(value, { stream: true });

                const lines = chunk.split("\n");

                for (const line of lines) {

                    if (!line.startsWith("data: ")) continue;

                    const data = line.substring(6);

                    if (data === "[DONE]") {
                        button.disabled = false;
                        button.innerText = "Generate Cover Letter";
                        return;
                    }

                    results.innerHTML += data;
                    results.scrollTop = results.scrollHeight;

                }

            }

        } catch (err) {

            results.innerHTML =
                `<span style="color:#ff5555;">${err.message}</span>`;

        } finally {

            button.disabled = false;
            button.innerText = "Generate Cover Letter";

        }

    });

}

document.addEventListener("DOMContentLoaded", () => {
    initCoverLetterGenerator();
});