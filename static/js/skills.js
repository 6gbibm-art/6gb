const ALL_SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "TypeScript",
    "React",
    "Angular",
    "Vue",
    "Node.js",
    "Express",
    "FastAPI",
    "Flask",
    "Django",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Redis",
    "Docker",
    "Kubernetes",
    "Git",
    "AWS",
    "Azure",
    "GCP",
    "Power BI",
    "Excel",
    "Pandas",
    "NumPy",
    "TensorFlow",
    "PyTorch",
    "Scikit-Learn"
];

let selectedSkills = [];

let filteredSkills = [];
if (filteredSkills.length > 0)
    highlightedIndex = 0;
else
    highlightedIndex = -1;

renderSuggestions();

function getSelectedSkills() {
    return selectedSkills;
}

document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("skill-input");

    if (!input) return;

    input.addEventListener("input", () => {

        const value = input.value.trim().toLowerCase();

        highlightedIndex = -1;

        if (!value) {
            clearSuggestions();
            return;
        }

        filteredSkills = ALL_SKILLS
            .filter(skill =>
                skill.toLowerCase().includes(value) &&
                !selectedSkills.includes(skill)
            )
            .slice(0, 8);
        if (filteredSkills.length > 0)
            highlightedIndex = 0;
        else
            highlightedIndex = -1;

        renderSuggestions();

    });

    input.addEventListener("keydown", (e) => {

        if (e.key === "ArrowDown") {

            e.preventDefault();

            if (!filteredSkills.length) return;

            highlightedIndex++;

            if (highlightedIndex >= filteredSkills.length)
                highlightedIndex = 0;

            renderSuggestions();

            return;

        }

        if (e.key === "ArrowUp") {

            e.preventDefault();

            if (!filteredSkills.length) return;

            highlightedIndex--;

            if (highlightedIndex < 0)
                highlightedIndex = filteredSkills.length - 1;

            renderSuggestions();

            return;

        }

        if (e.key === "Enter") {

            e.preventDefault();

            if (highlightedIndex >= 0) {

                addSkill(filteredSkills[highlightedIndex]);

                clearSuggestions();

                return;

            }

            const value = input.value.trim();

            if (!value) return;

            const match = ALL_SKILLS.find(
                skill => skill.toLowerCase() === value.toLowerCase()
            );

            if (match)
                addSkill(match);

            clearSuggestions();

            return;

        }

        // Gmail / LinkedIn behaviour
        if (e.key === "Backspace" &&
            input.value === "" &&
            selectedSkills.length > 0) {

            removeSkill(selectedSkills[selectedSkills.length - 1]);

        }

    });

});

function renderSuggestions() {

    const suggestions = document.getElementById("skill-suggestions");

    suggestions.innerHTML = "";

    filteredSkills.forEach((skill, index) => {

        const div = document.createElement("div");

        div.className = "skill-option";

        if (index === highlightedIndex)
            div.classList.add("active");

        div.textContent = skill;

        div.onclick = () => {

            addSkill(skill);

            clearSuggestions();

        };

        suggestions.appendChild(div);

    });

    suggestions.style.display =
        filteredSkills.length ? "block" : "none";

}

function clearSuggestions() {

    const suggestions = document.getElementById("skill-suggestions");
    const input = document.getElementById("skill-input");

    input.value = "";

    filteredSkills = [];

    highlightedIndex = -1;

    suggestions.innerHTML = "";

    suggestions.style.display = "none";

}

function addSkill(skill) {

    if (selectedSkills.includes(skill))
        return;

    selectedSkills.push(skill);

    renderSkills();

}

function removeSkill(skill) {

    selectedSkills = selectedSkills.filter(s => s !== skill);

    renderSkills();

}

function renderSkills() {

    const container = document.getElementById("selected-skills");
    const input = document.getElementById("skill-input");

    container.innerHTML = "";

    selectedSkills.forEach(skill => {

        const pill = document.createElement("div");

        pill.className = "skill-pill";

        pill.innerHTML = `
            <span>${skill}</span>
            <span class="remove-skill">&times;</span>
        `;

        pill.querySelector(".remove-skill").onclick = () =>
            removeSkill(skill);

        container.appendChild(pill);

    });

    container.appendChild(input);

    input.focus();

}