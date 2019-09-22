// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

//Link da view que retorna o JSON com os dados
var endpoint = 'http://localhost:8000/inout/api/chart/pie/'
var data = []
var labels = [];

$.ajax({
  method: "GET",
  url: endpoint,
  success: function(dados_grafico_pie){
    labels = dados_grafico_pie.tiposDeDocumento
    data = dados_grafico_pie.quantidadeTipoDocumento
    setChartPie();
  },
  erro: function(error_data){
    console.log("error")
    console.log(error_data)
  }
})
function setChartPie() {
  // Pie Chart Example
  var ctx = document.getElementById("myPieChart");
  var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        // Define as cores das fatias do gráfico
        //backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#F6A6FF', '#BFFCC6', '#D5AAFF', '#E7FFAC', '#AFCBFF'],
        backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#858796', '#E7FFAC', '#AFCBFF'],
        hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
        hoverBorderColor: "rgba(234, 236, 244, 1)",
      }],
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
      },
      legend: {
        display: false
      },
      cutoutPercentage: 80,
    },
  });
}