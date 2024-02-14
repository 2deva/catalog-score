
function toggleView() {
    // Toggle visibility of tile view
    var tileView = document.querySelectorAll('.product-tile');
    tileView.forEach(tile => tile.classList.toggle('hidden'));

    // Toggle visibility of list view
    var listView = document.getElementById('product-list');
    listView.classList.toggle('hidden');
}
// Function to display a collection
function displayCollection(collectionName) {
    // Code to display the collection
    console.log('Displaying collection:', collectionName);
}

// Fetch collection names and populate the select element
fetch('/get_collections')
    .then(response => response.json())
    .then(data => {
        const selectElement = document.getElementById('collection_name');
        // Clear any existing options
        selectElement.innerHTML = '<option value="" selected>Select Catalog</option>'; // Empty option
        // Populate options with collection names
        data.forEach(collection => {
            const option = document.createElement('option');
            option.value = collection;
            option.textContent = collection;
            selectElement.appendChild(option);
        });

        // Listen for changes to the selected option
        selectElement.addEventListener('change', function() {
            // Get the selected collection name
            var collectionName = this.value;

            // If a collection is selected, display it
            if (collectionName) {
                displayCollection(collectionName);
            }
        });
    })
    .catch(error => console.error('Error fetching collection names:', error));
// Listen for changes to the selected option
document.getElementById('collection_name').addEventListener('change', function() {
    // Get the selected collection name
    var collectionName = this.value;

    // If a collection is selected, display it
    if (collectionName) {
        displayCollection(collectionName);

        // Store the current collection name in the local storage
        localStorage.setItem('currentCollection', collectionName);

        // Update the current collection
        document.getElementById('current-collection').textContent = collectionName;
    }
});
// Display the current collection name when the page loads
window.addEventListener('DOMContentLoaded', (event) => {
    var currentCollection = localStorage.getItem('currentCollection');
    if (currentCollection) {
        document.getElementById('current-collection').textContent = currentCollection;
    }
});

// Select the <select> element
const selectElement = document.getElementById('collection_name');

// Add event listener for the 'change' event
selectElement.addEventListener('change', function() {
    // Get the form element
    const form = document.getElementById('catalogs-form');
    
    // Submit the form
    form.submit();
});

// Function to show product details in modal
function showProductDetails(productId, collectionName) {
    // Fetch product details from the database using AJAX
    fetch(`/get_product_details?id=${productId}&collection_name=${collectionName}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data); // Log the response data to the console
            // Check if data is valid
            if (data && data.product_details) {
                // Display product details in modal
                var modal = document.getElementById('product-modal');
                var modalContent = document.getElementById('product-details-content');
                modalContent.innerHTML = '<h2>Product Details</h2>';

                // Loop through product_details object and display each detail
                Object.keys(data.product_details).forEach(key => {
                    modalContent.innerHTML += '<p><strong>' + key + ':</strong> ' + data.product_details[key] + '</p>';
                });

                modal.style.display = 'block'; // Display modal
            } else {
                throw new Error('Invalid data received from server');
            }
        })
        .catch(error => console.error('Error fetching product details:', error));
}

// Function to close the product modal
function closeProductModal() {
    var modal = document.getElementById('product-modal');
    modal.style.display = 'none'; // Hide modal
  }




// JavaScript code in catalog.js
// Function to fetch aggregate scores for the current collection
function fetchAggregateScores() {
    // Get the current collection name from local storage
    const currentCollection = localStorage.getItem('currentCollection');

    // If a current collection is stored in local storage, fetch its aggregate scores
    if (currentCollection) {
        fetch(`/get_aggregate_scores?collection_name=${currentCollection}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Once data is fetched, display the pie chart
                displayCircles(data);
            })
            .catch(error => console.error('Error fetching aggregate scores:', error));
    } else {
        console.error('Current collection not found in local storage.');
    }
}

function displayCircles(data) {
    console.log('Data received:', data);

    if (data && data.aggregate_scores) {
        const aggregateScores = data.aggregate_scores;
        const completenessPercentage = aggregateScores.average_completeness_score;
        const correctnessPercentage = aggregateScores.average_correctness_score;
        const compliancePercentage = aggregateScores.average_compliance_score;

        const circleContainer = document.getElementById('circle-container');
        circleContainer.innerHTML = '';

        const getColorClass = (percentage) => {
            if (percentage >= 70) {
                return 'green';
            } else if (percentage >= 40) {
                return 'yellow';
            } else {
                return 'red';
            }
        };

        const createCircle = (percentage, colorClass, name) => {
            const circle = document.createElement('div');
            circle.classList.add('circle', colorClass);

            const percentageText = document.createElement('div');
            percentageText.classList.add('percentage');
            const roundedPercentage = Math.round(percentage);
            percentageText.textContent = `${roundedPercentage}%`;

            const nameText = document.createElement('div');
            nameText.classList.add('name');
            nameText.textContent = name;

            circle.appendChild(percentageText);
            circle.appendChild(nameText);

            return circle;
        };

        const completenessCircle = createCircle(completenessPercentage, getColorClass(completenessPercentage), 'Completeness');
        const correctnessCircle = createCircle(correctnessPercentage, getColorClass(correctnessPercentage), 'Correctness');
        const complianceCircle = createCircle(compliancePercentage, getColorClass(compliancePercentage), 'Compliance');

        circleContainer.appendChild(completenessCircle);
        circleContainer.appendChild(correctnessCircle);
        circleContainer.appendChild(complianceCircle);

        document.getElementById('aggregate-scores-modal').style.display = 'block';
    } else {
        console.error('Invalid data received:', data);
    }
}
// Function to close the modal
function closeModal() {
    var modal = document.getElementById('aggregate-scores-modal');
    modal.style.display = 'none';
}



