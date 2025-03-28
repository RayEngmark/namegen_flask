function generateName() {
  const tags = Array.from(document.getElementById("tagSelect").selectedOptions).map(opt => opt.value);
  const vibe = document.getElementById("vibe").value;
  const count = parseInt(document.getElementById("count").value) || 4;

  fetch("/generate-name", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ tags, vibe, count })
  })
    .then(res => res.json())
    .then(data => {
      const grid = document.getElementById("nameGrid");
      grid.innerHTML = "";
      data.names.forEach(name => {
        const card = document.createElement("div");
        card.className = "name-card";
        card.textContent = name.name || name; // support string or object
        grid.appendChild(card);
      });
    })
    .catch(err => {
      console.error("Error:", err);
    });
}
