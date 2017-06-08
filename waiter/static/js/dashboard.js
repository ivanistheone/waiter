// TODO: expose this in every view as part of header.
$(function() {
  var channel_search = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    // `states` is an array of state names defined in "The Basics"
    local: channels
  });

  $('#search-input').typeahead({
    hint: true,
    highlight: true,
    minLength: 1
  },
  {
    name: 'channel_search',
    source: channel_search
  });
  // Bind to channel page url.
  $('.typeahead').on('typeahead:select', 
                        function(ev, suggestion) {
      console.log('Selection: ' + suggestion);
  });
  var clipboard = new Clipboard('.channel-id-btn');
  $('.channel-id-btn').tooltip();
  $(document).on('shown.bs.tooltip', function (e) {
    setTimeout(function () {
      $(e.target).tooltip('hide');
    }, 500);
});
});