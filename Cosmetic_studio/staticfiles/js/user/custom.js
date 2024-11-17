(function() {
    'use strict';

    var toggles = document.querySelectorAll('.js-password-show-toggle');

    toggles.forEach(function(toggle) {
        var passwordInput = toggle.parentElement.querySelector('input[type="password"], input[type="text"]');

        toggle.addEventListener('click', function(e) {
            e.preventDefault();

            if (toggle.classList.contains('active')) {
                passwordInput.setAttribute('type', 'password');
                toggle.classList.remove('active');
            } else {
                passwordInput.setAttribute('type', 'text');
                toggle.classList.add('active');
            }
        });
    });
})();

