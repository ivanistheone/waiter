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