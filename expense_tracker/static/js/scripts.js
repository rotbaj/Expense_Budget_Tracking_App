// scripts.js

// Ensure the script runs after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {

    // ======================
    // 1. Form Validation
    // ======================
    const expenseForm = document.getElementById('expense-form');

    if (expenseForm) {
        expenseForm.addEventListener('submit', function (event) {
            const amount = document.getElementById('id_amount').value;
            const category = document.getElementById('id_category').value;

            if (!amount || amount <= 0) {
                alert('Please enter a valid amount.');
                event.preventDefault();
            }

            if (!category) {
                alert('Please select a category.');
                event.preventDefault();
            }
        });
    }

    // ======================
    // 2. Dynamic Dropdowns
    // ======================
    const categoryDropdown = document.getElementById('id_category');
    const subcategoryDropdown = document.getElementById('id_subcategory');

    if (categoryDropdown && subcategoryDropdown) {
        const subcategories = {
            'Food': ['Groceries', 'Restaurants', 'Snacks'],
            'Transport': ['Fuel', 'Public Transport', 'Maintenance'],
            'Entertainment': ['Movies', 'Concerts', 'Games'],
        };

        categoryDropdown.addEventListener('change', function () {
            const selectedCategory = categoryDropdown.value;
            subcategoryDropdown.innerHTML = '<option value="">Select Subcategory</option>';

            if (selectedCategory && subcategories[selectedCategory]) {
                subcategories[selectedCategory].forEach(function (subcategory) {
                    const option = document.createElement('option');
                    option.value = subcategory;
                    option.textContent = subcategory;
                    subcategoryDropdown.appendChild(option);
                });
            }
        });
    }

    // ======================
    // 3. Real-Time Budget Progress Bar
    // ======================
    const budgetSpentElement = document.getElementById('budget-spent');
    const budgetTotalElement = document.getElementById('budget-total');
    const progressBar = document.getElementById('progress-bar');

    if (budgetSpentElement && budgetTotalElement && progressBar) {
        const budgetSpent = parseFloat(budgetSpentElement.textContent);
        const budgetTotal = parseFloat(budgetTotalElement.textContent);

        if (budgetTotal > 0) {
            const progressPercentage = (budgetSpent / budgetTotal) * 100;
            progressBar.style.width = progressPercentage + '%';

            if (progressPercentage > 100) {
                progressBar.style.backgroundColor = 'red';
            }
        }
    }

    // ======================
    // 4. Interactive Charts (Using Chart.js)
    // ======================
    const ctx = document.getElementById('spendingChart')?.getContext('2d');

    if (ctx) {
        const spendingData = {
            labels: ['Food', 'Transport', 'Entertainment', 'Rent'],
            datasets: [{
                data: [300, 100, 50, 500],
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
            }]
        };

        new Chart(ctx, {
            type: 'pie',
            data: spendingData,
        });
    }

    // ======================
    // 5. Auto-Suggestions for Categories
    // ======================
    const categoryInput = document.getElementById('id_category');

    if (categoryInput) {
        categoryInput.addEventListener('input', function () {
            const inputValue = categoryInput.value.toLowerCase();
            const suggestions = document.getElementById('category-suggestions').options;

            for (let i = 0; i < suggestions.length; i++) {
                if (suggestions[i].value.toLowerCase().startsWith(inputValue)) {
                    categoryInput.value = suggestions[i].value;
                    break;
                }
            }
        });
    }

    // ======================
    // 6. Confirmation Dialogs
    // ======================
    const deleteButtons = document.querySelectorAll('.delete-button');

    deleteButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            if (!confirm('Are you sure you want to delete this item?')) {
                event.preventDefault();
            }
        });
    });

});