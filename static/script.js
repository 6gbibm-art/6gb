document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. View Navigation Logic ---
    const navButtons = document.querySelectorAll('.nav-btn');
    const views = document.querySelectorAll('.view-section');

    navButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Remove active class from all buttons and views
            navButtons.forEach(b => b.classList.remove('active'));
            views.forEach(v => v.classList.remove('active'));

            // Add active class to clicked button
            e.target.classList.add('active');

            // Show corresponding view
            const targetId = e.target.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');
        });
    });

    // --- 2. File Upload Interaction Logic ---
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('resume-upload');
    const analyzeBtn = document.getElementById('analyze-btn');

    if (dropzone && fileInput) {
        // Trigger file input when clicking the dropzone
        dropzone.addEventListener('click', () => {
            fileInput.click();
        });

        // Handle file selection
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                const fileName = e.target.files[0].name;
                
                // Update dropzone UI to show file selected
                dropzone.innerHTML = `<p class="neon-text">> File Loaded: ${fileName}</p>`;
                dropzone.style.borderStyle = 'solid';
                
                // Enable the analyze button
                analyzeBtn.disabled = false;
            }
        });

        // Optional: Basic Drag & Drop visual feedback
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
                // Manually trigger change event
                const event = new Event('change');
                fileInput.dispatchEvent(event);
            }
        });
    }
    // --- 3. AI Integration & Streaming Logic ---
    const resultsContainer = document.getElementById('analysis-results');

    if (analyzeBtn && fileInput) {
        analyzeBtn.addEventListener('click', async () => {
            const file = fileInput.files[0];
            if (!file) return;

            // 1. Prepare the UI for loading
            analyzeBtn.disabled = true;
            analyzeBtn.innerText = "Processing Data...";
            resultsContainer.style.display = "block";
            resultsContainer.innerHTML = "<span class='neon-text'>> Initializing connection to AI core...</span><br><br>";

            // 2. Package the file for the backend
            const formData = new FormData();
            formData.append("file", file);

            try {
                // 3. Send the POST request to FastAPI
                const response = await fetch('/api/analyze-resume', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) throw new Error("Server communication failed.");

                // 4. Initialize the Stream Reader
                const reader = response.body.getReader();
                const decoder = new TextDecoder("utf-8");
                resultsContainer.innerHTML = ""; // Clear the loading text

                // 5. Read the stream chunk by chunk
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    const chunk = decoder.decode(value, { stream: true });
                    
                    // Parse the Server-Sent Events (SSE) format
                    const lines = chunk.split('\n');
                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            const data = line.replace('data: ', '');
                            
                            // Check for our custom stop signal from the backend
                            if (data === '[DONE]') {
                                analyzeBtn.innerText = "Analysis Complete";
                                return;
                            }
                            
                            // Inject the text directly into the UI
                            resultsContainer.innerHTML += data;
                            
                            // Auto-scroll to the bottom as new text streams in
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
});