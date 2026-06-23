// Authentication helper functions

function initializeNavigation() {
    checkAuthState();
    
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    }
}

function checkAuthState() {
    const token = localStorage.getItem('access_token');
    const authNav = document.getElementById('authNav');
    const userNav = document.getElementById('userNav');
    const logoutNav = document.getElementById('logoutNav');
    
    if (authNav && userNav && logoutNav) {
        if (token) {
            authNav.style.display = 'none';
            userNav.style.display = 'block';
            logoutNav.style.display = 'block';
        } else {
            authNav.style.display = 'block';
            userNav.style.display = 'none';
            logoutNav.style.display = 'none';
        }
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');
    window.location.href = '/';
}

function getAuthHeader() {
    const token = localStorage.getItem('access_token');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
}

document.addEventListener('DOMContentLoaded', initializeNavigation);
