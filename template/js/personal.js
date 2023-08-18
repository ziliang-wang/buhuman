window.onload = () => {
    const $menu = document.getElementById('menu');

    $menu.onclick = (e) => {
        const self = e.target;
        const tabName = self.getAttribute('data-tab');

        if (tabName) {
            location.href = `?type=${tabName}`;
        }
    };
};