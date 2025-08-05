
// document.addEventListener('DOMContentLoaded', () => {
//   function formatDateLabel(dateString) {
//     const date = new Date(dateString);
//     if (isNaN(date)) return dateString;
//     const day = date.getDate();
//     const month = date.toLocaleString('default', { month: 'short' });
//     const getOrdinal = (n) => {
//       const s = ["th", "st", "nd", "rd"];
//       const v = n % 100;
//       return n + (s[(v - 20) % 10] || s[v] || s[0]);
//     };
//     return `${getOrdinal(day)} ${month}`;
//   }

//   const formattedAllDates = allDates.map(formatDateLabel);

//   // @ts-ignore
//   const allDates = window.dates || [];
//   const allVisitCounts = window.totals || [];
//   const typeLabels = window.typeLabels || [];
//   const typeCounts = window.typeCounts || [];


//   const lineChartOptions = {
//     chart: {
//       type: 'line',
//       height: 350,
//       toolbar: { show: false }
//     },
//     series: [{ name: 'Visits', data: allVisitCounts }],
//     xaxis: {
//       categories: formattedAllDates ,
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

//   const lineChartEl = document.querySelector("#lineChart");
//   const barChartEl = document.querySelector("#barChart");
//   const visitTypeSelect = document.getElementById('visitType');
//   const barChartContainer = document.getElementById('barChartContainer');
//   const chartSection = document.querySelector('.charts');

//   const lineChart = new ApexCharts(lineChartEl, lineChartOptions);
//   const barChart = new ApexCharts(barChartEl, barChartOptions);

//   lineChart.render();
//   barChart.render();

//   function updateCharts() {
//     const selectedType = visitTypeSelect.value.trim();

//     if (selectedType === 'All') {
//       barChartContainer.style.display = 'block';
//       chartSection.classList.remove('single-chart');

//       lineChart.updateOptions({ xaxis: { categories: formattedAllDates } });
//       lineChart.updateSeries([{ name: 'All Visits', data: allVisitCounts }]);

//       barChart.updateOptions({
//         xaxis: { categories: typeLabels, labels: { style: { colors: '#2e7d32' } } },
//         colors: ['#66bb6a', '#81c784', '#a5d6a7', '#c8e6c9']
//       });
//       barChart.updateSeries([{ name: 'Count', data: typeCounts }]);
//     } else {
//       barChartContainer.style.display = 'none';
//       chartSection.classList.add('single-chart');
//     }

//     // Update table rows
//     const tableRows = document.querySelectorAll('tbody tr');
//     tableRows.forEach(row => {
//       const visitTypeCell = row.querySelectorAll('td')[0];
//       const visitType = visitTypeCell.textContent.trim();
//       row.style.display = (selectedType === 'All' || visitType === selectedType) ? '' : 'none';
//     });
//   }

//   updateCharts();

//   visitTypeSelect.addEventListener('change', () => {
//     document.getElementById('filterForm').submit();
//   });
// });


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

  // Data from Django context
  const allDates = window.allDates || [];
  const allVisitCounts = window.allVisitCounts || [];
  const typeLabels = window.typeLabels || [];
  const typeCounts = window.typeCounts || [];

  const formattedAllDates = allDates.map(formatDateLabel);

  // Chart containers and dropdown
  const lineChartEl = document.querySelector("#lineChart");
  const barChartEl = document.querySelector("#barChart");
  const durationSelect = document.getElementById('duration');
  const barChartContainer = document.getElementById('barChartContainer');
  const chartSection = document.querySelector('.charts');

  const lineChartOptions = {
    chart: {
      type: 'line',
      height: 350,
      toolbar: { show: false }
    },
    series: [{ name: 'Visits', data: allVisitCounts }],
    xaxis: {
      categories: formattedAllDates,
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

  const lineChart = new ApexCharts(lineChartEl, lineChartOptions);
  const barChart = new ApexCharts(barChartEl, barChartOptions);

  lineChart.render();
  barChart.render();

  function updateCharts() {
    const selectedDuration = durationSelect.value.trim();
    let categories = formattedAllDates;
    let seriesName = 'Visits';
    let data = allVisitCounts;

    if (selectedDuration === 'week') {
      categories = formattedAllDates.slice(-7);
      data = allVisitCounts.slice(-7);
      seriesName = 'Weekly Visits';
    } else if (selectedDuration === 'month') {
      categories = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
      data = allVisitCounts.slice(-4);
      seriesName = 'Monthly Visits';
    } else if (selectedDuration === 'year') {
      categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      data = allVisitCounts.slice(0, 12);
      seriesName = 'Yearly Visits';
    } else if (selectedDuration === 'all') {
      categories = formattedAllDates;
      data = allVisitCounts;
      seriesName = 'All Visits';
    }

    // Update Line Chart
    lineChart.updateOptions({ xaxis: { categories } });
    lineChart.updateSeries([{ name: seriesName, data }]);

    // Update Bar Chart
    if (selectedDuration === 'all') {
      barChartContainer.style.display = 'block';
      chartSection.classList.remove('single-chart');

      barChart.updateOptions({ xaxis: { categories: typeLabels } });
      barChart.updateSeries([{ name: 'Count', data: typeCounts }]);
    } else {
      barChartContainer.style.display = 'none';
      chartSection.classList.add('single-chart');
    }
  }

  updateCharts();

  durationSelect.addEventListener('change', () => {
    document.getElementById('filterForm').submit();
  });
});
