document.addEventListener("DOMContentLoaded", function() {
    // Validación para formularios con input file (si aplica)
    const fileInput = document.querySelector("input[type='file']");
    const form = document.querySelector("form");
    if (fileInput && form) {
        form.addEventListener("submit", function(event) {
            if (!fileInput.files.length) {
                alert("Por favor, selecciona un archivo CSV antes de subir.");
                event.preventDefault();
                return;
            }
            const fileName = fileInput.files[0].name;
            const fileExtension = fileName.split(".").pop().toLowerCase();
            if (fileExtension !== "csv") {
                alert("Solo se permiten archivos CSV.");
                event.preventDefault();
            }
        });
    }

    // Mensaje de carga de página
    console.log("Página cargada.");

    // Lógica para mostrar opciones de gráficos
    const chartTypeSelect = document.getElementById("chart-type");
    const chartContainer = document.getElementById("chart-container");
    if (chartTypeSelect && chartContainer) {
        chartTypeSelect.addEventListener("change", function() {
            const selectedChart = chartTypeSelect.value;
            const chartOptions = chartContainer.getElementsByClassName("chart-option");
            Array.from(chartOptions).forEach(option => option.style.display = 'none');
            const selectedOption = document.getElementById(selectedChart);
            if (selectedOption) selectedOption.style.display = 'block';
        });
    }

    // Gestión de selección de columnas para outliers
    const columnCheckboxes = document.querySelectorAll('input[name="columns"]');
    columnCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            console.log("Cambio en la selección de columnas:", this.value);
        });
    });

    // Confirmación al hacer clic en el botón de guardar
    const saveButton = document.getElementById("save-button");
    if (saveButton) {
        saveButton.addEventListener('click', function(event) {
            const userConfirmed = confirm("¿Estás seguro de que deseas guardar los cambios?");
            if (!userConfirmed) {
                event.preventDefault();
            }
        });
    }

    // Selección de modelos de Machine Learning
    const modelSelect = document.getElementById("ml-model");
    const hyperparametersContainer = document.getElementById("hyperparameters-container");

    if (modelSelect && hyperparametersContainer) {
        modelSelect.addEventListener("change", function() {
            const selectedModel = modelSelect.value;
            console.log("Modelo seleccionado:", selectedModel);

            // Mostrar campos de hiperparámetros según el modelo
            const allHyperparameters = document.querySelectorAll(".hyperparameter-option");
            allHyperparameters.forEach(option => option.style.display = 'none');

            const selectedHyperparameters = document.getElementById(`${selectedModel}-params`);
            if (selectedHyperparameters) selectedHyperparameters.style.display = 'block';
        });
    }

    // Manejo de outliers - Mostrar opciones dinámicas
    const outlierMethodSelect = document.getElementById("outlier-method");
    const outlierOptionsContainer = document.getElementById("outlier-options");

    if (outlierMethodSelect && outlierOptionsContainer) {
        outlierMethodSelect.addEventListener("change", function() {
            const selectedMethod = outlierMethodSelect.value;
            console.log("Método de tratamiento de outliers seleccionado:", selectedMethod);

            const allOutlierOptions = document.querySelectorAll(".outlier-option");
            allOutlierOptions.forEach(option => option.style.display = 'none');

            const selectedOption = document.getElementById(`${selectedMethod}-options`);
            if (selectedOption) selectedOption.style.display = 'block';
        });
    }

    // Cargar y mostrar métricas de modelos
    const metricsButton = document.getElementById("metrics-button");
    const metricsContainer = document.getElementById("metrics-container");

    if (metricsButton && metricsContainer) {
        metricsButton.addEventListener("click", function() {
            console.log("Cargando métricas...");
            fetch("/get_metrics")  // Asumiendo que tienes una ruta en Flask que devuelve métricas
                .then(response => response.json())
                .then(data => {
                    metricsContainer.innerHTML = `<p>R²: ${data.r2}</p><p>MAE: ${data.mae}</p><p>RMSE: ${data.rmse}</p>`;
                })
                .catch(error => console.error("Error al obtener métricas:", error));
        });
    }
});
document.addEventListener("DOMContentLoaded", function() {
    // Validación para formularios
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function(event) {
            const questionInput = document.getElementById("question");
            if (!questionInput.value.trim()) {
                alert("Por favor, ingresa una pregunta para analizar.");
                event.preventDefault();
            }
        });
    }

    // Lógica para mostrar resultados de análisis
    const resultSection = document.querySelector(".analysis-result");
    if (resultSection) {
        const analysisResult = document.querySelector(".result-content");
        analysisResult.style.display = 'block';  // Mostrar la sección de resultados
    }

    // Gestión de selección de columnas
    const columnCheckboxes = document.querySelectorAll('input[name="columns"]');
    columnCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            console.log("Cambio en la selección de columnas:", this.value);
        });
    });
});
