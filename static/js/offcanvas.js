document.addEventListener('DOMContentLoaded', function () {
    const openBtn = document.getElementById('ofc-open-btn');
    const closeBtn = document.getElementById('ofc-close-btn');
    const offcanvasMenu = document.getElementById('kn-offcanvas');
    const body = document.body;

    openBtn.addEventListener('click', function () {
        body.style.overflow = 'hidden';
        #kn-offcanvas.style.overflow = 'scroll';
    });

    closeBtn.addEventListener('click', function () {
        body.style.overflow = 'auto';
    });
});
