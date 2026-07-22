function updateTemperatureUI(modelId, temperatureId, noteId) {
    const model = document.getElementById(modelId);
    const temperature = document.getElementById(temperatureId);
    const note = document.getElementById(noteId);

    if (!model || !temperature || !note) {
        console.error("Temperature UI setup failed");
        return;
    }

    function refresh() {
        const isGpt5 = model.value.startsWith("gpt-5");

        temperature.readOnly = isGpt5;

        temperature.classList.toggle(
            "readonly-field",
            isGpt5
        );

        note.style.display = isGpt5 ? "block" : "none";
    }

    model.addEventListener("change", refresh);
    refresh();
}
