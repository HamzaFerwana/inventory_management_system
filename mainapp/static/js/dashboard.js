document.addEventListener('DOMContentLoaded', function() {
  var expensesVal = parseFloat(document.getElementById('donut-chart')?.dataset.expenses || 0) || 0;
  var purchasesVal = parseFloat(document.getElementById('donut-chart')?.dataset.purchases || 0) || 0;
  
  console.log('Total Expenses:', expensesVal);
  console.log('Total Purchases:', purchasesVal);
  
  if (document.getElementById('donut-chart')) {
    var donutChart = {
      chart: {
        height: 350,
        type: 'donut',
        toolbar: { show: false }
      },
      series: [expensesVal, purchasesVal],
      colors: ['#ea5455', '#28c76f'],
      labels: ['Expenses', 'Purchases'],
      responsive: [
        {
          breakpoint: 480,
          options: {
            chart: { width: 200 },
            legend: { position: 'bottom' }
          }
        }
      ]
    };
    var donut = new ApexCharts(document.querySelector("#donut-chart"), donutChart);
    donut.render();
  }
});
