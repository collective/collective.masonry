$(document).ready(function() {
  var $portletAboveContainer = $('#portletsAboveContent');
  var $portletBelowContainer = $('#portletsBelowContent');
  $portletAboveContainer.imagesLoaded( function() {
        $portletAboveContainer.masonry({itemSelector:'.portletWrapper'});
  });
  $portletBelowContainer.imagesLoaded( function() {
        $portletBelowContainer.masonry({itemSelector:'.portletWrapper'});
  });
});