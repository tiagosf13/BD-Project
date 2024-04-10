function validateLowercase(inputElement) {
    // Get the user's input
    const inputValue = inputElement.value;

    // Convert the input to lowercase
    const lowercaseValue = inputValue.toLowerCase();

    // Check if the input matches the lowercase version; if not, update the input field
    if (inputValue !== lowercaseValue) {
        inputElement.value = lowercaseValue;
    }
}

function checkPasswordCriteria() {
    var password = document.getElementById("password").value;
    var confirm_password = document.getElementById("confirm_password").value;

    // Make an AJAX request to Flask route for breach verification
    fetch('/verify-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password : confirm_password })
    })
    .then(response => response.json())
    .then(data => {
        const breached = data.breached;

        // Remove leading and trailing spaces, and replace consecutive spaces with a single space
        const processedPassword = password.trim().replace(/\s+/g, ' ');
        const combinedPasswordLength = processedPassword.length;

        let criteria = {
            length: combinedPasswordLength >= 12 && combinedPasswordLength <= 128,
            uppercase: /[A-Z]/u.test(password),
            lowercase: /[a-z]/u.test(password),
            digit: /[0-9]/.test(password),
            special: /[\s\S]/u.test(password),
            match: confirm_password !== "" && password === confirm_password,
            breach_check: !breached && confirm_password !== "" && password === confirm_password
        };

        // Update the UI to reflect satisfied/unsatisfied criteria
        for (let criterion in criteria) {
            const criteriaElement = document.getElementById(`criteria-${criterion}`);
            if (criteria[criterion]) {
                criteriaElement.classList.add('satisfied');
            } else {
                criteriaElement.classList.remove('satisfied');
            }
        }

        // Check if all criteria are met
        const allCriteriaMet = Object.values(criteria).every(criterion => criterion);

        // Enable/disable sign-up button based on criteria
        const signUpButton = document.getElementById('savebtn');
        if (allCriteriaMet) {
            signUpButton.removeAttribute('disabled');
        } else {
            signUpButton.setAttribute('disabled', true);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle errors if any
    });
}





