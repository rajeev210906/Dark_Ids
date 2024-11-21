// Function to open the message card
function openMessage(sender, phoneEmail, message) {
    document.getElementById('cardSenderName').textContent = sender;
    document.getElementById('cardPhoneEmail').textContent = phoneEmail;
    document.getElementById('cardMessage').textContent = message;
    document.getElementById('messageCard').style.display = 'block';
}

// Function to close the message card
function closeMessage() {
    document.getElementById('messageCard').style.display = 'none';
}

// Function to open the reply popup
function openReplyPopup() {
    document.getElementById('replyPopup').style.display = 'block';
}

// Function to close the reply popup
function closeReplyPopup() {
    document.getElementById('replyPopup').style.display = 'none';
}

// Function to send the reply
function sendReply() {
    const replyMessage = document.getElementById('replyMessage').value;
    if (replyMessage) {
        alert('Reply sent: ' + replyMessage);  // Placeholder for backend integration
        document.getElementById('replyMessage').value = '';  // Clear the input
        closeReplyPopup();  // Close the popup
    }
}


// Green Button Popup
function openSendMessagePopup() {
    document.getElementById('sendMessagePopup').style.display = 'block';
}

function closeSendMessagePopup() {
    document.getElementById('sendMessagePopup').style.display = 'none';
}

function sendMessage() {
    const phoneNumber = document.getElementById('phoneNumber').value;
    const messageText = document.getElementById('messageText').value;
    alert(`Message sent to ${phoneNumber}: ${messageText}`);
    closeSendMessagePopup();
}

// Red Button Popup - All Users
function openAllUsersPopup() {
    document.getElementById('allUsersPopup').style.display = 'block';
}

function closeAllUsersPopup() {
    document.getElementById('allUsersPopup').style.display = 'none';
}

// User Message Popup
function openUserMessagePopup(phone) {
    document.getElementById('userMessagePopup').style.display = 'block';
    document.getElementById('userMessagePopup').dataset.phone = phone;
}

function closeUserMessagePopup() {
    document.getElementById('userMessagePopup').style.display = 'none';
}

function sendUserMessage() {
    const phone = document.getElementById('userMessagePopup').dataset.phone;
    const userMessageText = document.getElementById('userMessageText').value;
    alert(`Message sent to ${phone}: ${userMessageText}`);
    closeUserMessagePopup();
}
