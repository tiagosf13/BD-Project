function previewImage() {
    var preview = document.querySelector('.preview-image');
    var file = document.querySelector('input[type=file]').files[0];
    var reader = new FileReader();

    reader.addEventListener("load", function () {
        preview.src = reader.result;
        preview.style.display = 'block'; // display the preview image after loading it
    }, false);

    if (file) {
        reader.readAsDataURL(file);
    }
}

function validateForm() {

    // Check if all criteria are met
    const allCriteriaMet = Object.values(criteria).every(criterion => criterion);

    // Enable/disable sign-up button based on criteria
    const signUpButton = document.getElementById('signup-button');
    if (allCriteriaMet) {
        signUpButton.removeAttribute('disabled');
    } else {
        signUpButton.setAttribute('disabled', true);
    }

    var username = document.getElementById("username").value;
    var usernameExists = false;  // flag to indicate whether username exists
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            if (response.exists) {
                document.getElementById("error-message-username").innerHTML = "Username already exists.";
                usernameExists = true;  // set flag to true
            }
        }
    };
    xhr.open("POST", "/check_username", false);  // make request synchronous
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("username=" + encodeURIComponent(username));

    if (usernameExists) {
        return false;  // don't submit form if username exists
    }
    

    var email = document.getElementById("email").value;
    var emailExists = false;  // flag to indicate whether username exists
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            if (response.exists) {
                document.getElementById("error-message-email").innerHTML = "Email already exists.";
                emailExists = true;  // set flag to true
            }
        }
    };
    xhr.open("POST", "/check_email", false);  // make request synchronous
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("email=" + encodeURIComponent(email));

    if (emailExists) {
        return false;  // don't submit form if username exists
    }
    
    return true;  // submit form if username doesn't exist
}

function checkPasswordCriteria() {
    var password = document.getElementById("psw").value;
    var confirm_password = document.getElementById("psw-repeat").value;

    // Make an AJAX request to Flask route for breach verification
    fetch('/verify-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password: confirm_password })
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
            breach_check: !breached
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



function goToCatalogPage(id) {
    // Redirect to the profile page without the space character
    window.location.href = '/catalog/' + id;
}



// Function to generate new emergency codes and display in a pop-up
function generateEmergencyCodes() {
    // Here, implement the logic to generate new codes
    // This can be a call to your backend or some JavaScript code to generate new codes

    // Sample codes for demonstration (replace with your actual logic)
    const newCodes = [
        'Code1', 'Code2', 'Code3', 'Code4', 'Code5', // Example codes
        'Code6', 'Code7', 'Code8', 'Code9', 'Code10' // Example codes
    ];

    // Create a table to display the new codes in a pop-up
    let tableContent = '<table border="1">';
    for (let i = 0; i < newCodes.length; i++) {
        tableContent += `<tr><td>${newCodes[i]}</td></tr>`;
    }
    tableContent += '</table>';

    // Open a pop-up window to display the table of new codes
    const popup = window.open('', '_blank', 'width=600,height=400');
    popup.document.write(tableContent);
}