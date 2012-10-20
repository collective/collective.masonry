$(document).ready(function() {
  var $portletAboveContainer = $('#portlets-above');
  var $portletBelowContainer = $('#portlets-below');
  $portletAboveContainer.imagesLoaded( function() {
        $portletAboveContainer.masonry(masonry_configuration);
  });
  $portletBelowContainer.imagesLoaded( function() {
        $portletBelowContainer.masonry(masonry_configuration);
  });
});