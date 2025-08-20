// Function to get CSRF token from cookies
function getCSRFToken() {
    let cookieValue = null;
    const name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = "https://agrishield-5j83.onrender.com";
    console.log("Auth script loaded");
    
    // Get CSRF token once when the page loads
    const csrftoken = getCSRFToken();
    console.log('CSRF Token:', csrftoken); // Debug log
    
    // Auth Modals Elements
    const loginModal = document.getElementById('loginModal');
    const signupModal = document.getElementById('signupModal');
    const authButton = document.getElementById('authButton');
    const mobileAuthButton = document.getElementById('mobileAuthButton');
    const closeLoginBtn = document.getElementById('closeLogin');
    const closeSignupBtn = document.getElementById('closeSignup');
    const showSignupBtn = document.getElementById('showSignup');
    const showLoginBtn = document.getElementById('showLogin');

    // Forms and User display elements
    const loginForm = document.getElementById("loginForm");
    const signupForm = document.getElementById("signupForm");
    const loginError = document.getElementById("loginError");
    const signupError = document.getElementById("signupError");
    const logoutBtn = document.getElementById("logoutBtn");
    const welcomeBanner = document.getElementById("welcomeBanner");
    const loggedInUserSpan = document.getElementById("loggedInUser");
    const userDashboard = document.getElementById("userDashboard");

    // ---------------- MODAL VISIBILITY ----------------
    function openLoginModal() {
        if (signupModal) signupModal.classList.remove('active');
        if (loginModal) loginModal.classList.add('active');
    }

    function openSignupModal() {
        if (loginModal) loginModal.classList.remove('active');
        if (signupModal) signupModal.classList.add('active');
    }

    function closeModal() {
        if (loginModal) loginModal.classList.remove('active');
        if (signupModal) signupModal.classList.remove('active');
    }

    if (authButton) authButton.addEventListener('click', openLoginModal);
    if (mobileAuthButton) mobileAuthButton.addEventListener('click', openLoginModal);
    if (closeLoginBtn) closeLoginBtn.addEventListener('click', closeModal);
    if (closeSignupBtn) closeSignupBtn.addEventListener('click', closeModal);
    if (showSignupBtn) showSignupBtn.addEventListener('click', openSignupModal);
    if (showLoginBtn) showLoginBtn.addEventListener('click', openLoginModal);

    window.addEventListener('click', (e) => {
        if (e.target === loginModal || e.target === signupModal) {
            closeModal();
        }
    });

    // ---------------- LOGIN ----------------
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            if (loginError) loginError.textContent = "";

            const email = loginForm.loginEmail.value;
            const password = loginForm.loginPassword.value;

            try {
                const res = await fetch(`${API_BASE_URL}/auth/login/`, {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrftoken  // Add CSRF token
                    },
                    body: JSON.stringify({ email, password }),
                });

                const data = await res.json();
                if (!res.ok) {
                    loginError.textContent = data.non_field_errors?.[0] || data.detail || "Invalid credentials.";
                    return;
                }

                localStorage.setItem("authToken", data.key);
                await fetchUserProfile();
                closeModal();
            } catch (err) {
                if (loginError) loginError.textContent = "Something went wrong. Try again.";
                console.error("Login error:", err);
            }
        });
    }

    // ---------------- SIGNUP ----------------
    if (signupForm) {
        signupForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            if (signupError) signupError.textContent = "";

            const username = signupForm.signupName.value;
            const email = signupForm.signupEmail.value;
            const phone_number = signupForm.signupPhone.value;
            const user_type = signupForm.userType.value;
            const password = signupForm.signupPassword.value;
            const password2 = signupForm.signupConfirm.value;
            // The backend expects 'password1' and 'password2' for registration.
            const password1 = password;

            if (password !== password2) {
                if (signupError) signupError.textContent = "Passwords do not match.";
                return;
            }

            try {
                const res = await fetch(`${API_BASE_URL}/auth/registration/`, {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrftoken  // Add CSRF token
                    },
                    body: JSON.stringify({ username, email, phone_number, user_type, password1, password2 }),
                });

                const data = await res.json();
                if (!res.ok) {
                    // Handle various error formats from backend
                    let errorMsg = "Signup failed.";
                    if (data.username) errorMsg = `Username: ${data.username[0]}`;
                    else if (data.email) errorMsg = `Email: ${data.email[0]}`;
                    else if (data.password) errorMsg = `Password: ${data.password[0]}`;
                    else if (data.detail) errorMsg = data.detail;
                    if (signupError) signupError.textContent = errorMsg;
                    return;
                }

                localStorage.setItem("authToken", data.key);
                await fetchUserProfile();
                closeModal();
            } catch (err) {
                if (signupError) signupError.textContent = "Something went wrong. Try again.";
                console.error("Signup error:", err);
            }
        });
    }

    // ---------------- FETCH USER PROFILE ----------------
    async function fetchUserProfile() {
        const token = localStorage.getItem("authToken");
        if (!token) {
            updateUIForLoggedOutUser();
            return;
        }

        try {
            const res = await fetch(`${API_BASE_URL}/auth/user/`, {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Token ${token}`,
                },
            });

            if (res.ok) {
                const user = await res.json();
                updateUIForLoggedInUser(user);
            } else {
                // Token might be invalid/expired
                localStorage.removeItem("authToken");
                updateUIForLoggedOutUser();
            }
        } catch (err) {
            console.error("Failed to fetch user profile:", err);
            updateUIForLoggedOutUser();
        }
    }

    function updateUIForLoggedInUser(user) {
        if (loggedInUserSpan) loggedInUserSpan.textContent = user.username;
        if (welcomeBanner) welcomeBanner.style.display = "block";
        if (userDashboard) userDashboard.style.display = "block";
        if (authButton) authButton.style.display = 'none';
        if (mobileAuthButton) mobileAuthButton.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'inline-block';
    }

    function updateUIForLoggedOutUser() {
        if (welcomeBanner) welcomeBanner.style.display = "none";
        if (userDashboard) userDashboard.style.display = "none";
        if (authButton) authButton.style.display = 'inline-block';
        if (mobileAuthButton) mobileAuthButton.style.display = 'inline-block';
        if (logoutBtn) logoutBtn.style.display = 'none';
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
                        "X-CSRFToken": csrftoken  // Add CSRF token for logout too
                    },
                });
            } catch (err) {
                console.error("Logout failed:", err);
            } finally {
                localStorage.removeItem("authToken");
                updateUIForLoggedOutUser();
                window.location.reload(); // Or redirect to home
            }
        });
    }

    // Auto-fetch user profile on page load
    fetchUserProfile();
});