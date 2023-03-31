$(document).ready(function() {
    // Sélectionnez le lien parent
    var dropdownToggle = $('.sidebar-nav li a.has-dropdown');
    
    // Lorsque vous cliquez sur un lien de parent, ouvrez ou fermez le menu
    dropdownToggle.on('click', function(e) {
      e.preventDefault();
      var thisLink = $(this);
      var thisParent = thisLink.parent();
      
      if (thisParent.hasClass('open')) {
        thisParent.removeClass('open');
      } else {
        $('.sidebar-nav li').removeClass('open');
        thisParent.addClass('open');
      }
    });
    
    // Fermer le menu si l'utilisateur clique en dehors de celui-ci
    $(document).on('click', function(e) {
      if (!$(e.target).closest('.sidebar-nav li').length) {
        $('.sidebar-nav li').removeClass('open');
      }
    });
  });