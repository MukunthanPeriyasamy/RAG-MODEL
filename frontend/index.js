document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("sidebar");
  const handle = document.getElementById("handle");
  const body = document.body;
  const themeToggle = document.getElementById("themeToggle");
  const sunIcon = document.getElementById("sun-icon");
  const moonIcon = document.getElementById("moon-icon");
  const uploadPrompt = document.getElementById("upload-prompt");
  const chatInputContainer = document.getElementById("chat-input-container");
  const loadingMessage = document.getElementById("loading-message");
  const fileInput = document.getElementById("fileInput");
  const uploadDocButtonSidebar = document.getElementById(
    "uploadDocButtonSidebar"
  );
  const uploadDocButtonChat = document.getElementById("uploadDocButtonChat");
  const dropZone = document.getElementById("drop-zone");
  const documentList = document.getElementById("document-list");
  const chatMessages = document.getElementById("chat-messages");
  const messageModal = document.getElementById("message-modal");
  const modalMessage = document.getElementById("modal-message");
  const closeModal = document.getElementById("close-modal");

  // API endpoints
  const UPLOAD_API_ENDPOINT = "http://127.0.0.1:8000/upload/";
  const CHAT_API_ENDPOINT = "http://127.0.0.1:8000/chat/";

  const uploadedDocuments = [];

  // Function to show the custom message modal
  function showMessageModal(message, isWarning = false) {
    modalMessage.textContent = message;
    modalMessage.style.color = isWarning
      ? "var(--warning-color)"
      : "var(--text-color-main)";
    messageModal.classList.remove("hidden");
    messageModal.classList.add("flex");
  }

  // Event listener for closing the modal
  closeModal.addEventListener("click", () => {
    messageModal.classList.remove("flex");
    messageModal.classList.add("hidden");
  });

  // Theme toggle functionality
  themeToggle.addEventListener("click", () => {
    const currentTheme = body.getAttribute("data-theme");
    if (currentTheme === "light") {
      body.setAttribute("data-theme", "dark");
      sunIcon.classList.add("hidden");
      moonIcon.classList.remove("hidden");
    } else {
      body.setAttribute("data-theme", "light");
      moonIcon.classList.add("hidden");
      sunIcon.classList.remove("hidden");
    }
  });

  // Sidebar resize functionality
  let isResizing = false;
  handle.addEventListener("mousedown", (e) => {
    isResizing = true;
    document.body.style.cursor = "ew-resize";
  });

  document.addEventListener("mousemove", (e) => {
    if (!isResizing) return;
    const newWidth = e.clientX;
    const minWidth = parseInt(getComputedStyle(sidebar).minWidth);
    const maxWidth = parseInt(getComputedStyle(sidebar).maxWidth);
    if (newWidth > minWidth && newWidth < maxWidth) {
      sidebar.style.width = `${newWidth}px`;
    }
  });

  document.addEventListener("mouseup", () => {
    isResizing = false;
    document.body.style.cursor = "default";
  });

  // Function to handle document upload
  async function uploadDocument(file) {
    if (!file) return;

    if (uploadedDocuments.includes(file.name)) {
      showMessageModal("the document is already uploaded", true);
      return;
    }

    // Display the loading message in the chat area
    const loadingChatBubble = document.createElement("div");
    loadingChatBubble.id = "upload-loading-bubble";
    loadingChatBubble.className = "text-left my-2";
    loadingChatBubble.innerHTML = `<span class="bg-[var(--chat-bubble-bg)] text-[var(--text-color-main)] py-2 px-4 rounded-lg inline-block max-w-lg">
                    <svg class="animate-spin h-5 w-5 text-current inline-block mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Uploading document...
                </span>`;
    chatMessages.appendChild(loadingChatBubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    uploadPrompt.classList.add("hidden");
    chatMessages.classList.remove("hidden");

    const formData = new FormData();
    formData.append("files", file);

    try {
      const response = await fetch(UPLOAD_API_ENDPOINT, {
        method: "POST",
        body: formData,
      });

      // Remove the loading bubble regardless of success or failure
      document.getElementById("upload-loading-bubble").remove();

      if (response.ok) {
        const result = await response.json();
        showMessageModal("Document uploaded successfully!", false);
        addDocumentToList(file.name);
        uploadedDocuments.push(file.name);
        enableChatInterface();
      } else {
        const error = await response.json();
        showMessageModal(`Upload failed: ${error.message}`, true);
        uploadPrompt.classList.remove("hidden");
        chatInputContainer.classList.add("hidden");
      }
    } catch (error) {
      // Remove the loading bubble in case of a network error
      document.getElementById("upload-loading-bubble").remove();
      showMessageModal(
        "An error occurred during upload. Please check the network connection.",
        true
      );
      uploadPrompt.classList.remove("hidden");
      chatInputContainer.classList.add("hidden");
    } finally {
      loadingMessage.classList.add("hidden");
    }
  }

  // Drag and drop event listeners
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("border-[var(--accent-color)]");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("border-[var(--accent-color)]");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("border-[var(--accent-color)]");
    const file = e.dataTransfer.files[0];
    if (file) {
      uploadDocument(file);
    }
  });

  // Click to browse functionality
  dropZone.addEventListener("click", () => fileInput.click());

  // Event listeners for other upload buttons
  uploadDocButtonSidebar.addEventListener("click", () => fileInput.click());
  uploadDocButtonChat.addEventListener("click", () => fileInput.click());

  // File input change event listener
  fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
      uploadDocument(file);
    }
  });

  // Function to enable the chat interface
  function enableChatInterface() {
    uploadPrompt.classList.add("hidden");
    chatInputContainer.classList.remove("hidden");
    chatMessages.classList.remove("hidden");
  }

  // Function to add a document to the sidebar list
  function addDocumentToList(fileName) {
    const docItem = document.createElement("div");
    docItem.className = "document-item";
    docItem.innerHTML = `
                    <span class="truncate">${fileName}</span>
                    <button class="delete-doc p-1 rounded-full hover:bg-[var(--accent-bg-hover)] focus:outline-none">
                        <svg class="w-4 h-4 text-[var(--text-color-secondary)]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                `;
    documentList.prepend(docItem);

    // Add event listener for the delete button
    docItem.querySelector(".delete-doc").addEventListener("click", (e) => {
      e.stopPropagation();
      const index = uploadedDocuments.indexOf(fileName);
      if (index > -1) {
        uploadedDocuments.splice(index, 1);
      }
      docItem.remove();
      showMessageModal(`${fileName} has been removed.`, false);
    });
  }

  // Chat functionality
  const chatInput = document.getElementById("chat-input");
  const sendButton = document.getElementById("send-button");

  async function sendMessage(message) {
    // Display user message
    const userMessageElement = document.createElement("div");
    userMessageElement.className = "text-right my-2";
    userMessageElement.innerHTML = `<span class="bg-[var(--accent-color)] text-[var(--accent-text-color)] py-2 px-4 rounded-lg inline-block max-w-lg">${message}</span>`;
    chatMessages.appendChild(userMessageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Display loading message for AI response
    const loadingAiMessage = document.createElement("div");
    loadingAiMessage.className = "text-left my-2";
    loadingAiMessage.innerHTML = `<span class="bg-[var(--chat-bubble-bg)] text-[var(--text-color-main)] py-2 px-4 rounded-lg inline-block max-w-lg">
                    <svg class="animate-spin h-5 w-5 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                </span>`;
    chatMessages.appendChild(loadingAiMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    const payload = { question: message };

    try {
      const response = await fetch(CHAT_API_ENDPOINT, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      loadingAiMessage.remove(); // Remove loading message after response

      if (response.ok) {
        const result = await response.json();
        const aiMessageElement = document.createElement("div");
        aiMessageElement.className = "text-left my-2";
        aiMessageElement.innerHTML = `<span class="bg-[var(--chat-bubble-bg)] text-[var(--text-color-main)] py-2 px-4 rounded-lg inline-block max-w-lg">${result.answer}</span>`;
        chatMessages.appendChild(aiMessageElement);
      } else {
        const error = await response.json();
        const errorMessageElement = document.createElement("div");
        errorMessageElement.className = "text-left my-2";
        errorMessageElement.innerHTML = `<span class="bg-red-500 text-white py-2 px-4 rounded-lg inline-block max-w-lg">Error: ${
          error.detail || "An unknown error occurred."
        }</span>`;
        chatMessages.appendChild(errorMessageElement);
      }
    } catch (error) {
      loadingAiMessage.remove(); // Remove loading message in case of network error
      const errorMessageElement = document.createElement("div");
      errorMessageElement.className = "text-left my-2";
      errorMessageElement.innerHTML = `<span class="bg-red-500 text-white py-2 px-4 rounded-lg inline-block max-w-lg">Network error. Please check your API server.</span>`;
      chatMessages.appendChild(errorMessageElement);
    } finally {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  }

  sendButton.addEventListener("click", () => {
    const userMessage = chatInput.value.trim();
    if (userMessage) {
      sendMessage(userMessage);
      chatInput.value = "";
    }
  });

  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendButton.click();
    }
  });
});
