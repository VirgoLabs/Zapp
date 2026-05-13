document.addEventListener('DOMContentLoaded', () => {
    // 1. Drag and Drop visual feedback for the upload box
    const uploadSection = document.querySelector('.upload-section');
    if (uploadSection) {
        uploadSection.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadSection.classList.add('dragover');
        });
        
        uploadSection.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadSection.classList.remove('dragover');
        });
        
        uploadSection.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadSection.classList.remove('dragover');
            const fileInput = document.getElementById('file');
            if (fileInput && e.dataTransfer.files.length > 0) {
                fileInput.files = e.dataTransfer.files;
            }
        });
    }

    // 2. Auto-inject a "Copy Link" button if a share URL is generated
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

        // Success animation function
        const showSuccess = () => {
            copyBtn.innerText = 'Copied!';
            copyBtn.style.backgroundColor = '#27ae60'; 
            setTimeout(() => {
                copyBtn.innerText = 'Copy Link';
                copyBtn.style.backgroundColor = '#2c3e50';
            }, 2000);
        };

        // Add copy functionality with a fallback for local HTTP testing
        copyBtn.addEventListener('click', () => {
            const textToCopy = (shareUrlDiv.innerText || shareUrlDiv.textContent).trim();

            // Try modern clipboard API first (requires HTTPS or strict localhost)
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(textToCopy)
                    .then(showSuccess)
                    .catch(err => {
                        console.error('Clipboard API failed: ', err);
                        copyBtn.innerText = 'Error copying';
                    });
            } else {
                // Fallback for HTTP (127.0.0.1) development
                const textArea = document.createElement("textarea");
                textArea.value = textToCopy;
                
                // Hide the textarea off-screen
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
                    textArea.remove(); // Clean up
                }
            }
        });
    }
});