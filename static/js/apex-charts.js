// document.addEventListener('DOMContentLoaded', function () {
//   function formatDateLabel(dateString) {
//     const date = new Date(dateString);
//     const day = date.getDate();
//     const month = date.toLocaleString('default', { month: 'long' });
//     const getOrdinal = (n) => {
//       const s = ["th", "st", "nd", "rd"];
//       const v = n % 100;
//       return n + (s[(v - 20) % 10] || s[v] || s[0]);
//     };
//     return `${getOrdinal(day)} ${month}`;
//   }

//   // Variables passed from Django template
//   const allDates = window.allDates || [];
//   const allVisitCounts = window.allVisitCounts || [];
//   const typeLabels = window.typeLabels || [];
//   const typeCounts = window.typeCounts || [];

//   // Format dates for x-axis labels
//   const formattedAllDates = allDates.map(formatDateLabel);

//   // Initialize line chart
//   const lineChartOptions = {
//     chart: {
//       type: 'line',
//       height: 350,
//       toolbar: { show: false }
//     },
//     series: [{
//       name: 'All Visits',
//       data: allVisitCounts
//     }],
//     xaxis: {
//       categories: formattedAllDates,
//       labels: { style: { colors: '#2e7d32' } }
//     },
//     stroke: { curve: 'smooth' },
//     markers: {
//       size: 5,
//       colors: ['#388e3c'],
//       strokeColors: '#43a047',
//       strokeWidth: 2
//     },
//     fill: {
//       type: 'gradient',
//       gradient: {
//         shadeIntensity: 1,
//         opacityFrom: 0.2,
//         opacityTo: 0.0,
//         stops: [0, 90, 100]
//       }
//     },
//     colors: ['#43a047'],
//     legend: { show: false }
//   };
//   const lineChart = new ApexCharts(document.querySelector("#lineChart"), lineChartOptions);
//   lineChart.render();

//   // Initialize bar chart
//   const barChartOptions = {
//     chart: {
//       type: 'bar',
//       height: 350,
//       toolbar: { show: false },
//       animations: { enabled: true }
//     },
//     series: [{ name: 'Count', data: typeCounts }],
//     plotOptions: {
//       bar: {
//         borderRadius: 6,
//         distributed: true,
//         columnWidth: '50%'
//       }
//     },
//     colors: ['#66bb6a', '#81c784', '#a5d6a7', '#c8e6c9'],
//     xaxis: {
//       categories: typeLabels,
//       labels: { style: { colors: '#2e7d32' } }
//     },
//     yaxis: {
//       labels: { style: { colors: '#2e7d32' } },
//       min: 0
//     },
//     legend: { show: false }
//   };
//   const barChart = new ApexCharts(document.querySelector("#barChart"), barChartOptions);
//   barChart.render();

//   // Elements
//   const visitTypeSelect = document.getElementById('visitType');
//   const barChartContainer = document.getElementById('barChartContainer');
//   const chartSection = document.querySelector('.charts');

//   // Handle visit type change
//   function handleVisitTypeChange() {
//     const selectedType = visitTypeSelect.value.trim();

//     if (selectedType === 'All') {
//       // Show bar chart and full line chart
//       barChartContainer.style.display = 'block';
//       chartSection.classList.remove('single-chart');

//       lineChart.updateOptions({ xaxis: { categories: formattedAllDates } });
//       lineChart.updateSeries([{ name: 'All Visits', data: allVisitCounts }]);

//       barChart.updateOptions({
//         xaxis: {
//           categories: typeLabels,
//           labels: { style: { colors: '#2e7d32' } }
//         },
//         colors: ['#66bb6a', '#81c784', '#a5d6a7', '#c8e6c9']
//       });
//       barChart.updateSeries([{ name: 'Count', data: typeCounts }]);
//     } else {
//       // Hide bar chart and update line chart for selected visit type
//       barChartContainer.style.display = 'none';
//       chartSection.classList.add('single-chart');

//       // TODO: Replace this with real filtered data from backend or JS
//       lineChart.updateOptions({ xaxis: { categories: [selectedType] } });
//       lineChart.updateSeries([{
//         name: `${selectedType}s`,
//         data: [0]  // Placeholder count, update with real data when available
//       }]);
//     }

//     // Filter table rows based on selected type
//     const tableRows = document.querySelectorAll('tbody tr');
//     tableRows.forEach(row => {
//       const visitTypeCell = row.querySelectorAll('td')[0]; // Assuming first cell is visit type
//       const visitType = visitTypeCell.textContent.trim();
//       row.style.display = (selectedType === 'All' || visitType === selectedType) ? '' : 'none';
//     });
//   }

//   // Run once on page load
//   handleVisitTypeChange();

//   // Attach event listener
//   visitTypeSelect.addEventListener('change', handleVisitTypeChange);
// });

// 



document.addEventListener('DOMContentLoaded', () => {
  function formatDateLabel(dateString) {
    const date = new Date(dateString);
    if (isNaN(date)) return dateString;
    const day = date.getDate();
    const month = date.toLocaleString('default', { month: 'short' });
    const getOrdinal = (n) => {
      const s = ["th", "st", "nd", "rd"];
      const v = n % 100;
      return n + (s[(v - 20) % 10] || s[v] || s[0]);
    };
    return `${getOrdinal(day)} ${month}`;
  }

  const formattedAllDates = allDates.map(formatDateLabel);

  // @ts-ignore
  const allDates = window.dates || [];
  const allVisitCounts = window.totals || [];
  const typeLabels = window.typeLabels || [];
  const typeCounts = window.typeCounts || [];


  const lineChartOptions = {
    chart: {
      type: 'line',
      height: 350,
      toolbar: { show: false }
    },
    series: [{ name: 'Visits', data: allVisitCounts }],
    xaxis: {
      categories: formattedAllDates ,
      labels: { style: { colors: '#2e7d32' } }
    },
    stroke: { curve: 'smooth' },
    markers: {
      size: 5,
      colors: ['#388e3c'],
      strokeColors: '#43a047',
      strokeWidth: 2
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.2,
        opacityTo: 0.0,
        stops: [0, 90, 100]
      }
    },
    colors: ['#43a047'],
    legend: { show: false }
  };

  const barChartOptions = {
    chart: {
      type: 'bar',
      height: 350,
      toolbar: { show: false },
      animations: { enabled: true }
    },
    series: [{ name: 'Count', data: typeCounts }],
    plotOptions: {
      bar: {
        borderRadius: 6,
        distributed: true,
        columnWidth: '50%'
      }
    },
    colors: ['#66bb6a', '#81c784', '#a5d6a7', '#c8e6c9'],
    xaxis: {
      categories: typeLabels,
      labels: { style: { colors: '#2e7d32' } }
    },
    yaxis: {
      labels: { style: { colors: '#2e7d32' } },
      min: 0
    },
    legend: { show: false }
  };

  const lineChartEl = document.querySelector("#lineChart");
  const barChartEl = document.querySelector("#barChart");
  const visitTypeSelect = document.getElementById('visitType');
  const barChartContainer = document.getElementById('barChartContainer');
  const chartSection = document.querySelector('.charts');

  const lineChart = new ApexCharts(lineChartEl, lineChartOptions);
  const barChart = new ApexCharts(barChartEl, barChartOptions);

  lineChart.render();
  barChart.render();

  function updateCharts() {
    const selectedType = visitTypeSelect.value.trim();

    if (selectedType === 'All') {
      barChartContainer.style.display = 'block';
      chartSection.classList.remove('single-chart');

      lineChart.updateOptions({ xaxis: { categories: formattedAllDates } });
      lineChart.updateSeries([{ name: 'All Visits', data: allVisitCounts }]);

      barChart.updateOptions({
        xaxis: { categories: typeLabels, labels: { style: { colors: '#2e7d32' } } },
        colors: ['#66bb6a', '#81c784', '#a5d6a7', '#c8e6c9']
      });
      barChart.updateSeries([{ name: 'Count', data: typeCounts }]);
    } else {
      barChartContainer.style.display = 'none';
      chartSection.classList.add('single-chart');
    }

    // Update table rows
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
      const visitTypeCell = row.querySelectorAll('td')[0];
      const visitType = visitTypeCell.textContent.trim();
      row.style.display = (selectedType === 'All' || visitType === selectedType) ? '' : 'none';
    });
  }

  updateCharts();

  visitTypeSelect.addEventListener('change', () => {
    document.getElementById('filterForm').submit();
  });
});
