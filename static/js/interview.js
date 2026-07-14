function initInterviewPrep() {

    console.log("Interview Prep initialized");

    const input = document.getElementById("role-title");
    const button = document.getElementById("start-interview-btn");
    const results = document.getElementById("interview-results");
    
    if (!input || !button || !results) return;

    button.addEventListener("click", async () => {

        const role = input.value.trim();

        if (!role) {
            results.style.display = "block";
            results.innerHTML =
                "<span style='color:#ff5555;'>Please enter a target role.</span>";
            return;
        }

        button.disabled = true;
        button.innerText = "Generating...";

        results.style.display = "block";
        results.innerHTML =
            "> Connecting to AI Interview Engine...<br><br>";

        const formData = new FormData();
        formData.append("role_title", role);
        let markdown = "";
        try {

            const response = await fetch("/api/start-interview", {
                method: "POST",
                body: formData
            });

            if (!response.ok)
                throw new Error("Server communication failed.");

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            results.innerHTML = "";

            let markdown = "";

            while (true) {

                const { done, value } = await reader.read();

                if (done) break;

                const chunk = decoder.decode(value, { stream: true });

                const lines = chunk.split("\n");

                for (const line of lines) {

                    if (!line.startsWith("data: ")) continue;

                    const data = line.substring(6);

                    if (data === "[DONE]") {
                        results.innerHTML = marked.parse(markdown);
                        button.disabled = false;
                        button.innerText = "Start Simulation";

                        return;
                    }

                    markdown += data;
                }
            }

        } catch (err) {

            results.innerHTML +=
                `<br><span style="color:#ff5555;">${err.message}</span>`;

            button.disabled = false;
            button.innerText = "Start Simulation";
        }

    });

}

document.addEventListener("DOMContentLoaded", () => {
    initInterviewPrep();
});