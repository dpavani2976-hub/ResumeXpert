/* =====================================
        ResumeXpert Authentication JS
====================================== */



/* ---------- Show / Hide Password ---------- */
/* =====================================
        ResumeXpert Authentication JS
====================================== */


/* ---------- Show / Hide Password ---------- */

const password = document.getElementById("password");
const togglePassword = document.getElementById("togglePassword");

if (password && togglePassword) {

    togglePassword.onclick = () => {

        if (password.type === "password") {

            password.type = "text";
            togglePassword.innerHTML = "Hide";

        } else {

            password.type = "password";
            togglePassword.innerHTML = "Show";

        }

    };

}


/* ---------- Confirm Password ---------- */

const confirmPassword =
    document.getElementById("confirmPassword");

const toggleConfirm =
    document.getElementById("toggleConfirm");

if (confirmPassword && toggleConfirm) {

    toggleConfirm.onclick = () => {

        if (confirmPassword.type === "password") {

            confirmPassword.type = "text";
            toggleConfirm.innerHTML = "Hide";

        } else {

            confirmPassword.type = "password";
            toggleConfirm.innerHTML = "Show";

        }

    };

}