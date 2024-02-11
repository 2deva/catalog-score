document.getElementById('single-product-score-button').addEventListener('click', function() {
    // Hide all buttons
    document.getElementById('buttons-container').style.display = 'none';

    // Show the form
    document.getElementById('form-box').style.display = 'block';
});

document.getElementById('collect-catalog-button').addEventListener('click', function() {
    // Hide all buttons
    document.getElementById('buttons-container').style.display = 'none';

    // Show the form
    document.getElementById('form-box2').style.display = 'block';
});
document.getElementById('catalog-score-button').addEventListener('click', function() {
    // Hide all buttons
    document.getElementById('buttons-container').style.display = 'none';

    // Show the form
    document.getElementById('form-box3').style.display = 'block';
});

function closeForm() {
            // Show all buttons
            document.getElementById('buttons-container').style.display = 'block';

            // Hide the form
            document.getElementById('form-box').style.display = 'none';
            document.getElementById('form-box2').style.display = 'none';
            document.getElementById('form-box3').style.display = 'none';
        }

// Fetch collection names and populate the select element
fetch('/get_collections')
    .then(response => response.json())
    .then(data => {
        const selectElement = document.getElementById('collection_name');
        // Clear any existing options
        selectElement.innerHTML = '';
        // Populate options with collection names
        data.forEach(collection => {
            const option = document.createElement('option');
            option.value = collection;
            option.textContent = collection;
            selectElement.appendChild(option);
        });
    })
    .catch(error => console.error('Error fetching collection names:', error));

const element = document.querySelector('.some-selector');
if (element) {
    // Access properties or perform actions on the element
    element.classList.add('some-class');
}

document.getElementById('single-product-score-form').addEventListener('submit', function(event) {
    var productUrl = document.getElementById('product_url').value;
    if (!productUrl || !productUrl.startsWith('https://ondc.meesho.org/')) {
        event.preventDefault();
        var errorMessage = document.getElementById('error-message');
        errorMessage.classList.add('active');
        setTimeout(function() {
            errorMessage.classList.remove('active');
        }, 3000);  // Hide the error message after 5 seconds
    }
});

document.getElementById('scrape-catalog-form').addEventListener('submit', function(event) {
    // Prevent default form submission
    event.preventDefault();

    // Fetch catalog URL from form
    var catalogUrl = document.getElementById('catalog_url').value;

    // Validate catalog URL (replace with actual validation logic if needed)
    if (!catalogUrl || !catalogUrl.startsWith('https://ondc.meesho.org/')) {
        // Display error message if URL is invalid
        var errorMessage = document.getElementById('error-message2');
        errorMessage.classList.add('active');
        setTimeout(function() {
            errorMessage.classList.remove('active');
        }, 5000);  // Hide the error message after 5 seconds
    } else {
        // Hide form elements
        document.getElementById('scrape-catalog-form').style.display = 'none';
        document.getElementById('error-message2').style.display = 'none';

        // Show loading animation
        document.getElementById('loading-animation').style.display = 'block';

        // Submit form data asynchronously
        fetch('/scrape', {
            method: 'POST',
            body: new FormData(this)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Display success message with transition effect
                var successMessage = document.createElement('div');
                successMessage.textContent = data.message;
                successMessage.classList.add('success-message');
                // Inside the fetch `.then` block after the success message is displayed
                document.querySelector('.loader span').textContent = 'Scraping successful';

                setTimeout(function() {
                    successMessage.classList.add('active');
                }, 1000);  // Delay to allow for the DOM to update

                // Redirect to next page after scraping is completed
                setTimeout(function() {
                    window.location.href = '/';
                }, 2000);  // Show loading animation for 2 seconds before redirecting
            } else {
                // Handle error response
                console.error('Error:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error.message);
        });
    }
});
