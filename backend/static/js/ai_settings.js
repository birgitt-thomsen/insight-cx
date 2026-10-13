function updateTemperatureUI(modelId, temperatureId, noteId) {
    const model = document.getElementById(modelId);
    const temperature = document.getElementById(temperatureId);
    const note = document.getElementById(noteId);

    if (!model || !temperature || !note) {
        console.error("Temperature UI setup failed");
        return;
    }

    function refresh() {
        const selected = model.options[model.selectedIndex];
        const ignoresTemperature = !selected
            || selected.dataset.supportsTemperature !== "true";

        temperature.readOnly = ignoresTemperature;

        temperature.classList.toggle(
            "readonly-field",
            ignoresTemperature
        );

        note.style.display = ignoresTemperature ? "block" : "none";
    }

    model.addEventListener("change", refresh);
    refresh();
}

function disableGenerateSummaryButton() {

    const button = document.getElementById(
        "generate-summary-button"
    );

    button.disabled = true;

    button.innerText =
        "Generating Executive Summary...";
}