const OTPinputs = document.querySelectorAll(".input_field_box input");
const button = document.querySelector("button");

const gatherAndSendOTP = () => {
    let otp = "";
    OTPinputs.forEach(input => {
        if (input.value !== "") {
            otp += input.value;
        }
    });
    
    fetch(`/verify_totp_login/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: otp }),
    })
    .then(response => {
        if (response.ok) {
            // Call a function to update the cart display
            window.location.href = `/catalog/${id}`;
        } else {
            // Handle errors or server responses here
            console.error('Verification error.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

window.addEventListener("load", () => OTPinputs[0].focus());

OTPinputs.forEach((input) => {
    input.addEventListener("input", () => {
        const currentInput = input;
        const nextInput = input.nextElementSibling;

        if (currentInput.value.length > 1 && currentInput.value.length === 2) {
            currentInput.value = "";
        }

        if (nextInput !== null && nextInput.hasAttribute("disabled") && currentInput.value !== "") {
            nextInput.removeAttribute("disabled");
            nextInput.focus();
        }
        
        if (!OTPinputs[3].disabled && OTPinputs[3].value !== "") {
            button.classList.add("active");
        } else {
            button.classList.remove("active");
        }
    });

    input.addEventListener("keyup", (e) => {
        if (e.key === "Backspace") {
            if (input.previousElementSibling !== null) {
                e.target.value = "";
                e.target.setAttribute("disabled", true);
                input.previousElementSibling.focus();
            }
        }
    });
});

button.addEventListener("click", (event) => {
    event.preventDefault(); // Prevent default button behavior

    if (button.classList.contains("active")) {
        console.log("button clicked");
        gatherAndSendOTP();
    }
});
