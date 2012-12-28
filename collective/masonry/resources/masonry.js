$(document).ready(function() {
  if (typeof(masonry_configuration) != "undefined"){
    var $portletsContainer = $('.portlets-masonry');
    $portletsContainer.imagesLoaded( function() {
      $portletsContainer.masonry(masonry_configuration);
    });
  }
});