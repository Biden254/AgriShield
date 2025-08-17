// Authentication functionality
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const loginModal = document.getElementById('loginModal');
    const signupModal = document.getElementById('signupModal');
    const authButton = document.getElementById('authButton');
    const mobileAuthButton = document.getElementById('mobileAuthButton');
    const showLogin = document.getElementById('showLogin');
    const showSignup = document.getElementById('showSignup');
    const closeLogin = document.getElementById('closeLogin');
    const closeSignup = document.getElementById('closeSignup');
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const userDashboard = document.getElementById('userDashboard');
    const userGreeting = document.getElementById('userGreeting');
    const userReports = document.getElementById('userReports');
    const userAlerts = document.getElementById('userAlerts');
    const userImpact = document.getElementById('userImpact');
    const quickReportBtn = document.getElementById('quickReportBtn');
    const viewHistoryBtn = document.getElementById('viewHistoryBtn');

    // Demo user data (replace with real auth in production)
    let currentUser = null;

    // Show/hide modals
    function showModal(modal) {
        document.querySelectorAll('.auth-modal').forEach(m => m.classList.remove('active'));
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function hideModals() {
        document.querySelectorAll('.auth-modal').forEach(m => m.classList.remove('active'));
        document.body.style.overflow = '';
    }

    // Event listeners
    authButton.addEventListener('click', () => currentUser ? logout() : showModal(loginModal));
    mobileAuthButton.addEventListener('click', () => currentUser ? logout() : showModal(loginModal));
    showLogin.addEventListener('click', () => showModal(loginModal));
    showSignup.addEventListener('click', () => showModal(signupModal));
    closeLogin.addEventListener('click', hideModals);
    closeSignup.addEventListener('click', hideModals);

    // Close modals when clicking outside
    document.querySelectorAll('.auth-modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) hideModals();
        });
    });

    // Login form submission
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        
        // Demo authentication - replace with real API call
        if (email && password) {
            currentUser = {
                name: email.split('@')[0],
                email: email,
                type: "farmer",
                reports: 5,
                alerts: 12,
                impact: 8
            };
            updateAuthUI();
            hideModals();
            showToast('Login successful!');
        } else {
            showToast('Please enter both email and password', 'error');
        }
    });

    // Signup form submission
    signupForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const name = document.getElementById('signupName').value;
        const email = document.getElementById('signupEmail').value;
        const phone = document.getElementById('signupPhone').value;
        const password = document.getElementById('signupPassword').value;
        const confirm = document.getElementById('signupConfirm').value;
        const userType = document.getElementById('userType').value;
        
        // Basic validation
        if (password !== confirm) {
            showToast('Passwords do not match', 'error');
            return;
        }
        
        if (name && email && phone && password) {
            currentUser = {
                name: name,
                email: email,
                phone: phone,
                type: userType,
                reports: 0,
                alerts: 0,
                impact: 0
            };
            updateAuthUI();
            hideModals();
            showToast('Account created successfully!');
        } else {
            showToast('Please fill all fields', 'error');
        }
    });

    // Update UI based on auth state
    function updateAuthUI() {
        if (currentUser) {
            // User is logged in
            authButton.innerHTML = `
                <div class="user-profile">
                    <div class="user-avatar">${currentUser.name.charAt(0)}</div>
                    <span class="user-name">${currentUser.name.split(' ')[0]}</span>
                </div>
            `;
            mobileAuthButton.innerHTML = `
                <span>${currentUser.name.split(' ')[0]}</span>
            `;
            
            // Show user dashboard
            userDashboard.style.display = 'block';
            userGreeting.textContent = currentUser.name;
            userReports.textContent = currentUser.reports;
            userAlerts.textContent = currentUser.alerts;
            userImpact.textContent = currentUser.impact;
            
            // Update translations for new elements
            updateLanguage(currentLanguage);
        } else {
            // User is logged out
            authButton.innerHTML = '<span data-i18n="auth.login">Login</span>';
            mobileAuthButton.innerHTML = '<span data-i18n="auth.login">Login</span>';
            userDashboard.style.display = 'none';
        }
    }

    // Logout function
    function logout() {
        currentUser = null;
        updateAuthUI();
        showToast('Logged out successfully');
    }

    // Show toast notifications
    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => {
                    document.body.removeChild(toast);
                }, 300);
            }, 3000);
        }, 100);
    }

    // Quick report button
    quickReportBtn.addEventListener('click', function() {
        document.getElementById('report').scrollIntoView({ behavior: 'smooth' });
    });

    // View history button
    viewHistoryBtn.addEventListener('click', function() {
        showToast('History feature coming soon!');
    });

    // Initialize
    updateAuthUI();
});

// Add to language.js translations
const authTranslations = {
    en: {
        'auth.login_title': 'Login to AgriShield',
        'auth.signup_title': 'Create Account',
        'auth.email': 'Email',
        'auth.password': 'Password',
        'auth.confirm_password': 'Confirm Password',
        'auth.full_name': 'Full Name',
        'auth.phone': 'Phone Number',
        'auth.user_type': 'I am a:',
        'auth.farmer': 'Farmer',
        'auth.fisher': 'Fisher',
        'auth.official': 'Government Official',
        'auth.login': 'Login',
        'auth.signup': 'Sign Up',
        'auth.logout': 'Logout',
        'auth.no_account': "Don't have an account?",
        'auth.have_account': 'Already have an account?',
        'user.welcome': 'Welcome back,',
        'user.reports_submitted': 'Reports Submitted',
        'user.alerts_received': 'Alerts Received',
        'user.community_impact': 'Community Impact',
        'user.quick_report': 'Quick Report',
        'user.view_history': 'View History'
    },
    sw: {
        'auth.login_title': 'Ingia kwenye AgriShield',
        'auth.signup_title': 'Tengeneza Akaunti',
        'auth.email': 'Barua Pepe',
        'auth.password': 'Nenosiri',
        'auth.confirm_password': 'Thibitisha Nenosiri',
        'auth.full_name': 'Jina Kamili',
        'auth.phone': 'Nambari ya Simu',
        'auth.user_type': 'Mimi ni:',
        'auth.farmer': 'Mkulima',
        'auth.fisher': 'Mvuvi',
        'auth.official': 'Afisa Serikali',
        'auth.login': 'Ingia',
        'auth.signup': 'Jisajili',
        'auth.logout': 'Ondoka',
        'auth.no_account': "Huna akaunti?",
        'auth.have_account': 'Tayari una akaunti?',
        'user.welcome': 'Karibu tena,',
        'user.reports_submitted': 'Ripoti Zilizowasilishwa',
        'user.alerts_received': 'Taadhari Zilizopokelewa',
        'user.community_impact': 'Athari ya Jamii',
        'user.quick_report': 'Ripoti Haraka',
        'user.view_history': 'Tazama Historia'
    }
};

// Merge with existing translations
Object.keys(authTranslations.en).forEach(key => {
    translations.en[key] = authTranslations.en[key];
    translations.sw[key] = authTranslations.sw[key];
});