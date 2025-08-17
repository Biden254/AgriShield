// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Timeline Chart
    const timelineCtx = document.getElementById('timelineChart').getContext('2d');
    new Chart(timelineCtx, {
        type: 'line',
        data: {
            labels: ['Today', 'Day 2', 'Day 3', 'Day 4', 'Day 5'],
            datasets: [
                {
                    label: 'Scientific Prediction',
                    data: [25, 40, 55, 70, 80],
                    borderColor: '#1976D2',
                    backgroundColor: 'rgba(25, 118, 210, 0.1)',
                    tension: 0.3,
                    fill: true
                },
                {
                    label: 'Community Reports',
                    data: [30, 45, 60, 75, 85],
                    borderColor: '#FFA000',
                    backgroundColor: 'rgba(255, 160, 0, 0.1)',
                    tension: 0.3,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false
                },
                legend: {
                    display: false
                },
                annotation: {
                    annotations: {
                        dangerZone: {
                            type: 'box',
                            yMin: 70,
                            yMax: 100,
                            backgroundColor: 'rgba(255, 0, 0, 0.1)',
                            borderWidth: 0
                        }
                    }
                }
            },
            scales: {
                y: {
                    min: 0,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });

    // Historical Chart
    const historicalCtx = document.getElementById('historicalChart').getContext('2d');
    new Chart(historicalCtx, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [
                {
                    label: 'Flood Events',
                    data: [2, 1, 3, 0, 0, 0, 5, 4, 3, 2, 1, 2],
                    backgroundColor: '#D32F2F'
                },
                {
                    label: 'Rainfall (mm)',
                    data: [120, 110, 150, 200, 180, 90, 250, 230, 190, 170, 140, 130],
                    type: 'line',
                    borderColor: '#1976D2',
                    backgroundColor: 'transparent'
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Flood Events'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    grid: {
                        drawOnChartArea: false
                    },
                    title: {
                        display: true,
                        text: 'Rainfall (mm)'
                    }
                }
            }
        }
    });
});