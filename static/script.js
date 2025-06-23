document.addEventListener('DOMContentLoaded', () => {

    // --- General File Handling & UI ---
    const fileInput = document.querySelector('input[type="file"]');
    const fileListContainer = document.getElementById('file-list');
    const uploadArea = document.querySelector('.upload-area');

    if (uploadArea) {
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('drag-over');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
            if (e.dataTransfer.files.length > 0) {
                fileInput.files = e.dataTransfer.files;
                updateFileList(fileInput.files);
            }
        });

        fileInput.addEventListener('change', () => {
            updateFileList(fileInput.files);
        });
    }

    function updateFileList(files) {
        fileListContainer.innerHTML = '';
        Array.from(files).forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.textContent = file.name;
            fileListContainer.appendChild(fileItem);
        });
    }

    function handleFormSubmit(form, url) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const errorMessage = form.parentElement.querySelector('.error-message');
            const loadingSpinner = form.parentElement.querySelector('.spinner');
            const submitButton = form.querySelector('.action-button');
            
            errorMessage.textContent = '';
            
            if (fileInput.files.length === 0) {
                errorMessage.textContent = 'Please select a file first.';
                return;
            }

            const formData = new FormData(form);

            submitButton.style.display = 'none';
            loadingSpinner.style.display = 'block';

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const downloadUrl = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = downloadUrl;
                    
                    const contentDisposition = response.headers.get('Content-Disposition');
                    let filename = 'download';
                    if (contentDisposition) {
                        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
                        if (filenameMatch.length > 1) {
                            filename = filenameMatch[1];
                        }
                    }
                    a.download = filename;
                    
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(downloadUrl);
                    a.remove();
                    
                    fileInput.value = '';
                    updateFileList([]);
                } else {
                    const errorData = await response.json();
                    errorMessage.textContent = errorData.error || 'An unexpected error occurred.';
                }
            } catch (error) {
                errorMessage.textContent = 'An error occurred while communicating with the server.';
            } finally {
                submitButton.style.display = 'block';
                loadingSpinner.style.display = 'none';
            }
        });
    }

    // --- Page-specific Logic ---
    const mergeForm = document.getElementById('merge-form');
    if (mergeForm) {
        handleFormSubmit(mergeForm, '/api/merge');
    }

    const wordToPdfForm = document.getElementById('word-to-pdf-form');
    if (wordToPdfForm) {
        handleFormSubmit(wordToPdfForm, '/api/word-to-pdf');
    }

    const pdfToWordForm = document.getElementById('pdf-to-word-form');
    if (pdfToWordForm) {
        handleFormSubmit(pdfToWordForm, '/api/pdf-to-word');
    }
}); 