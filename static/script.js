const API = 'http://127.0.0.1:5000';

function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}
function goHome() { showScreen('home'); }

function toast(msg, type = 'inf') {
    const el = document.createElement('div');
    el.className = `toast toast-${type}`;
    el.innerText = msg;
    document.getElementById('toasts').appendChild(el);
    setTimeout(() => el.remove(), 3000);
}

async function bookTicket() {
    const data = {
        booking_date: document.getElementById('bDate').value,
        class: document.getElementById('bClass').value,
        fare: document.getElementById('bFare').value
    };
    const res = await fetch(`${API}/add`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    if(res.ok) { toast('Booked!', 'ok'); goHome(); }
}

async function loadTickets() {
    const res = await fetch(`${API}/tickets`);
    const data = await res.json();
    const html = data.map(t => `<tr><td>#${t.id}</td><td>${t.booking_date}</td><td>${t.class}</td><td>₹${t.fare}</td></tr>`).join('');
    document.getElementById('ticketTable').innerHTML = `<table><thead><tr><th>ID</th><th>Date</th><th>Class</th><th>Fare</th></tr></thead><tbody>${html}</tbody></table>`;
}

async function updateTicket() {
    const id = document.getElementById('uId').value;
    const data = { class: document.getElementById('uClass').value, fare: document.getElementById('uFare').value };
    const res = await fetch(`${API}/update/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    if(res.ok) toast('Updated!', 'ok');
}

async function cancelTicket() {
    const id = document.getElementById('cId').value;
    const res = await fetch(`${API}/delete/${id}`, { method: 'DELETE' });
    if(res.ok) toast('Cancelled!', 'ok');
}