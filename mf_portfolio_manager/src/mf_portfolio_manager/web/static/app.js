const form = document.getElementById('chat-form');
const messageInput = document.getElementById('message');
const chatLog = document.getElementById('chat-log');
const template = document.getElementById('message-template');

const history = [];

function appendMessage(role, content) {
  const node = template.content.firstElementChild.cloneNode(true);
  node.classList.add(role);
  node.querySelector('.meta').textContent =
    role === 'user' ? 'You' : 'CrewAI';
  node.querySelector('.content').textContent = content;
  chatLog.appendChild(node);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function collectFormPayload() {
  const data = new FormData(form);
  const payload = Object.fromEntries(data.entries());
  payload.monthly_sip = Number(payload.monthly_sip);
  payload.investment_months = Number(payload.investment_months);
  payload.holding_months = Number(payload.holding_months);
  payload.lumpsum_amount = Number(payload.lumpsum_amount);
  payload.purchase_nav = Number(payload.purchase_nav);
  payload.current_nav = Number(payload.current_nav);
  payload.holding_years = Number(payload.holding_years);
  payload.investment_horizon = Number(payload.investment_horizon);
  payload.monthly_budget = Number(payload.monthly_budget);
  payload.lumpsum_budget = Number(payload.lumpsum_budget);
  payload.history = history;
  return payload;
}

async function sendMessage(event) {
  event.preventDefault();
  const message = messageInput.value.trim();
  if (!message) {
    return;
  }

  appendMessage('user', message);
  history.push({ role: 'user', content: message });
  form.querySelector('button[type="submit"]').disabled = true;

  try {
    const payload = collectFormPayload();
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Unknown server error');
    }

    const data = await response.json();
    appendMessage('assistant', data.reply);
    history.push({ role: 'assistant', content: data.reply });
  } catch (error) {
    appendMessage('assistant', `⚠️ ${error.message}`);
  } finally {
    form.querySelector('button[type="submit"]').disabled = false;
    messageInput.value = '';
    messageInput.focus();
  }
}

form.addEventListener('submit', sendMessage);

appendMessage(
  'assistant',
  'Hi! Provide your investment goal and press Send to run the crew. Every call is traced in CrewAI AMP.'
);

