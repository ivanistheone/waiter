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
  $('.typeahead').on('typeahead:select', 
                        function(ev, suggestion) {
      console.log('Selection: ' + suggestion);
  });
});