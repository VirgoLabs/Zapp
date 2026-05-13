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
        // Create the button dynamically
        const copyBtn = document.createElement('button');
        copyBtn.innerText = 'Copy Link';
        copyBtn.className = 'btn';
        copyBtn.style.marginTop = '15px';
        copyBtn.style.backgroundColor = '#2c3e50';
        copyBtn.style.padding = '8px 15px';
        copyBtn.style.fontSize = '10pt';
        
        // Insert it right after the URL box
        shareUrlDiv.parentNode.insertBefore(copyBtn, shareUrlDiv.nextSibling);

        // Add copy functionality
        copyBtn.addEventListener('click', () => {
            const textToCopy = shareUrlDiv.innerText || shareUrlDiv.textContent;
            navigator.clipboard.writeText(textToCopy.trim()).then(() => {
                copyBtn.innerText = 'Copied!';
                copyBtn.style.backgroundColor = '#27ae60'; // Green on success
                
                // Reset button text after 2 seconds
                setTimeout(() => {
                    copyBtn.innerText = 'Copy Link';
                    copyBtn.style.backgroundColor = '#2c3e50';
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy URL: ', err);
                copyBtn.innerText = 'Error copying';
            });
        });
    }
});