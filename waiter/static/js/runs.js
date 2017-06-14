function createConfig() {
  return {
    type: 'line',
    data: {
      labels: ["January", "February", "March", "April", "May", "June", "July"],
      datasets: [{
        label: ".mp4",
        data: [10, 20, 30, 40, 50, 60, 20],
        backgroundColor: Chart.helpers.color("#F1BB7B").alpha(0.5).rgbString(),
        borderColor: "#F1BB7B",
        borderWidth: 1,
        fill: false
      },
      {
        label: ".pdf",
        data: [14, 12, 19, 20, 25, 26, 28],
        backgroundColor: Chart.helpers.color("#FD6467").alpha(0.5).rgbString(),
        borderColor: "#FD6467",
        borderWidth: 1,
        fill: false
      }]
    },
    options: {
      responsive: true,
      legend: {
        position: 'top',
      },
      scales: {
        xAxes: [{
          display: true,
          scaleLabel: {
            display: true,
            labelString: 'Month'
          }
        }],
        yAxes: [{
          display: true,
          scaleLabel: {
            display: true,
            labelString: 'Value'
          }
        }]
      },
      title: {
        display: true,
        text: 'Resource Counts'
      }
    }
  };
}

$(function() {
  $('.stage-progress').tooltip();
  $('.save-icon').click(function() {
    var toggleSave = function(data) {
      $(this).toggleClass('fa-star');
      $(this).toggleClass('fa-star-o');
    };
    if ($(this).hasClass('fa-star')) {
      // Unfollow this channel.
      // TODO(arvnd): I guess this becomes a different method?
      $.post("/api/runs/channels/" + channel_id + "/save_to_profile/", toggleSave);
    } else {
      // Follow this channel.
      $.post("/api/runs/channels/" + channel_id + "/save_to_profile/", toggleSave);
    }
  });
  var myLineChart = new Chart($("#resource-chart")[0].getContext('2d'), createConfig());
});