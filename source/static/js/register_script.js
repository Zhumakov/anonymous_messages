function displayError(message) {
    const errorElement = document.getElementById('error_block');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    } else {
        alert(message);
    }
}


document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');


    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращаем отправку формы обычным способом

        if (passwordField.value !== confirmPasswordField.value) {
            displayError('Пароли не совпадают')
            confirmPasswordField.focus();
            return;
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
                    fetch('/api/users/auth', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json' // Указываем, что отправляем JSON
                        },
                        body: JSON.stringify(formData) // Преобразуем объект в JSON-строку
                    })
                    window.location.href = '/';
                } else {
                    console.error('Ошибка при регистрации', response.status);
                    switch (response.status) {
                        case 400:
                            response.text().then(errorMessage => {
                                console.error(errorMessage);
                                displayError('Не удалось зарегестрировать пользователя');
                            });
                            break;
                        case 409:
                            response.text().then(errorMessage => {
                                console.error(errorMessage);
                                displayError('Пользователь с таким именем или электронной почтой уже существует');
                            });
                            break;
                        case 422:
                            response.text().then(errorMessage => {
                                console.error(errorMessage);
                                displayError('Данные не допустимы');
                            });
                            break;
                        default:
                            response.text().then(errorMessage => {
                                console.error(errorMessage);
                                displayError('Произошла ошибка');
                            });
                            break;
                    }
                }
            })
            .catch(error => {
                console.error('Ошибка сети:', error);
                displayError('Ошибка сети: проверьте подключение');
            });
    });
});
