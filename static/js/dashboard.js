const ctx = document.getElementById("themeChart");

if (ctx) {
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: themeLabels,
            datasets: [
                {
                    label: "Feedback",
                    data: themeCounts
                }
            ]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
            legend: {
                display: false // Hides the top legend labels
                }
            },
            scales: {
                x: {
                    display: false, // Hides all the x-axis grid lines
                    ticks: {
                        display: false // Hides X-axis labels
                    },
                    grid: {
                        display: false,
                    },
                },
                y: {
                    grid: {
                        display: false
                    }
                },
            }
        }
    });
}