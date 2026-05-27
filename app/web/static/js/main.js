document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendBtn = document.getElementById('send-btn');
    const newChatBtn = document.getElementById('new-chat-btn');
    const recentChatsList = document.getElementById('recent-chats-list');
    
    // Mobile Sidebar Elements
    const menuToggleBtn = document.getElementById('menu-toggle-btn');
    const closeSidebarBtn = document.getElementById('close-sidebar-btn');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebar-overlay');

    // Configure Marked.js
    if (typeof marked !== 'undefined') {
        marked.setOptions({
            breaks: true,
            gfm: true
        });
    }

    // Auto-resize textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        sendBtn.disabled = this.value.trim() === '';
    });

    // Handle Enter key (Shift+Enter for new line)
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!sendBtn.disabled) {
                chatForm.dispatchEvent(new Event('submit'));
            }
        }
    });

    // Handle Mobile Sidebar Toggle
    function toggleSidebar() {
        if(sidebar && sidebarOverlay) {
            sidebar.classList.toggle('open');
            sidebarOverlay.classList.toggle('active');
        }
    }

    if (menuToggleBtn) menuToggleBtn.addEventListener('click', toggleSidebar);
    if (closeSidebarBtn) closeSidebarBtn.addEventListener('click', toggleSidebar);
    if (sidebarOverlay) sidebarOverlay.addEventListener('click', toggleSidebar);

    function closeSidebarOnMobile() {
        if (window.innerWidth <= 768 && sidebar && sidebarOverlay) {
            sidebar.classList.remove('open');
            sidebarOverlay.classList.remove('active');
        }
    }

    // Fetch and display recent sessions
    async function fetchSessions() {
        try {
            const response = await fetch('/sessions?t=' + Date.now(), {
                headers: { 'Cache-Control': 'no-cache' }
            });
            const data = await response.json();
            
            if (recentChatsList) {
                recentChatsList.innerHTML = '';
                if (data.sessions) {
                    data.sessions.forEach(session => {
                        const li = document.createElement('li');
                        li.dataset.id = session.id;
                        
                        if (session.id === data.active_session_id) {
                            li.classList.add('active');
                        }
                        
                        const titleSpan = document.createElement('span');
                        titleSpan.className = 'session-title';
                        titleSpan.textContent = session.title || "New Chat";
                        
                        const deleteBtn = document.createElement('button');
                        deleteBtn.className = 'delete-session-btn';
                        deleteBtn.innerHTML = '<i class="fa-solid fa-trash"></i>';
                        deleteBtn.title = "Delete Chat";
                        
                        deleteBtn.addEventListener('click', async (e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            try {
                                const delRes = await fetch(`/session/${session.id}`, { method: 'DELETE' });
                                if(delRes.ok) {
                                    const newActiveId = await fetchSessions();
                                    if (newActiveId) {
                                        loadSession(newActiveId);
                                    } else {
                                        chatMessages.innerHTML = '';
                                        showWelcomeScreen();
                                    }
                                }
                            } catch(err) {
                                console.error("Error deleting session", err);
                            }
                        });
                        
                        li.appendChild(titleSpan);
                        li.appendChild(deleteBtn);
                        
                        li.addEventListener('click', () => {
                            loadSession(session.id);
                            closeSidebarOnMobile();
                        });
                        
                        recentChatsList.appendChild(li);
                    });
                }
            }
            return data.active_session_id;
        } catch (error) {
            console.error('Error fetching sessions:', error);
        }
    }
    
    // Load Session
    async function loadSession(sessionId) {
        try {
            const response = await fetch(`/session/${sessionId}?t=` + Date.now(), {
                headers: { 'Cache-Control': 'no-cache' }
            });
            const data = await response.json();
            
            if (data.error) {
                console.error(data.error);
                return;
            }
            
            chatMessages.innerHTML = '';
            
            if (!data.history || data.history.length === 0) {
                showWelcomeScreen();
            } else {
                data.history.forEach(msg => {
                    if (msg.role === 'user') {
                        appendUserMessage(msg.content);
                    } else {
                        appendAssistantMessage({ 
                            response: msg.content, 
                            status: "success", 
                            code_snippet: null 
                        });
                    }
                });
            }
            
            fetchSessions();
        } catch (error) {
            console.error('Error loading session:', error);
        }
    }

    // Reset Chat
    if (newChatBtn) {
        newChatBtn.addEventListener('click', async () => {
            try {
                const response = await fetch('/reset', { method: 'POST' });
                if (response.ok) {
                    chatMessages.innerHTML = '';
                    showWelcomeScreen();
                    messageInput.value = '';
                    messageInput.style.height = 'auto';
                    sendBtn.disabled = true;
                    fetchSessions();
                    closeSidebarOnMobile();
                }
            } catch (error) {
                console.error('Error resetting chat:', error);
            }
        });
    }

    // Submit Chat
    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const message = messageInput.value.trim();
            if (!message) return;
            
            const welcomeContainer = document.getElementById('welcome-container');
            if (welcomeContainer) {
                welcomeContainer.remove();
            }
            
            appendUserMessage(message);
            
            messageInput.value = '';
            messageInput.style.height = 'auto';
            sendBtn.disabled = true;
            
            const typingId = showTypingIndicator();
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                removeTypingIndicator(typingId);
                appendAssistantMessage(data);
                fetchSessions();
                
            } catch (error) {
                console.error('Error sending message:', error);
                removeTypingIndicator(typingId);
                appendErrorMessage('Sorry, there was an error communicating with the server.');
            }
        });
    }

    function showWelcomeScreen() {
        chatMessages.innerHTML = `
            <div class="welcome-container" id="welcome-container">
                <div class="welcome-logo">
                    <i class="fa-solid fa-robot"></i>
                </div>
                <h2>How can I help you today?</h2>
                <p>I am Shukaku AI, specializing in technical questions. Try asking me about one of these topics:</p>
                <div class="capabilities-grid">
                    <div class="capability-card"><i class="fa-brands fa-python"></i><span>Programming</span></div>
                    <div class="capability-card"><i class="fa-brands fa-linux"></i><span>Linux OS</span></div>
                    <div class="capability-card"><i class="fa-brands fa-docker"></i><span>Docker</span></div>
                    <div class="capability-card"><i class="fa-brands fa-aws"></i><span>AWS Cloud</span></div>
                    <div class="capability-card"><i class="fa-solid fa-brain"></i><span>AI / ML</span></div>
                    <div class="capability-card"><i class="fa-solid fa-code-branch"></i><span>DevOps</span></div>
                </div>
            </div>
        `;
    }

    function appendUserMessage(text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message user-message';
        const escapedText = escapeHTML(text);
        const formattedText = formatTextWithLineBreaks(escapedText);
        
        msgDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-user"></i></div>
            <div class="message-content">
                <p>${formattedText}</p>
            </div>
        `;
        
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function appendAssistantMessage(data) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message assistant-message';
        let contentHtml = '';
        
        if (data.status === 'rejected' || data.status === 'error') {
            msgDiv.classList.add('status-rejected');
            contentHtml = `<p><strong>${escapeHTML(data.response || '')}</strong></p>`;
        } else {
            if (typeof marked !== 'undefined' && typeof DOMPurify !== 'undefined') {
                let fullText = data.response || '';
                if (data.code_snippet) {
                    fullText += `\n\n\`\`\`\n${data.code_snippet}\n\`\`\``;
                }
                const rawHtml = marked.parse(fullText);
                contentHtml = DOMPurify.sanitize(rawHtml);
            } else {
                contentHtml = `<p>${formatTextWithLineBreaks(escapeHTML(data.response || ''))}</p>`;
                if (data.code_snippet) {
                    contentHtml += `<pre><code>${escapeHTML(data.code_snippet)}</code></pre>`;
                }
            }
        }
        
        msgDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="message-content">${contentHtml}</div>
        `;
        chatMessages.appendChild(msgDiv);
        
        // Format Code Blocks
        msgDiv.querySelectorAll('pre code').forEach((block) => {
            if(typeof hljs !== 'undefined') {
                hljs.highlightElement(block);
            }
            
            const langClass = Array.from(block.classList).find(c => c.startsWith('language-'));
            const lang = langClass ? langClass.replace('language-', '') : 'code';
            
            const pre = block.parentElement;
            const codeContainer = document.createElement('div');
            codeContainer.className = 'code-container';
            
            codeContainer.innerHTML = `
                <div class="code-header">
                    <div class="code-header-left">
                        <div class="window-dots">
                            <div class="window-dot red"></div>
                            <div class="window-dot yellow"></div>
                            <div class="window-dot green"></div>
                        </div>
                        <span class="language-label">${lang}</span>
                    </div>
                    <button class="copy-btn" title="Copy code">
                        <i class="fa-regular fa-clipboard"></i> Copy
                    </button>
                </div>
            `;
            
            pre.parentNode.insertBefore(codeContainer, pre);
            codeContainer.appendChild(pre);
            
            const copyBtn = codeContainer.querySelector('.copy-btn');
            copyBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(block.innerText).then(() => {
                    copyBtn.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
                    setTimeout(() => {
                        copyBtn.innerHTML = '<i class="fa-regular fa-clipboard"></i> Copy';
                    }, 2000);
                });
            });
        });
        
        scrollToBottom();
    }

    function appendErrorMessage(text) {
        appendAssistantMessage({ response: text, status: "error" });
    }

    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message assistant-message';
        msgDiv.id = id;
        
        msgDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="message-content">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function escapeHTML(str) {
        if (!str) return '';
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
    
    function formatTextWithLineBreaks(str) {
        if (!str) return '';
        return str.replace(/\n/g, '<br>');
    }

    // Initial Load
    fetchSessions().then(active_id => {
        if (active_id) {
            loadSession(active_id);
        }
    });
});
