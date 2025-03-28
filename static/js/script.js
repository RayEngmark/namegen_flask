async function generateName() {
  const vibe = document.getElementById("vibe").value;
  const count = parseInt(document.getElementById("count").value) || 4;
  const selectedTags = Array.from(document.getElementById("tagSelect").selectedOptions).map(o => o.value);
  const grid = document.getElementById("nameGrid");
  grid.innerHTML = "";

  for (let i = 0; i < count; i++) {
    const shimmer = document.createElement("div");
    shimmer.className = "name-box shimmer";
    shimmer.textContent = "Generating...";
    grid.appendChild(shimmer);
  }

  const res = await fetch("/generate-name", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tags: selectedTags, vibe, count })
  });

  const data = await res.json();
  const names = Array.isArray(data.names) ? data.names : [];

  grid.innerHTML = "";
  names.forEach(item => {
    const card = document.createElement("div");
    card.className = "name-box";
    card.textContent = item.name || item;
    grid.appendChild(card);
  });
}
