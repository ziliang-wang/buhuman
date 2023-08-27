window.onload = () => {

    const $menu = document.getElementById('menu');

    $menu.onclick = (e) => {
        const self = e.target;
        const tabName = self.getAttribute('data-tab');
        const uid = self.getAttribute('data-uid');

        if (tabName) {
            location.href = `/u?user=${uid}&type=${tabName}`;
        }
    };
};