document.addEventListener('DOMContentLoaded', () => {
    
    // --- NEW: Cloudinary Direct Upload Logic ---
    const uploadForm = document.getElementById('uploadForm');
    const submitBtn = document.querySelector('.submit-btn');

    if (uploadForm) {
        uploadForm.addEventListener('submit', (e) => {
            e.preventDefault(); // Stop normal submission
            
            const fileInput = document.getElementById('file');
            
            // Check if file is selected
            if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
                alert("Please select a file to upload.");
                return;
            }

            const file = fileInput.files[0];
            
            // Change button UI to show progress
            submitBtn.innerText = "Uploading to Cloud... Please wait";
            submitBtn.style.backgroundColor = "#f59e0b"; // Orange warning
            submitBtn.disabled = true;

            // Prepare Cloudinary Payload
            const formData = new FormData();
            formData.append('file', file);
            
            // ⚠️ REPLACE THIS STRING WITH YOUR ACTUAL UPLOAD PRESET NAME
            formData.append('upload_preset', 'rs6svgv1'); 

            // Cloudinary API endpoint
            const cloudName = 'dbdahtals'; 
            const cloudinaryUrl = `https://api.cloudinary.com/v1_1/${cloudName}/auto/upload`;

            fetch(cloudinaryUrl, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.secure_url) {
                    // Upload successful! Populate hidden fields
                    document.getElementById('file_url').value = data.secure_url;
                    document.getElementById('file_name').value = file.name;
                    
                    // Submit the form to Django to save the URL to the database
                    submitBtn.innerText = "Generating Secure Link...";
                    uploadForm.submit();
                } else {
                    console.error("Cloudinary error:", data);
                    submitBtn.innerText = "Upload Failed - Try Again";
                    submitBtn.style.backgroundColor = "#ef4444";
                    submitBtn.disabled = false;
                }
            })
            .catch(error => {
                console.error("Fetch failed:", error);
                submitBtn.innerText = "Upload Failed - Try Again";
                submitBtn.style.backgroundColor = "#ef4444";
                submitBtn.disabled = false;
            });
        });
    }

    // --- Original Drag and Drop Logic ---
    const fileInput = document.getElementById('file');
    const dropzoneText = document.getElementById('dropzone-text');
    const dropzoneBox = document.getElementById('dropzone');

    if (fileInput && dropzoneText && dropzoneBox) {
        fileInput.addEventListener('change', function(e) {
            if (this.files && this.files.length > 0) {
                dropzoneText.innerHTML = `<span style="color: #3b82f6; font-weight: bold;">Selected:</span><br><span style="color: #0f172a;">${this.files[0].name}</span>`;
            } else {
                dropzoneText.innerHTML = "Click to browse or drag files<br>here to start sharing";
            }
        });

        dropzoneBox.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropzoneBox.classList.add('dragover');
        });

        dropzoneBox.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dropzoneBox.classList.remove('dragover');
        });

        dropzoneBox.addEventListener('drop', (e) => {
            e.preventDefault();
            dropzoneBox.classList.remove('dragover');
            
            if (e.dataTransfer.files.length > 0) {
                fileInput.files = e.dataTransfer.files;
                fileInput.dispatchEvent(new Event('change'));
            }
        });
    }

    // --- Original Copy Link Logic ---
    const shareUrlDiv = document.querySelector('.share-url');
    if (shareUrlDiv) {
        const copyBtn = document.createElement('button');
        copyBtn.innerText = 'Copy Link';
        copyBtn.className = 'btn';
        copyBtn.style.marginTop = '15px';
        copyBtn.style.backgroundColor = '#2c3e50';
        copyBtn.style.padding = '8px 15px';
        copyBtn.style.fontSize = '10pt';
        
        shareUrlDiv.parentNode.insertBefore(copyBtn, shareUrlDiv.nextSibling);

        const showSuccess = () => {
            copyBtn.innerText = 'Copied!';
            copyBtn.style.backgroundColor = '#27ae60'; 
            setTimeout(() => {
                copyBtn.innerText = 'Copy Link';
                copyBtn.style.backgroundColor = '#2c3e50';
            }, 2000);
        };

        copyBtn.addEventListener('click', () => {
            const textToCopy = (shareUrlDiv.innerText || shareUrlDiv.textContent).trim();

            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(textToCopy)
                    .then(showSuccess)
                    .catch(err => {
                        console.error('Clipboard API failed: ', err);
                        copyBtn.innerText = 'Error copying';
                    });
            } else {
                const textArea = document.createElement("textarea");
                textArea.value = textToCopy;
                textArea.style.position = "absolute";
                textArea.style.left = "-999999px";
                document.body.appendChild(textArea);
                
                textArea.select();
                try {
                    document.execCommand('copy');
                    showSuccess();
                } catch (error) {
                    console.error('Fallback copy failed', error);
                    copyBtn.innerText = 'Error copying';
                } finally {
                    textArea.remove();
                }
            }
        });
    }
});