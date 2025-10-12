const form = document.getElementById('studentForm');
const messageDiv = document.getElementById('message');
const submitBtn = document.getElementById('submitBtn');
const yearSelect = document.getElementById('yearSelect');
const yearCustom = document.getElementById('yearCustom');

// Backend API URL (AWS Lambda)
const API_URL = 'https://qkfsddvd8j.execute-api.us-east-1.amazonaws.com/production';

// Security: API Key (configured via environment or build process)
// IMPORTANT: In production, inject this via a build script, not hardcoded
const API_KEY = window.WMU_API_KEY || 'YOUR_API_KEY_HERE';

// Toggle between dropdown and custom input for year
function toggleYearInput() {
    if (yearSelect.value === 'custom') {
        yearCustom.style.display = 'block';
        yearCustom.required = true;
        yearCustom.value = '';
    } else {
        yearCustom.style.display = 'none';
        yearCustom.required = false;
        yearCustom.value = yearSelect.value;
    }
}

// Auto-capitalize yearCustom input
yearCustom.addEventListener('input', function() {
    this.value = this.value.toUpperCase();
});

// Initialize year field on page load
toggleYearInput();

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Disable button and show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner"></span> Submitting...';

    const formData = new FormData(form);

    // Make sure year is set correctly
    if (yearSelect.value !== 'custom') {
        formData.set('year', yearSelect.value);
    }

    try {
        const response = await fetch(`${API_URL}/submit`, {
            method: 'POST',
            headers: {
                'X-API-Key': API_KEY
            },
            body: formData
        });

        const result = await response.json();

        // Show message
        messageDiv.className = 'message show';

        if (result.status === 'added') {
            messageDiv.classList.add('success');
            messageDiv.textContent = result.message;
            form.reset(); // Clear form for new entry
            // Restore default university value
            document.getElementById('university').value = 'Western Michigan University';
            toggleYearInput(); // Reset year field
        } else if (result.status === 'updated') {
            messageDiv.classList.add('updated');
            messageDiv.textContent = result.message;
        } else {
            messageDiv.classList.add('error');
            messageDiv.textContent = result.message;
        }

        // Hide message after 5 seconds
        setTimeout(() => {
            messageDiv.className = 'message';
        }, 5000);

    } catch (error) {
        messageDiv.className = 'message show error';
        messageDiv.textContent = 'An error occurred. Please try again.';
        console.error('Error:', error);
    } finally {
        // Re-enable button
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit';
    }
});