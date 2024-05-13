
    var navbarCollapse = document.getElementById('navbarNav');
    var navbarToggle = document.querySelector('.navbar-toggler');

    navbarToggle.addEventListener('click', function() {
        if (navbarCollapse.classList.contains('show')) {
            navbarCollapse.classList.remove('show');
        } else {
            navbarCollapse.classList.add('show');
        }
    });

