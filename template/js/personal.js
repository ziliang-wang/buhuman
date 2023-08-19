window.onload = () => {
    const $menu = document.getElementById('menu');
    const $avatarBtn = document.getElementById('avatarBtn');
    const $avatarModal = document.getElementById('avatarModal');
    const $personalModalClose = document.querySelector('.personal-modal-close');

    $menu.onclick = (e) => {
        const self = e.target;
        const tabName = self.getAttribute('data-tab');

        if (tabName) {
            location.href = `?type=${tabName}`;
        }
    };

    $avatarBtn.onclick = () => {
        $avatarModal.style.display = 'block';
    };

    $personalModalClose.onclick = () => {
        $avatarModal.style.display = 'none';
    };
};