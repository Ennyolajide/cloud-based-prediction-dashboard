
$(document).ready(function () {
    // Get the current path
    const currentPath = window.location.pathname;
    // Find the navigation link with matching href and add 'active' class
    $('.navbar-nav .nav-link[href="' + currentPath + '"]').addClass('active');
});
