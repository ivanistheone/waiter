/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');

$(function() {
  var channel_search = new Bloodhound({
    datumTokenizer: function(datum) {
      return datum["name"].split(" ");
    },
    identify: function(datum) {
      return datum["channel_id"];
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: "/api/channels/"
  });

  $('#search-input').typeahead({
    hint: true,
    highlight: true,
    minLength: 1
  },
  {
    name: 'channel_search',
    source: channel_search,
    display: function(data) {
      return data["name"];
    },
  });
  // Bind to channel page url.
  $('.typeahead').on('typeahead:select',
                        function(ev, suggestion) {
      window.location.href = "/channels/" + suggestion["channel_id"] + "/";
  });
});




// setup required to attach CSRF header for jquery POST requests
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
