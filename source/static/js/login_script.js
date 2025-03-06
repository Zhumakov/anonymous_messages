document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращаем отправку формы обычным способом


        // Собираем данные формы в объект
        const formData = {
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
        };

        fetch('/api/users/auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Указываем, что отправляем JSON
            },
            body: JSON.stringify(formData) // Преобразуем объект в JSON-строку
        })
        .then(response => {
            if (response.ok) {
                // Успешная авторизация, перенаправляем на главную страницу
                window.location.href = '/';
            } else {
                response.text().then(text => {
                    console.error("Ошибка:", text);
                });
            }
        })
        .catch(error => {
            console.error('Ошибка сети:', error);
            // Обработать ошибку сети и показать сообщение пользователю
        });
    });
});
