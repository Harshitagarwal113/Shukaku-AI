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

    // Local Storage State Management
    const STORAGE_KEY = 'shukaku_sessions';
    let activeSessionId = null;

    function getSessions() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
        } catch (e) {
            return [];
        }
    }

    function saveSessions(sessions) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(sessions));
    }
    
    function getSession(id) {
        const sessions = getSessions();
        return sessions.find(s => s.id === id);
    }
    
    function updateSession(updatedSession) {
        let sessions = getSessions();
        const index = sessions.findIndex(s => s.id === updatedSession.id);
        if (index !== -1) {
            sessions[index] = updatedSession;
        } else {
            sessions.unshift(updatedSession);
        }
        if (sessions.length > 10) sessions.pop(); // Keep only 10 recent
        saveSessions(sessions);
    }

    function createNewSession() {
        const id = 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        const newSession = {
            id: id,
            title: "New Chat",
            history: []
        };
        updateSession(newSession);
        return id;
    }

    function deleteSessionLocal(id) {
        let sessions = getSessions();
        sessions = sessions.filter(s => s.id !== id);
        saveSessions(sessions);
    }

    // Render Sessions to Sidebar
    function renderSessions() {
        const sessions = getSessions();
        
        if (recentChatsList) {
            recentChatsList.innerHTML = '';
            
            // Filter out empty "New Chat" sessions unless it's the active one
            const displaySessions = sessions.filter(s => s.title !== "New Chat" || s.id === activeSessionId);
            
            displaySessions.forEach(session => {
                const li = document.createElement('li');
                li.dataset.id = session.id;
                
                if (session.id === activeSessionId) {
                    li.classList.add('active');
                }
                
                const titleSpan = document.createElement('span');
                titleSpan.className = 'session-title';
                titleSpan.textContent = session.title || "New Chat";
                
                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'delete-session-btn';
                deleteBtn.innerHTML = '<i class="fa-solid fa-trash"></i>';
                deleteBtn.title = "Delete Chat";
                
                deleteBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    deleteSessionLocal(session.id);
                    
                    if (session.id === activeSessionId) {
                        // Deleted active session, start a new one
                        const newSessions = getSessions();
                        if (newSessions.length > 0) {
                            loadSession(newSessions[0].id);
                        } else {
                            activeSessionId = createNewSession();
                            loadSession(activeSessionId);
                        }
                    } else {
                        renderSessions();
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
    
    // Load Session
    function loadSession(sessionId) {
        activeSessionId = sessionId;
        const session = getSession(sessionId);
        
        if (!session) return;
        
        chatMessages.innerHTML = '';
        
        if (!session.history || session.history.length === 0) {
            showWelcomeScreen();
        } else {
            session.history.forEach(msg => {
                if (msg.role === 'user') {
                    appendUserMessage(msg.content);
                } else {
                    appendAssistantMessage({ 
                        response: msg.content, 
                        intent: "unknown",
                        risk_level: "low"
                    });
                }
            });
        }
        
        renderSessions();
    }

    // Reset Chat
    if (newChatBtn) {
        newChatBtn.addEventListener('click', () => {
            const sessions = getSessions();
            if (sessions.length > 0 && sessions[0].title === "New Chat" && sessions[0].history.length === 0) {
                // Already have a blank new chat
                activeSessionId = sessions[0].id;
            } else {
                activeSessionId = createNewSession();
            }
            
            chatMessages.innerHTML = '';
            showWelcomeScreen();
            messageInput.value = '';
            messageInput.style.height = 'auto';
            sendBtn.disabled = true;
            renderSessions();
            closeSidebarOnMobile();
        });
    }

    // Submit Chat
    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const message = messageInput.value.trim();
            if (!message) return;
            
            // Ensure we have an active session
            if (!activeSessionId || !getSession(activeSessionId)) {
                activeSessionId = createNewSession();
            }
            
            const currentSession = getSession(activeSessionId);
            
            // Set title on first message
            if (currentSession.title === "New Chat") {
                let title = message.split(' ').slice(0, 4).join(' ');
                if (message.split(' ').length > 4) title += "...";
                currentSession.title = title;
            }
            
            const welcomeContainer = document.getElementById('welcome-container');
            if (welcomeContainer) {
                welcomeContainer.remove();
            }
            
            appendUserMessage(message);
            
            // Send current history to backend
            const historyToSend = [...(currentSession.history || [])];
            
            // Save user message to local state
            currentSession.history.push({ role: 'user', content: message });
            updateSession(currentSession);
            renderSessions();
            
            messageInput.value = '';
            messageInput.style.height = 'auto';
            sendBtn.disabled = true;
            
            const typingId = showTypingIndicator();
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        message: message,
                        history: historyToSend 
                    })
                });
                
                const data = await response.json();
                removeTypingIndicator(typingId);
                appendAssistantMessage(data);
                
                // Add assistant response to local history
                if (data.risk_level === "low" && data.intent !== "malicious_activity") {
                    currentSession.history.push({ role: 'assistant', content: data.response || '' });
                    
                    // Keep max history in state (e.g., 20 messages)
                    if (currentSession.history.length > 20) {
                        currentSession.history = currentSession.history.slice(-20);
                    }
                    updateSession(currentSession);
                }
                
            } catch (error) {
                console.error('Error sending message:', error);
                removeTypingIndicator(typingId);
                appendErrorMessage('Sorry, there was an error communicating with the server.');
                // Remove the user message from history on error since it wasn't processed successfully
                currentSession.history.pop();
                updateSession(currentSession);
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
        
        if (data.risk_level === 'high' || data.intent === 'off_topic') {
            msgDiv.classList.add('status-rejected');
            contentHtml = `<p><strong>${escapeHTML(data.response || '')}</strong></p>`;
        } else {
            if (typeof marked !== 'undefined' && typeof DOMPurify !== 'undefined') {
                let fullText = data.response || '';
                const rawHtml = marked.parse(fullText);
                contentHtml = DOMPurify.sanitize(rawHtml);
            } else {
                contentHtml = `<p>${formatTextWithLineBreaks(escapeHTML(data.response || ''))}</p>`;
            }
        }
        
        msgDiv.innerHTML = `
            <div class="avatar" style="background-image: url('/web-static/shukaku_logo.png?v=5'); background-size: contain; background-position: center; background-repeat: no-repeat; border-radius: 6px;"></div>
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
        appendAssistantMessage({ response: text, risk_level: "high", intent: "error" });
    }

    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message assistant-message';
        msgDiv.id = id;
        
        msgDiv.innerHTML = `
            <div class="avatar" style="background-image: url('/web-static/shukaku_logo.png?v=5'); background-size: contain; background-position: center; background-repeat: no-repeat; border-radius: 6px;"></div>
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
        return str.replace(/\\n/g, '<br>');
    }

    // Initial Load - load from localStorage
    function init() {
        const sessions = getSessions();
        if (sessions.length > 0) {
            loadSession(sessions[0].id);
        } else {
            activeSessionId = createNewSession();
            loadSession(activeSessionId);
        }
    }
    
    init();
});
