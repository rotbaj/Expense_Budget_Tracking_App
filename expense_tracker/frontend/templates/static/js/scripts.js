// Document Ready Function
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Auto-format currency inputs
    document.querySelectorAll('.currency-input').forEach(function(input) {
        input.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (!isNaN(value)) {
                this.value = value.toFixed(2);
            }
        });
    });

    // Date picker initialization
    document.querySelectorAll('.date-picker').forEach(function(input) {
        input.type = 'date';
        if (!input.value) {
            const today = new Date().toISOString().split('T')[0];
            input.value = today;
        }
    });

    // Confirm before delete actions
    document.querySelectorAll('.confirm-delete').forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Toggle dark mode (optional)
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });

        // Check for saved preference
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
        }
    }

    // Dynamic chart resizing
    window.addEventListener('resize', function() {
        document.querySelectorAll('.chartjs-size-monitor').forEach(function(chart) {
            chart.chart.resize();
        });
    });

    // Auto-focus on first input in forms
    document.querySelectorAll('form').forEach(function(form) {
        const firstInput = form.querySelector('input[type="text"], input[type="email"], input[type="password"], input[type="number"], select, textarea');
        if (firstInput) {
            firstInput.focus();
        }
    });

    // Flash message auto-dismiss
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Budget progress bar animation
    document.querySelectorAll('.progress-bar').forEach(function(bar) {
        const width = bar.style.width;
        bar.style.width = '0';
        setTimeout(function() {
            bar.style.width = width;
        }, 300);
    });

    // Profile picture preview
    const profilePictureInput = document.getElementById('profilePictureInput');
    if (profilePictureInput) {
        profilePictureInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    document.getElementById('profilePicturePreview').src = event.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }
});

// API Helper Functions
const api = {
    get: async function(url) {
        const response = await fetch(url);
        return await response.json();
    },
    post: async function(url, data) {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    },
    delete: async function(url) {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        return await response.json();
    }
};

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Date formatting
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Initialize all charts on page
function initializeCharts() {
    document.querySelectorAll('[data-chart]').forEach(function(element) {
        const chartData = JSON.parse(element.dataset.chart);
        const ctx = element.getContext('2d');
        new Chart(ctx, chartData);
    });
}

// Call initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeCharts);