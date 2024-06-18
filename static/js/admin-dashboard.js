/* globals Chart:false, feather:false */
$(document).ready(function() {

  $("#form_dashboard_graph").submit(function(event){
    $("#btn_load_seven_range").html(`<i class="fa-solid fa-spinner fa-spin-pulse"></i>`);

    event.preventDefault();
    var formData = new FormData(this)
    console.log(formData)
    $.ajax({
      type: 'POST',
      url: $(this).attr('action'),
      data: formData,
      processData: false,
      contentType: false,
      success: function(response){
        var labels = [];
        var values = [];
        $.each(response, function(key, value){
          labels.push(key)
          values.push(value)
        })
        drawGraph(labels, values)
        $("#btn_load_seven_range").html(`<i class="fa-solid fa-arrows-rotate"></i>`)
      },
      error: function(xhr, status, error){
        console.error("Error:", error);
      }
    });
  })
  $("#btn_load_seven_range").click();

});
function drawGraph(labels, values){
  'use strict'
  
    //feather.replace({ 'aria-hidden': 'true' })
  
    // Graphs
    var ctx = document.getElementById('myChart')
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          data: values,
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#007bff',
          borderWidth: 4,
          pointBackgroundColor: '#007bff'
        }]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: false
            }
          }]
        },
        legend: {
          display: false
        }
      }
    })
}
  