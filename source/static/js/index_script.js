async function attemptAuthorization() {
  const response = await fetch('/api/users/auth/tokens');
  if (response.ok) {
    return true
  } else {
    return false
  };
}


async function GetAuthorizedUser() {
  const response = await fetch('/api/users');

  if (response.ok) {
    const userData = await response.json();
    return userData;
  } else {
    switch (response.status) {
      case 401:
        const success = await attemptAuthorization();
        if (success) {
          // Авторизация прошла успешно, повторяем запрос
          return await GetAuthorizedUser();
        } else {
          window.location.href = '/login';
        }
        break;
      default:
        return null;
    }
  }
}


document.addEventListener('DOMContentLoaded', async function() {
  const tabButtons = document.querySelectorAll('.tab-button');
  const messageContainer = document.getElementById('message-container');

  const userAvatar = document.getElementById('profile-avatar');
  const username = document.getElementById('username');
  const userUID = document.getElementById('user-uid');
  const email = document.getElementById('email');

  const userInfo = await GetAuthorizedUser();
  if (userInfo.hasOwnProperty('avatar_url')) {
    userAvatar.src = userInfo.avatar_url
  };
  if (userInfo.hasOwnProperty('username')) {
    username.textContent = userInfo.username
  };
  if (userInfo.hasOwnProperty('user_uid')) {
    userUID.textContent = userInfo.user_uid
  };
  if (userInfo.hasOwnProperty('email')) {
    email.textContent = userInfo.email
  };

  const logoutButton = document.getElementsByClassName('logout-button');
  if (logoutButton) {
    logoutButton.addEventListener('click', function() {
      fetch('/api/users/auth', {
        method: 'DELETE',
      })
        .then(response => {
          if (response.ok) {
            window.location.href = '/login';
          }
        })
        .catch(error => {
          alert("Ошибка сети")
        });
    });
  }

  tabButtons.forEach(button => {
    button.addEventListener('click', function() {
      const tab = this.dataset.tab;

      // Удаляем класс 'active' у всех кнопок
      tabButtons.forEach(btn => btn.classList.remove('active'));
      // Добавляем класс 'active' к нажатой кнопке
      this.classList.add('active');


      // Вызываем функцию для загрузки сообщений
      loadMessages(tab);
    });
  });

  // Функция для загрузки сообщений из API
  function loadMessages(tab) {
    // Определяем URL API в зависимости от выбранной вкладки
    let apiUrl = `/api/message/${tab}`;

    // Показываем индикатор загрузки
    messageContainer.innerHTML = '<div class="loading">Загрузка...</div>';

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          switch (response.status) {
            case 401:
              const success = attemptAuthorization();
              if (success) {
                // Авторизация прошла успешно, повторяем запрос
                return loadMessages(tab)
              } else {
                window.location.href = '/login';
              }
              break;
            default:
              throw new Error('Server error');
          }
        }
        return response.json(); // Преобразуем ответ в JSON
      })
      .then(messages => {
        // Отображаем сообщения в контейнере
        displayMessages(messages);
      })
      .catch(error => {
        console.error('Ошибка при загрузке сообщений:', error);
        messageContainer.innerHTML = '<div class="error">Ошибка при загрузке сообщений.</div>';
      });
  }

  // Функция для отображения сообщений
  function displayMessages(messages) {
    messageContainer.innerHTML = ''; // Очищаем контейнер

    if (messages && messages.length > 0) {
      messages.forEach(message => {
        // Создаем элементы HTML для отображения каждого сообщения
        const messageElement = document.createElement('div');
        messageElement.classList.add('message'); // Можно добавить класс для стилизации

        // Пример отображения данных сообщения (замените на свои поля)
        messageElement.innerHTML = `
          <div class="message-header">
            <span class="sender">Неизвестный отправитель</span>
            <span class="date">${message.date || 'Неизвестная дата'}</span>
          </div>
          <div class="message-body">
            ${message.body || 'Нет текста сообщения'}
          </div>
        `;

        messageContainer.appendChild(messageElement);
      });
    } else {
      messageContainer.innerHTML = '<div class="empty">Нет сообщений.</div>';
    }
  }

  // Загружаем сообщения для вкладки "Принятые" по умолчанию при загрузке страницы
  loadMessages('accepted');
  tabButtons[0].classList.add('active');
});
