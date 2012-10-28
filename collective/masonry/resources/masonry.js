$(document).ready(function() {
  var $portletsContainer = $('.portlets-masonry');
  $portletsContainer.imagesLoaded( function() {
	  $portletsContainer.masonry(masonry_configuration);
  });
});