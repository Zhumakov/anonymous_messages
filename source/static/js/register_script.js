document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');
    const passwordError = document.getElementById('password_error');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращаем отправку формы обычным способом

        if (passwordField.value !== confirmPasswordField.value) {
            passwordError.textContent = 'Пароли не совпадают';
            confirmPasswordField.focus();
            return;
        } else {
            passwordError.textContent = '';
        }

        // Собираем данные формы в объект
        const formData = {
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
        };

        fetch('/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Указываем, что отправляем JSON
            },
            body: JSON.stringify(formData) // Преобразуем объект в JSON-строку
        })
        .then(response => {
            if (response.ok) {
                // Успешная регистрация, перенаправляем на главную страницу
                window.location.href = '/';
            } else {
                // Ошибка при регистрации
                console.error('Ошибка при регистрации:', response.status);
                // Можно получить текст ошибки из response.text() или response.json() и показать пользователю
                response.text().then(text => {
                    console.error("Ошибка:", text);
                    // Добавь код для отображения ошибки на странице
                });
            }
        })
        .catch(error => {
            console.error('Ошибка сети:', error);
            // Обработать ошибку сети и показать сообщение пользователю
        });
    });
});
