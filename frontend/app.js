const form = document.querySelector('#qualification-form');
const errorBox = document.querySelector('#form-error');
const emptyState = document.querySelector('#result-empty');
const result = document.querySelector('#recommendation');
const submitButton = form.querySelector('button[type="submit"]');

function showError(message) {
  errorBox.textContent = message;
  errorBox.hidden = false;
}

function clearError() {
  errorBox.hidden = true;
  errorBox.textContent = '';
}

function formPayload() {
  const data = new FormData(form);
  const comment = String(data.get('comment') || '').trim();
  return {
    name: String(data.get('name') || '').trim(),
    email: String(data.get('email') || '').trim(),
    phone: String(data.get('phone') || '').trim(),
    experience: data.get('experience'),
    goal: data.get('goal'),
    destination: data.get('destination'),
    season: data.get('season'),
    group_type: data.get('group_type'),
    comment: comment || null,
  };
}

function renderRecommendation(recommendation) {
  document.querySelector('#result-title').textContent = recommendation.title;
  document.querySelector('#result-subtitle').textContent = recommendation.subtitle;
  document.querySelector('#result-reason').textContent = recommendation.reason;
  document.querySelector('#result-next-step').textContent = recommendation.next_step;
  const benefits = document.querySelector('#result-benefits');
  benefits.replaceChildren(...recommendation.benefits.map((text) => {
    const item = document.createElement('li');
    item.textContent = text;
    return item;
  }));
  emptyState.hidden = true;
  result.hidden = false;
  result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  clearError();
  if (!form.checkValidity()) {
    form.reportValidity();
    showError('Проверьте обязательные поля формы.');
    return;
  }
  submitButton.disabled = true;
  submitButton.querySelector('span').textContent = 'Строим маршрут…';
  try {
    const response = await fetch('/api/qualify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formPayload()),
    });
    const body = await response.json();
    if (!response.ok) throw new Error(body.detail?.[0]?.msg || body.detail || 'Не удалось сохранить заявку');
    renderRecommendation(body.recommendation);
  } catch (error) {
    showError(error.message || 'Сервис временно недоступен. Попробуйте ещё раз.');
  } finally {
    submitButton.disabled = false;
    submitButton.querySelector('span').textContent = 'Получить рекомендацию';
  }
});

document.querySelector('#restart-button').addEventListener('click', () => {
  form.reset();
  result.hidden = true;
  emptyState.hidden = false;
  clearError();
  form.scrollIntoView({ behavior: 'smooth' });
});

async function loadFaq() {
  const list = document.querySelector('#faq-list');
  try {
    const response = await fetch('/api/faq');
    const items = await response.json();
    list.replaceChildren(...items.map((item) => {
      const details = document.createElement('details');
      const summary = document.createElement('summary');
      const answer = document.createElement('p');
      summary.textContent = item.question;
      answer.textContent = item.answer;
      details.append(summary, answer);
      return details;
    }));
  } catch {
    list.textContent = 'Не удалось загрузить вопросы.';
  }
}

loadFaq();

