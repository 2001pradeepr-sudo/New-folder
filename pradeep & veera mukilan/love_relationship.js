const sideOnePoints = [
  "Loyal support",
  "Kind words",
  "Happy moments together",
  "Trust and honesty"
];

const sideTwoPoints = [
  "Care and affection",
  "Understanding each other",
  "Fun and laughter",
  "Shared dreams"
];

const advantages = [
  "They support each other",
  "They share love and care",
  "They build trust together",
  "They enjoy happy memories"
];

const disadvantages = [
  "Small misunderstandings can happen",
  "Arguments may create stress",
  "Jealousy can hurt the bond",
  "Distance or time issues may affect them"
];

function renderList(elementId, items) {
  const list = document.getElementById(elementId);
  list.innerHTML = "";

  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    list.appendChild(li);
  });
}

function updateRelationship() {
  const person1 = document.getElementById("person1").value.trim() || "Aisha";
  const person2 = document.getElementById("person2").value.trim() || "Arjun";

  document.getElementById("name1").textContent = person1;
  document.getElementById("name2").textContent = person2;
  document.getElementById("relationshipTitle").textContent = `${person1} and ${person2}`;

  renderList("side1", sideOnePoints);
  renderList("side2", sideTwoPoints);
  renderList("advantagesList", advantages);
  renderList("disadvantagesList", disadvantages);
}

updateRelationship();
