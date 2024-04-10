function printCodes() {
    // Print the codes board
    window.print();
    showContinueButton();
}

function copyAllCodes() {
    // Get all code elements from the board
    const codeElements = document.querySelectorAll('.code');

    // Create an array to store codes
    const codesArray = [];

    // Extract codes from elements and add them to the array
    codeElements.forEach(codeElement => {
        codesArray.push(codeElement.textContent.trim());
    });

    // Join codes with newline for better formatting
    const codesString = codesArray.join('\n');

    // Copy codes string to clipboard
    const el = document.createElement('textarea');
    el.value = codesString;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    alert('Codes copied to clipboard!');
    showContinueButton();
}


function showContinueButton() {
    const continueButton = document.querySelector('.continue-button');
    continueButton.style.display = 'block';
}

function redirectLogin() {
    // Redirect to the login page
    window.location.href = '/login';
}

function redirectProfile(username) {
    // Redirect to the login page
    window.location.href = `/profile/${username}`;
}

// Function to fetch and populate codes from Flask route
async function fetchCodes() {
    const response = await fetch(`/get_codes/${id}`); // Replace {{ id }} with the actual ID
    const data = await response.json();

    const codesBoard = document.getElementById('codes-board');

    // Accessing the inner 'codes' object
    const codesData = data.codes;

    // Populate the board with fetched codes and their validity status
    let count = 0;
    let currentColumn = null;

    for (const code in codesData) {
        if (Object.hasOwnProperty.call(codesData, code)) {
            if (count % 5 === 0) {
                // Create a new column after every 5 codes
                currentColumn = document.createElement('div');
                currentColumn.classList.add('column');
                codesBoard.appendChild(currentColumn);
            }

            const codeElement = document.createElement('div');
            codeElement.classList.add('code');
            codeElement.textContent = code;
            currentColumn.appendChild(codeElement);

            count++;
        }
    }
}