function initResumeAnalyzer() {
    console.log("initResumeAnalyzer called");
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('resume-upload');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsContainer = document.getElementById('analysis-results');

    // Break early if we aren't viewing the resume screen element structure
    if (!dropzone || !fileInput) return;

    // Monitor for actual file changes
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            const fileName = e.target.files[0].name;
            
            // Target the internal text layout node cleanly
            const textNode = document.getElementById('dropzone-text') || dropzone;
            textNode.innerHTML = `> File Loaded: ${fileName}`;
            dropzone.style.borderStyle = 'solid';
            
            // Light up the execution button action trigger
            analyzeBtn.disabled = false;
        }
    });

    // Drag-and-drop mechanics support
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.style.background = 'rgba(0, 240, 255, 0.3)';
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.style.background = 'var(--neon-cyan-dim)';
    });
    
    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.style.background = 'var(--neon-cyan-dim)';
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            fileInput.dispatchEvent(new Event('change'));
        }
    });

    // AI Core response processing stream pipeline 
    analyzeBtn.addEventListener('click', async () => {
        const file = fileInput.files[0];
        if (!file) return;

        analyzeBtn.disabled = true;
        analyzeBtn.innerText = "Processing Data...";
        resultsContainer.style.display = "block";
        resultsContainer.innerHTML = "<span class='neon-text'>> Initializing connection to AI core...</span><br><br>";

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch('/api/analyze-resume', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error("Server communication failed.");

            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            resultsContainer.innerHTML = ""; 

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n');
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.replace('data: ', '');
                        if (data === '[DONE]') {
                            analyzeBtn.innerText = "Analysis Complete";
                            return;
                        }
                        resultsContainer.innerHTML += data;
                        resultsContainer.scrollTop = resultsContainer.scrollHeight;
                    }
                }
            }
        } catch (error) {
            resultsContainer.innerHTML += `<br><span style="color: #ff4444;">> Critical Error: ${error.message}</span>`;
            analyzeBtn.disabled = false;
            analyzeBtn.innerText = "Retry Analysis";
        }
    });
}

// Initial attachment
document.addEventListener('DOMContentLoaded', () => {
    initResumeAnalyzer();
});