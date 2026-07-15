async function apiFetch(url, options = {}) {

    const response = await fetch(url, options);

    if (response.status === 429) {

        const error = await response.json();

        showRateLimit(error.message);

        throw new Error("RATE_LIMIT");
    }

    if (!response.ok) {

        const error = await response.json();

        throw new Error(error.message || "Server Error");
    }

    return response;
}

function showRateLimit(message) {

    const box = document.getElementById("rate-limit-box");

    if (!box) return;

    box.textContent = `⚠ ${message}`;
    box.style.display = "block";
}

function hideRateLimit() {

    const box = document.getElementById("rate-limit-box");

    if (!box) return;

    box.style.display = "none";
}
async function copyToClipboard(text, button, originalText) {

    try {

        await navigator.clipboard.writeText(text);

        button.innerText = "✓ Copied";

        setTimeout(() => {
            button.innerText = originalText;
        }, 1500);

    }

    catch {

        alert("Clipboard access failed.");

    }

}
async function downloadFromApi(
    url,
    body,
    filename
) {

    const response = await apiFetch(url, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(body)

    });

    const blob = await response.blob();

    const objectURL =
        window.URL.createObjectURL(blob);

    const a =
        document.createElement("a");

    a.href = objectURL;

    a.download = filename;

    a.click();

    URL.revokeObjectURL(objectURL);

}

function showError(container, message) {

    container.style.display = "block";

    container.innerHTML =
        `<span style="color:#ff5555;">${message}</span>`;

}