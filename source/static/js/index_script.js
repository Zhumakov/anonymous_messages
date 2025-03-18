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


function loadMessages(tab) {
  const messageContainer = document.getElementById('message-container');
  let apiUrl = `/api/message/${tab}`;

  messageContainer.innerHTML = '<div class="loading">Загрузка...</div>';

  fetch(apiUrl)
    .then(response => {
      if (!response.ok) {
        switch (response.status) {
          case 401:
            const success = attemptAuthorization();
            if (success) {
              return loadMessages(tab)
            } else {
              window.location.href = '/login';
            }
            break;
          default:
            throw new Error('Server error');
        }
      }
      return response.json();
    })
    .then(messages => {
      displayMessages(messages);
    })
    .catch(error => {
      console.error('Ошибка при загрузке сообщений:', error);
      messageContainer.innerHTML = '<div class="error">Ошибка при загрузке сообщений.</div>';
    });
}


function displayMessages(messages) {
  const messageContainer = document.getElementById('message-container');
  messageContainer.innerHTML = '';

  if (messages && messages.length > 0) {
    messages.forEach(message => {
      const messageElement = document.createElement('div');
      messageElement.classList.add('message');

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


async function sendMessage() {

  var uid = document.getElementById("uid").value;
  var message = document.getElementById("message").value;
  var modal = document.getElementById("modal");

  fetch('/api/message', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      to_user_uid: uid,
      body: message
    })
  })
    .then(response => {
      if (response.ok) {
        modal.style.display = "none";
        document.getElementById("uid").value = "";
        document.getElementById("message").value = "";

      } else {
        alert("Произошла ошибка при отправке сообщения.");
      }
    })
    .catch(error => {
      alert("Произошла ошибка сети при отправке сообщения.");
    });
}


document.addEventListener('DOMContentLoaded', async function() {
  const tabButtons = document.querySelectorAll('.tab-button');

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

  const logoutButton = document.getElementsByClassName('logout-button')[0];
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


  var modal = document.getElementById("modal");
  var btn = document.getElementsByClassName("open-modal-button")[0];
  var closeSpan = document.getElementsByClassName("close")[0];
  var sendButton = document.getElementById("send-button");

  btn.onclick = function() {
    modal.style.display = "block";
  };

  closeSpan.onclick = function() {
    modal.style.display = "none";
  };

  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };

  sendButton.onclick = sendMessage;


  loadMessages('accepted');
  tabButtons[0].classList.add('active');
});
