function displayError(message) {
  const errorElement = document.getElementById("error_block");
  if (errorElement) {
    errorElement.textContent = message;
    errorElement.style.display = "block";
  } else {
    alert(message);
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("registerForm");

  form.addEventListener("submit", function (event) {
    event.preventDefault(); // Предотвращаем отправку формы обычным способом

    // Собираем данные формы в объект
    const formData = {
      email: document.getElementById("email").value,
      password: document.getElementById("password").value,
    };

    fetch("/api/users/auth", {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // Указываем, что отправляем JSON
      },
      body: JSON.stringify(formData), // Преобразуем объект в JSON-строку
    })
      .then((response) => {
        if (response.ok) {
          // Успешный вход, перенаправляем на главную страницу
          window.location.href = "/";
        } else {
          console.error("Ошибка при входе", response.status);
          switch (response.status) {
            case 400:
              response.text().then((errorMessage) => {
                console.error(errorMessage);
                displayError("Не удалось войти");
              });
              break;
            case 403:
              response.text().then((errorMessage) => {
                console.error(errorMessage);
                displayError("Неверная электронная почта или пароль");
              });
              break;
            default:
              response.text().then((errorMessage) => {
                console.error(errorMessage);
                displayError("Произошла ошибка");
              });
              break;
          }
        }
      })
      .catch((error) => {
        console.error("Ошибка сети:", error);
        displayError("Ошибка сети: проверьте подключение");
      });
  });
});
