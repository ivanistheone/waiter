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
  // using jQuery
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  // setup so CSRF token will be added to all POST requests
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (settings.type==="POST" && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });


});


$(function() {
  $('.stage-progress').tooltip();

  // channel save functionality
  var toggleSave = function(data) {
    $('.save-icon').toggleClass('fa-star');
    $('.save-icon').toggleClass('fa-star-o');
  };
  $('.save-icon').click(function() {
    var save_channel_url = "/api/runs/channels/" + channel_id + "/save_to_profile/";
    if ($(this).hasClass('fa-star')) {
      // Unfollow this channel.
      $.post(save_channel_url, {"save_channel_to_profile": false}, toggleSave);
    } else {
      // Follow this channel.
      $.post(save_channel_url, {"save_channel_to_profile": true}, toggleSave);
      // TODO: check if successful (what if user not logged in? redirect to login page?)
    }
  });

  var myLineChart = new Chart($("#resource-chart")[0].getContext('2d'), createConfig());
});