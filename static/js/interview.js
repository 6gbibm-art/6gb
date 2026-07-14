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

            results.innerHTML =
                data.guide.replace(/\n/g, "<br>");

        }

        catch (err) {

            results.innerHTML =
                `<span style="color:#ff5555;">${err.message}</span>`;

        }

        finally {

            button.disabled = false;
            button.innerText = "Start Simulation";

        }

    });

}

document.addEventListener("DOMContentLoaded", () => {
    initInterviewPrep();
});