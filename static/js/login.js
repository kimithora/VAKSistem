document.addEventListener("DOMContentLoaded", function () {

    const tokenInput = document.querySelector("#token");
    const toggleToken = document.querySelector("#toggle-token");
    const loginForm = document.querySelector("form");
    const loginButton = loginForm
        ? loginForm.querySelector("button[type='submit']")
        : null;

    if (tokenInput && tokenInput.type !== "password") {
        tokenInput.type = "password";
    }

    if (tokenInput) {
        tokenInput.addEventListener("input", function () {
            const errorMessage = document.querySelector(".error-message");
            if (errorMessage) {
                errorMessage.style.display = "none";
            }
        });
    }

    if (tokenInput && toggleToken) {
        toggleToken.addEventListener("click", function () {
            if (tokenInput.type === "password") {
                tokenInput.type = "text";
                toggleToken.textContent = "Sembunyikan";
                toggleToken.setAttribute("aria-label", "Sembunyikan token");
            } else {
                tokenInput.type = "password";
                toggleToken.textContent = "Tampilkan";
                toggleToken.setAttribute("aria-label", "Tampilkan token");
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            const token = tokenInput ? tokenInput.value.trim() : "";

            if (!token) {
                event.preventDefault();
                if (tokenInput) {
                    tokenInput.focus();
                }
                return;
            }

            if (loginButton) {
                loginButton.disabled = true;
                loginButton.dataset.originalText = loginButton.textContent;
                loginButton.textContent = "Memproses...";
            }
        });
    }
});
