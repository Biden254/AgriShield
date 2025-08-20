const API_BASE_URL = "https://agrishield-5j83.onrender.com";

// Elements
const loginForm = document.getElementById("login-form");
const signupForm = document.getElementById("signup-form");
const loginError = document.getElementById("login-error");
const signupError = document.getElementById("signup-error");
const logoutBtn = document.getElementById("logout-btn");
const usernameSpan = document.getElementById("username");
const dashboardSection = document.getElementById("dashboard");

// ---------------- LOGIN ----------------
if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        loginError.textContent = "";

        const email = loginForm.email.value;
        const password = loginForm.password.value;

        try {
            const res = await fetch(`${API_BASE_URL}/auth/login/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            if (!res.ok) {
                const data = await res.json();
                loginError.textContent = data.non_field_errors || "Invalid credentials.";
                return;
            }

            const data = await res.json();
            localStorage.setItem("authToken", data.key);
            fetchUserProfile();
        } catch (err) {
            loginError.textContent = "Something went wrong. Try again.";
        }
    });
}

// ---------------- SIGNUP ----------------
if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        signupError.textContent = "";

        const username = signupForm.username.value;
        const email = signupForm.email.value;
        const password1 = signupForm.password1.value;
        const password2 = signupForm.password2.value;

        try {
            const res = await fetch(`${API_BASE_URL}/auth/registration/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, email, password1, password2 }),
            });

            if (!res.ok) {
                const data = await res.json();
                signupError.textContent = data.detail || "Signup failed.";
                return;
            }

            const data = await res.json();
            localStorage.setItem("authToken", data.key);
            fetchUserProfile();
        } catch (err) {
            signupError.textContent = "Something went wrong. Try again.";
        }
    });
}

// ---------------- FETCH USER PROFILE ----------------
async function fetchUserProfile() {
    const token = localStorage.getItem("authToken");
    if (!token) return;

    try {
        const res = await fetch(`${API_BASE_URL}/auth/user/`, {
            headers: {
                "Content-Type": "application/json",
                Authorization: `Token ${token}`,
            },
        });

        if (res.ok) {
            const data = await res.json();
            usernameSpan.textContent = data.username;
            dashboardSection.style.display = "block";
            logoutBtn.style.display = "inline";
        }
    } catch (err) {
        console.error("Failed to fetch user profile:", err);
    }
}

// ---------------- LOGOUT ----------------
if (logoutBtn) {
    logoutBtn.addEventListener("click", async (e) => {
        e.preventDefault();

        const token = localStorage.getItem("authToken");
        if (!token) return;

        try {
            await fetch(`${API_BASE_URL}/auth/logout/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Token ${token}`,
                },
            });
        } catch (err) {
            console.error("Logout failed:", err);
        } finally {
            localStorage.removeItem("authToken");
            window.location.reload();
        }
    });
}

// Auto-fetch user profile on page load
fetchUserProfile();
