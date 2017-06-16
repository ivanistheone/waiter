function format_date(run) {
  return moment(run["created_at"]).format("MMM D");
}

function get_dataset(resource, idx, data) {
  // Bottle Rocket and Castello Cavalcanti.
  var colors = ["#D8B70A", "#02401B", "#A2A475", "#81A88D", "#972D15", "#FAD510", "#CB2314", "#273046", "#354823", "#1E1E1E"];
  return {
    label: resource,
    data: data.map(function(x) {
      return x.resource_counts[resource] || 0;
    }),
    backgroundColor: Chart.helpers.color(colors[idx]).alpha(0.5).rgbString(),
    borderColor: colors[idx],
    borderWidth: 1,
    fill: false
  }
}

function create_config(data) {
  return {
    type: 'line',
    data: {
      labels: data.map(format_date),
      datasets: Object.keys(data[0].resource_counts).map(
        function(x, i) {
          return get_dataset(x, i, data);
        }),
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
            labelString: 'Date'
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

  // channel save functionality
  var toggleSave = function(data) {
    $('.save-icon').toggleClass('fa-star');
    $('.save-icon').toggleClass('fa-star-o');
  };
  $('.save-icon').click(function() {
    var save_channel_url = "/api/channels/" + channel_id + "/save_to_profile/";
    if ($(this).hasClass('fa-star')) {
      // Unfollow this channel.
      $.post(save_channel_url, {"save_channel_to_profile": false}, toggleSave);
    } else {
      // Follow this channel.
      $.post(save_channel_url, {"save_channel_to_profile": true}, toggleSave);
      // TODO: check if successful (what if user not logged in? redirect to login page?)
    }
  });
  // Get chart data.
  $.getJSON("/api/channels/" + channel_id + "/runs/", function(data) {
    var myLineChart = new Chart(
      $("#resource-chart")[0].getContext('2d'), 
      create_config(
        data.filter(function(x) {
          return x.resource_counts !== undefined && x.resource_counts !== null;
        }).slice(0, 10)));
  });
  // Collapse content tree.
  $('.content-tree > li a').click(function() {
    $(this).parent().find('ul').toggle();
  });
});
