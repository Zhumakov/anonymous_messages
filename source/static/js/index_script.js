document.addEventListener('DOMContentLoaded', function() {
  const tabButtons = document.querySelectorAll('.tab-button');
  const messageContainer = document.getElementById('message-container');

  tabButtons.forEach(button => {
    button.addEventListener('click', function() {
      const tab = this.dataset.tab; // Получаем значение data-tab атрибута

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
          throw new Error(`HTTP error! status: ${response.status}`);
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
