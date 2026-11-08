// UI only: renders what the server returns. No booking rules live here.
const $ = (id) => document.getElementById(id);
let selectedRoom = null;

async function api(path, options) {
  const res = await fetch(path, options);
  return res.json();
}

function selectedEquipment() {
  return [...document.querySelectorAll("#equipment input:checked")].map((i) => i.value);
}

function renderRooms(data) {
  $("search-error").textContent = data.error || "";
  $("empty").hidden = !data.empty;
  const list = $("rooms");
  list.innerHTML = "";
  for (const r of data.rooms) {
    const li = document.createElement("li");
    li.dataset.id = r.id;
    if (r.id === selectedRoom) li.className = "sel";
    li.innerHTML = `<strong>${r.name}</strong> <span class="tag ${r.status}">${r.status}</span>
      <div class="muted">Capacity ${r.capacity} · ${r.equipment.join(", ") || "no equipment"}</div>`;
    const b = document.createElement("button");
    b.textContent = "Select";
    b.onclick = () => selectRoom(r);
    li.appendChild(b);
    list.appendChild(li);
  }
}

function selectRoom(r) {
  selectedRoom = r.id;
  $("selected").textContent = r.name;
  $("bookings").innerHTML = r.bookings.length
    ? r.bookings.map((b) => `<li>Booked ${b}</li>`).join("") : "<li>No bookings</li>";
  document.querySelectorAll("#rooms li").forEach((li) => (li.className = li.dataset.id === r.id ? "sel" : ""));
  $("result").textContent = "";
  $("result").className = "result";
  if ($("start").value && $("end").value) check();   // F5: re-check for the new room
}

async function search() {
  const q = new URLSearchParams({ participants: $("participants").value, equipment: selectedEquipment().join(",") });
  renderRooms(await api("/api/rooms?" + q));
}

async function check() {
  const out = await api("/api/check", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ room: selectedRoom, start: $("start").value, end: $("end").value }),
  });
  $("result").textContent = (out.room ? out.room + ": " : "") + out.message;
  $("result").className = "result " + (out.available ? "ok" : "bad");
}

async function init() {
  const cfg = await api("/api/config");
  $("nowline").textContent = `Current time is fixed at ${cfg.nowText} (${cfg.now} minutes). Max booking ${cfg.maxLength} min.`;
  $("equipment").innerHTML = cfg.equipment.map((e) => `<label><input type="checkbox" value="${e}"> ${e}</label>`).join("");
  $("equipment").addEventListener("change", search);
  $("participants").addEventListener("input", search);
  $("check").addEventListener("click", check);
  search();
}
init();
