let adminKey = sessionStorage.getItem('yachtdream_admin_key') || '';
const loginPanel = document.querySelector('#admin-login');
const dashboard = document.querySelector('#dashboard');
const adminError = document.querySelector('#admin-error');

const labels = {
  experience: { none: 'Без опыта', beginner: 'Начальный', experienced: 'Опытный' },
  goal: { captain: 'Стать капитаном', cruise: 'Круиз', skills: 'Повысить уровень', family: 'Семейный отдых' },
  destination: { turkey: 'Турция', thailand: 'Таиланд', any: 'Нужен совет' },
  season: { spring: 'Весна', summer: 'Лето', autumn: 'Осень', winter: 'Зима', flexible: 'Гибко' },
};

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { 'Content-Type': 'application/json', 'X-Admin-Key': adminKey, ...(options.headers || {}) },
  });
  if (!response.ok) throw new Error(response.status === 401 ? 'Неверный ключ администратора' : 'Ошибка загрузки данных');
  return response.json();
}

function statusSelect(lead) {
  const select = document.createElement('select');
  select.className = 'status-select';
  const statuses = { new: 'Новая', contacted: 'Связались', qualified: 'Квалифицирована', closed: 'Закрыта' };
  for (const [value, text] of Object.entries(statuses)) {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = text;
    option.selected = lead.status === value;
    select.append(option);
  }
  select.addEventListener('change', async () => {
    select.disabled = true;
    try {
      await api(`/api/admin/leads/${lead.id}`, { method: 'PATCH', body: JSON.stringify({ status: select.value }) });
    } finally {
      select.disabled = false;
    }
  });
  return select;
}

function textCell(...lines) {
  const cell = document.createElement('td');
  lines.filter(Boolean).forEach((line, index) => {
    const element = document.createElement(index === 0 ? 'strong' : 'span');
    element.textContent = line;
    cell.append(element);
  });
  return cell;
}

async function loadLeads() {
  const filter = document.querySelector('#status-filter').value;
  const data = await api(`/api/admin/leads${filter ? `?status=${encodeURIComponent(filter)}` : ''}`);
  document.querySelector('#total-leads').textContent = data.total;
  const table = document.querySelector('#leads-table');
  table.replaceChildren(...data.items.map((lead) => {
    const row = document.createElement('tr');
    const statusCell = document.createElement('td');
    statusCell.append(statusSelect(lead));
    row.append(
      textCell(lead.name, new Date(lead.created_at).toLocaleString('ru-RU')),
      textCell(labels.goal[lead.goal], `${labels.experience[lead.experience]} · ${labels.destination[lead.destination]} · ${labels.season[lead.season]}`),
      textCell(lead.recommended_program, lead.comment || ''),
      textCell(lead.phone, lead.email),
      statusCell,
    );
    return row;
  }));
  document.querySelector('#empty-table').hidden = data.items.length > 0;
}

async function enterDashboard() {
  try {
    await loadLeads();
    sessionStorage.setItem('yachtdream_admin_key', adminKey);
    loginPanel.hidden = true;
    dashboard.hidden = false;
    adminError.hidden = true;
  } catch (error) {
    adminError.textContent = error.message;
    adminError.hidden = false;
  }
}

document.querySelector('#admin-login-form').addEventListener('submit', (event) => {
  event.preventDefault();
  adminKey = document.querySelector('#admin-key').value;
  enterDashboard();
});
document.querySelector('#status-filter').addEventListener('change', loadLeads);
document.querySelector('#logout-button').addEventListener('click', () => {
  sessionStorage.removeItem('yachtdream_admin_key');
  window.location.reload();
});

if (adminKey) enterDashboard();

