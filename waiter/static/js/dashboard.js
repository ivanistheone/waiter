// TODO: expose this in every view as part of header.
$(function() {
  var clipboard = new Clipboard('.channel-id-btn');
  $('.channel-id-btn').tooltip();
  $(document).on('shown.bs.tooltip', function (e) {
    setTimeout(function () {
      $(e.target).tooltip('hide');
    }, 500);
  });
});


$(function() {
  var start_channel_handler = function (channel_id) {
      console.log('calling channel control/ endpoint');

      var toggleRestartButton = function () {
          button_el = $('*[data-target="#restart-'+channel_id+'-modal"]');
          // TODO: change icon to indicate it's running...
      }

      // POST
      var channel_control_url = "/api/channels/" + channel_id + "/control/";
      // post_data = {"command":"start", "options": JSON.stringify({"--publish": false}) }
      post_data = {"command":"start", "options": JSON.stringify({}) }
      $.post(channel_control_url, post_data, toggleRestartButton);

      // close modal
      $('#restart-'+channel_id+'-modal').modal('hide');
  }

  // HACK: attach to window so it's globally accessible
  window.start_channel_handler = start_channel_handler;
});
