document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const dropArea = document.getElementById('dropArea');
    const uploadStatus = document.getElementById('uploadStatus');
    const jobIdInput = document.getElementById('jobIdInput');
    const checkJobBtn = document.getElementById('checkJobBtn');
    const jobStatus = document.getElementById('jobStatus');
    const analyizeBtn = document.getElementById('analyzeBtn');
    const analysisResults = document.getElementById('analysisResults');

    const viewTableBtn = document.getElementById('viewTableBtn');
    const viewTable = document.getElementById('viewTable');
    const tableNameInput = document.getElementById('tableNameInput');

    

    let currentJobId = null;

    viewTableBtn.addEventListener('click', async function() {
        if (!currentJobId) {
            alert('No job selected');
            return;
        }
        const response = await fetch(`/api/table/${currentJobId}`);
        const data = await response.json();
        viewTable.innerHTML = `<p>${data}</p>`;
    });

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropArea.classList.add('active');
    }

    function unhighlight() {
        dropArea.classList.remove('active');
    }

    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;
        updateFileDisplay(files[0]);
    }

    fileInput.addEventListener('change', function() {
        if (this.files.length) {
            updateFileDisplay(this.files[0]);
        }
    });

    function updateFileDisplay(file) {
        const dropContent = dropArea.querySelector('.drop-content');
        dropContent.innerHTML = `
            <svg class="upload-icon" viewBox="0 0 24 24">
                <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
            </svg>
            <p>${file.name} (${formatFileSize(file.size)})</p>
        `;
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!fileInput.files.length) {
            showStatus('Please select a file first', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            showStatus('Uploading file...', 'warning');
            
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Error: ${errorData.error}`);
            }

            const data = await response.json();
            currentJobId = data.job_id;
            
            showStatus(`File uploaded successfully! Job ID: ${data.job_id}`, 'success');
            jobIdInput.value = data.job_id;
            checkJobStatus(data.job_id);
            
        } catch (error) {
            showStatus(`Upload failed: ${error.message}`, 'error');
            console.error('Upload error:', error);
        }
    });

    checkJobBtn.addEventListener('click', function() {
        const jobId = jobIdInput.value.trim();
        if (!jobId) {
            showJobStatus('Please enter a Job ID', 'error');
            return;
        }
        currentJobId = jobId;
        checkJobStatus(jobId);
    });

    async function checkJobStatus(jobId) {
        try {
            showJobStatus('Checking job status...', 'warning');
            
            const response = await fetch(`/api/jobs/${jobId}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const jobData = await response.json();
            
            let statusHtml = `
                <div class="job-info">
                    <p><strong>Job ID:</strong> ${jobData.id}</p>
                    <p><strong>Status:</strong> <span class="${getStatusClass(jobData.status)}">${jobData.status}</span></p>
                    <p><strong>Created At:</strong> ${new Date(jobData.created_at).toLocaleString()}</p>
                    ${jobData.completed_at ? `<p><strong>Completed At:</strong> ${new Date(jobData.completed_at).toLocaleString()}</p>` : ''}
                    ${jobData.message ? `<p><strong>Message:</strong> ${jobData.message}</p>` : ''}
                </div>
            `;
            
            if (jobData.results) {
                showJobResults(JSON.stringify(jobData.results, null, 2), 'success')
            }
            
            showJobStatus(statusHtml, 'success');
            
            // Enable/disable analyze button based on status
            analyizeBtn.disabled = jobData.status === 'completed';
            
        } catch (error) {
            showJobStatus(`Failed to check job status: ${error.message}`, 'error');
            // analyizeBtn.disabled = true;
            console.error('Job status error:', error);
        }
    }

    analyizeBtn.addEventListener('click', async function() {
        if (!currentJobId) {
            alert('No job selected');
            return;
        }
        
        try {
            showJobStatus('Starting analysis...', 'warning');
            analyizeBtn.disabled = true;
            
            const response = await fetch(`/api/analysis/${currentJobId}`, {
                method: 'POST'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            showJobStatus('Analysis started successfully!', 'success');
            
            setTimeout(() => {
                checkJobStatus(currentJobId);
            }, 2000);
            
        } catch (error) {
            showJobStatus(`Analysis failed to start: ${error.message}`, 'error');
            analyizeBtn.disabled = false;
            console.error('Analysis error:', error);
        }
    });

    function showStatus(message, type) {
        uploadStatus.innerHTML = message;
        uploadStatus.className = `status-message ${type}`;
    }

    function showJobStatus(message, type) {
        if (typeof message === 'string') {
            jobStatus.innerHTML = `<p>${message}</p>`;
        } else {
            jobStatus.innerHTML = message;
        }
        jobStatus.className = `status-display ${type}`;
    }
    function showJobResults(message, type) {
        analysisResults.innerHTML = `<p>${message}</p>`;
        analysisResults.className = `results-display ${type}`;
    }

    function getStatusClass(status) {
        switch (status.toLowerCase()) {
            case 'completed': return 'success';
            case 'failed': return 'error';
            case 'processing': return 'warning';
            default: return '';
        }
    }
});