let isLogin = true;

function toggleAuth() {
    isLogin = !isLogin;
    
    const title = document.getElementById('auth-title');
    const subtitle = document.getElementById('auth-subtitle');
    const form = document.getElementById('auth-form');
    const submitBtn = document.getElementById('submit-btn');
    const toggleText = document.getElementById('toggle-text');
    const toggleLink = document.getElementById('toggle-auth');
    
    const regFields = document.getElementById('register-only-fields');
    const confirmPass = document.getElementById('confirm-password-group');
    const loginOptions = document.getElementById('login-options');

    if (isLogin) {
        title.innerText = "Ласкаво просимо!";
        subtitle.innerText = "Будь ласка, введіть свої дані для входу";
        
        // ВИПРАВЛЕНО: Використовуємо константу з HTML
        form.action = loginUrl; 
        
        submitBtn.innerText = "Увійти";
        toggleText.innerText = "Немає акаунту?";
        toggleLink.innerText = "Створити зараз";
        
        regFields.style.display = "none";
        confirmPass.style.display = "none";
        loginOptions.style.display = "flex";
        
        document.getElementById('username').required = false;
        document.getElementById('password_confirm').required = false;
    } else {
        title.innerText = "Реєстрація";
        subtitle.innerText = "Створіть свій профіль у FastFood";
        
        // ВИПРАВЛЕНО: Використовуємо константу з HTML
        form.action = registerUrl; 
        
        submitBtn.innerText = "Зареєструватися";
        toggleText.innerText = "Вже є акаунт?";
        toggleLink.innerText = "Увійти";
        
        regFields.style.display = "block";
        confirmPass.style.display = "block";
        loginOptions.style.display = "none";

        document.getElementById('username').required = true;
        document.getElementById('password_confirm').required = true;
    }
}