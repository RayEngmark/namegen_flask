const tags = document.querySelectorAll(".tag");
const generateBtn = document.getElementById("generateBtn");
const nameOutput = document.getElementById("nameOutput");
const resultBox = document.getElementById("resultBox");

tags.forEach(tag => {
  tag.addEventListener("click", () => {
    tag.classList.toggle("active");
  });
});

generateBtn.addEventListener("click", async () => {
  const selectedTags = Array.from(document.querySelectorAll(".tag.active")).map(tag => tag.innerText.trim());
  const vibe = document.getElementById("vibe").value;

  const res = await fetch("/generate-name", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tags: selectedTags, vibe })
  });

  const data = await res.json();
  nameOutput.innerText = data.name;
  resultBox.classList.remove("hidden");
});
