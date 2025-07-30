document.addEventListener('DOMContentLoaded', function () {
  function formatDateLabel(dateString) {
    const date = new Date(dateString);
    const day = date.getDate();
    const month = date.toLocaleString('default', { month: 'long' });
    const getOrdinal = (n) => {
      const s = ["th", "st", "nd", "rd"];
      const v = n % 100;
      return n + (s[(v - 20) % 10] || s[v] || s[0]);
    };
    return `${getOrdinal(day)} ${month}`;
  }

  // These variables come from Django template context via <script> in dashboard.html
  // They must be arrays, so Django context must use |safe and JSON-serializable lists.
  const allDates = window.allDates || [];
  const allVisitCounts = window.allVisitCounts || [];
  const typeLabels = window.typeLabels || [];
  const typeCounts = window.typeCounts || [];

  // Format dates for x-axis labels
  const formattedAllDates = allDates.map(formatDateLabel);

  const dashboardData = JSON.parse(document.getElementById('dashboard-data').textContent);


  // Initialize line chart (Visits Over Time)
  const lineChartOptions = {
    chart: {
      type: 'line',
      height: 350,
      toolbar: { show: false }
    },
    series: [{
      name: 'All Visits',
      data: allVisitCounts
    }],
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

  const lineChart = new ApexCharts(document.querySelector("#lineChart"), lineChartOptions);
  lineChart.render();

  // Initialize bar chart (Distribution by Type)
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

  const barChart = new ApexCharts(document.querySelector("#barChart"), barChartOptions);
  barChart.render();

  // === Filter dropdown change ===
  document.getElementById('visitType').addEventListener('change', function () {
    const selectedType = this.value.trim();
    const barChartContainer = document.getElementById('barChart').parentElement;
    const chartSection = document.querySelector('.charts');

    if (selectedType === 'All') {
      barChartContainer.style.display = 'block';
      chartSection.classList.remove('single-chart');

      lineChart.updateOptions({ xaxis: { categories: formattedAllDates } });
      lineChart.updateSeries([{ name: 'All Visits', data: allVisitCounts }]);

      barChart.updateOptions({
        xaxis: {
          categories: typeLabels,
          labels: { style: { colors: '#2e7d32' } }
        },
        colors: ['#66bb6a', '#81c784', '#a5d6a7', '#c8e6c9']
      });
      barChart.updateSeries([{ name: 'Count', data: typeCounts }]);
    } else {
      // For simplicity, when a specific type is selected,
      // hide bar chart and show only line chart filtered to that type.
      barChartContainer.style.display = 'none';
      chartSection.classList.add('single-chart');

      // You need to get filtered data for the selected type.
      // For now, use placeholder empty data (you should implement filtering backend or JS)
      lineChart.updateOptions({ xaxis: { categories: [selectedType] } });
      lineChart.updateSeries([{
        name: `${selectedType}s`,
        data: [0]
      }]);
    }

    // Filter table rows
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
      const visitTypeCell = row.querySelectorAll('td')[0]; // column 0 = Visit Type
      const visitType = visitTypeCell.textContent.trim();
      row.style.display = (selectedType === 'All' || visitType === selectedType) ? '' : 'none';
    });
  });
});
