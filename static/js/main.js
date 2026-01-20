// Tab Switching
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn. classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName + '-tab').classList.add('active');
    
    // Activate button
    event.target.classList.add('active');
    
    // Clear previous results
    clearResults();
}

// Handle File Selection
function handleFileSelect(event) {
    const file = event. target.files[0];
    const fileName = document.getElementById('fileName');
    const uploadBtn = document.getElementById('uploadBtn');
    
    if (file) {
        fileName.textContent = file.name;
        uploadBtn.disabled = false;
    } else {
        fileName.textContent = 'Choose a file or drag here';
        uploadBtn. disabled = true;
    }
}

// Tokenize Text Input
async function tokenizeText() {
    const code = document.getElementById('codeInput').value;
    
    if (!code.trim()) {
        showError('Please enter some code to tokenize.');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/tokenize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayTokens(data.tokens, data.errors, data.total_tokens);
        } else {
            showError(data.error || 'An error occurred during tokenization.');
        }
    } catch (error) {
        showError('Network error:  ' + error.message);
    } finally {
        hideLoading();
    }
}

// Tokenize Uploaded File
async function tokenizeFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        showError('Please select a file first.');
        return;
    }
    
    showLoading();
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayTokens(data.tokens, data.errors, data.total_tokens);
        } else {
            showError(data.error || 'An error occurred during file processing.');
        }
    } catch (error) {
        showError('Network error: ' + error. message);
    } finally {
        hideLoading();
    }
}

// Display Tokens in Table
function displayTokens(tokens, errors, totalTokens) {
    // Hide empty state and error display
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('errorDisplay').style.display = 'none';
    
    // Show stats
    const statsDiv = document.getElementById('stats');
    statsDiv.style.display = 'flex';
    document.getElementById('totalTokens').textContent = totalTokens;
    document.getElementById('errorCount').textContent = errors.length;
    
    // Display lexical errors if any
    const lexicalErrorsDiv = document.getElementById('lexicalErrors');
    const errorList = document.getElementById('errorList');
    
    if (errors.length > 0) {
        lexicalErrorsDiv.style.display = 'block';
        errorList.innerHTML = '';
        errors.forEach(error => {
            const li = document.createElement('li');
            li.textContent = error;
            errorList.appendChild(li);
        });
    } else {
        lexicalErrorsDiv.style.display = 'none';
    }
    
    // Display tokens in table
    const tableContainer = document.getElementById('tokenTableContainer');
    const tableBody = document.getElementById('tokenTableBody');
    
    tableContainer.style.display = 'block';
    tableBody.innerHTML = '';
    
    tokens.forEach((token, index) => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${index + 1}</td>
            <td><span class="token-type token-${token.type}">${token.type}</span></td>
            <td><span class="token-value">${escapeHtml(token.value)}</span></td>
            <td>${token.line}</td>
            <td>${token.position}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

// Show Loading Indicator
function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('tokenTableContainer').style.display = 'none';
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('errorDisplay').style.display = 'none';
    document.getElementById('stats').style.display = 'none';
    document.getElementById('lexicalErrors').style.display = 'none';
}

// Hide Loading Indicator
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

// Show Error Message
function showError(message) {
    const errorDiv = document. getElementById('errorDisplay');
    errorDiv.textContent = '❌ ' + message;
    errorDiv.style.display = 'block';
    
    document.getElementById('tokenTableContainer').style.display = 'none';
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('stats').style.display = 'none';
    document.getElementById('lexicalErrors').style.display = 'none';
}

// Clear Input
function clearInput() {
    document.getElementById('codeInput').value = '';
    clearResults();
}

// Clear Results
function clearResults() {
    document.getElementById('tokenTableContainer').style.display = 'none';
    document.getElementById('errorDisplay').style.display = 'none';
    document.getElementById('stats').style.display = 'none';
    document.getElementById('lexicalErrors').style.display = 'none';
    document.getElementById('emptyState').style.display = 'block';
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<':  '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Keyboard Shortcut:  Ctrl+Enter to tokenize
document.getElementById('codeInput').addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'Enter') {
        tokenizeText();
    }
});

// Drag and drop file upload
const fileLabel = document.querySelector('. file-label');

fileLabel.addEventListener('dragover', function(e) {
    e.preventDefault();
    this.style.background = '#e8ebff';
});

fileLabel.addEventListener('dragleave', function(e) {
    e.preventDefault();
    this.style.background = '#f8f9ff';
});

fileLabel.addEventListener('drop', function(e) {
    e.preventDefault();
    this.style.background = '#f8f9ff';
    
    const file = e.dataTransfer.files[0];
    if (file) {
        const fileInput = document.getElementById('fileInput');
        fileInput.files = e.dataTransfer.files;
        handleFileSelect({ target: fileInput });
    }
});