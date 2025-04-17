async function attemptAuthorization() {
  const response = await fetch("/api/users/auth/tokens");
  if (response.ok) {
    return true;
  } else {
    return false;
  }
}

async function GetAuthorizedUser() {
  const response = await fetch("/api/users");

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
          window.location.href = "/login";
        }
        break;
      default:
        return null;
    }
  }
}

async function loadMessages(tab) {
  const messageContainer = document.getElementById("message-container");
  const url = `/api/message/${tab}`;

  messageContainer.innerHTML = '<div class="loading">Загрузка...</div>';

  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      throw new Error();
    }
    const messages = await response.json();
    return messages;
  } catch (error) {
    messageContainer.innerHTML =
      '<div class="error">Ошибка при загрузке сообщений.</div>';
  }
}

function displayMessages(messages, category) {
  const messageContainer = document.getElementById("message-container");
  messageContainer.innerHTML = "";

  if (messages && messages.length > 0) {
    messages.forEach((message) => {
      const messageElement = document.createElement("div");
      messageElement.classList.add("message");

      const senderInfo = message.to_user
        ? `Сообщение для ${message.to_user}`
        : message.from_user
          ? `Сообщение от ${message.from_user}`
          : "Неизвестный отправитель";

      const fullMessageBody = message.body || "Нет текста сообщения";
      const truncatedMessageBody =
        fullMessageBody.length > 100
          ? fullMessageBody.substring(0, 100) + "..."
          : fullMessageBody;

      messageElement.innerHTML = `
          <div class="message-header">
            <div>${senderInfo}</div>
            <div class="message-date">${message.date || "Неизвестная дата"}</div>
          </div>
          <div class="message-body">
            ${truncatedMessageBody}
          </div>
        `;

      messageElement.addEventListener("click", () => {
        openFullMessage(
          fullMessageBody,
          message.id,
          senderInfo,
          message.date || "Неизвестная дата",
          category,
        );
      });

      messageContainer.appendChild(messageElement);
    });
  } else {
    messageContainer.innerHTML = '<div class="empty">Нет сообщений.</div>';
  }
}

async function openFullMessage(fullMessage, messageId, sender, date, category) {
  const modal = document.createElement("div");
  modal.classList.add("modal");

  const modalContent = document.createElement("div");
  modalContent.classList.add("modal-content");

  const modalHeader = document.createElement("div");
  modalHeader.classList.add("modal-header");

  const closeButton = document.createElement("span");
  closeButton.classList.add("close");
  closeButton.innerHTML = "&times;";
  closeButton.addEventListener("click", () => {
    modal.remove();
  });

  const sender_div = document.createElement("div");
  sender_div.innerHTML = `${sender}`;

  const date_div = document.createElement("div");
  date_div.innerHTML = `${date}`;

  modalHeader.appendChild(closeButton);
  modalHeader.appendChild(sender_div);
  modalHeader.appendChild(date_div);
  modalContent.appendChild(modalHeader);

  const modalBody = document.createElement("div");
  modalBody.classList.add("modal-body");
  modalBody.textContent = fullMessage;
  modalContent.appendChild(modalBody);

  var sendButton = document.getElementById("send-button");
  if (category == "accepted") {
    const replyButton = document.createElement("button");
    replyButton.classList.add("open-modal-button");
    replyButton.textContent = "Ответить";
    replyButton.onclick = function () {
      var modalSendMessage = document.getElementById("modal");
      var uidInput = document.getElementById("uid");
      var uidLabel = document.getElementById("uid-label");
      uidInput.style.display = "none";
      uidLabel.style.display = "none";
      modalSendMessage.style.display = "block";

      sendButton.onclick = () => {
        sendMessage(messageId);
        uidInput.style.display = "block";
        uidLabel.style.display = "block";
      };
    };

    const modalFooter = document.createElement("div");
    modalFooter.appendChild(replyButton);
    modalContent.appendChild(modalFooter);
  }

  modal.appendChild(modalContent);
  modal.style.display = "block";

  modal.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.remove();
      sendButton.onclick = () => {
        sendMessage();
      };
    }
  });
  document.body.appendChild(modal);
}

async function sendMessage(messageId = null) {
  var uid = document.getElementById("uid").value;
  var message = document.getElementById("message").value;
  var modal = document.getElementById("modal");

  const url = messageId ? `/api/message/accepted/${messageId}` : "/api/message";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      to_user_uid: uid,
      body: message,
    }),
  })
    .then((response) => {
      modal.style.display = "none";
      if (response.ok) {
        document.getElementById("uid").value = "";
        document.getElementById("message").value = "";
        displayNotification("Сообщение успешно отправлено", "success");
      } else {
        switch (response.status) {
          case 400:
            displayNotification(
              "Не удалось отправить сообщение, пользователь с данным UID не найден",
              "failed",
            );
            break;
          case 422:
            displayNotification(
              "Не удалось отправить сообщение, укажите UID пользователя и введите текст сообщения",
              "failed",
            );
            break;
        }
      }
    })
    .catch((error) => {
      displayNotification(
        "Произошла ошибка сети, пожалуйста повторите попытку",
        "failed",
      );
    });
}

async function displayNotification(message, type = "info") {
  const container = document.getElementsByClassName(
    "notification-container",
  )[0];
  const notificationElement = document.createElement("div");
  notificationElement.classList.add("notification", type);
  notificationElement.textContent = message;

  container.appendChild(notificationElement);
  notificationElement.style.display = "block";

  setTimeout(function () {
    notificationElement.remove();
  }, 3000);
}

document.addEventListener("DOMContentLoaded", async function () {
  const tabButtons = document.querySelectorAll(".tab-button");

  const username = document.getElementById("username");
  const userUID = document.getElementById("user-uid");
  const email = document.getElementById("email");

  const userInfo = await GetAuthorizedUser();
  if (userInfo.hasOwnProperty("username")) {
    username.textContent = userInfo.username;
  }
  if (userInfo.hasOwnProperty("user_uid")) {
    userUID.textContent = userInfo.user_uid;
  }
  if (userInfo.hasOwnProperty("email")) {
    email.textContent = userInfo.email;
  }

  const logoutButton = document.getElementsByClassName("logout-button")[0];
  if (logoutButton) {
    logoutButton.addEventListener("click", function () {
      fetch("/api/users/auth", {
        method: "DELETE",
      })
        .then((response) => {
          if (response.ok) {
            window.location.href = "/login";
          }
        })
        .catch((error) => {
          displayNotification("Ошибка сети", "failed");
        });
    });
  }

  tabButtons.forEach((button) => {
    button.addEventListener("click", async function () {
      const tab = this.dataset.tab;

      tabButtons.forEach((btn) => btn.classList.remove("active"));
      this.classList.add("active");

      const messages = await loadMessages(tab);
      displayMessages(messages, tab);
    });
  });

  var modal = document.getElementById("modal");
  var btn = document.getElementsByClassName("open-modal-button")[0];
  var closeSpan = document.getElementsByClassName("close")[0];
  var sendButton = document.getElementById("send-button");

  btn.onclick = function () {
    modal.style.display = "block";
  };

  closeSpan.onclick = function () {
    modal.style.display = "none";
  };

  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };

  sendButton.onclick = () => {
    sendMessage();
  };
});
