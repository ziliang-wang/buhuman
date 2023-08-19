window.onload = () => {
    const $menu = document.getElementById('menu');
    const $avatarBtn = document.getElementById('avatarBtn');
    const $avatarModal = document.getElementById('avatarModal');
    const $personalModalClose = document.querySelector('.personal-modal-close');
    const $randomAvatar = document.getElementById('randomAvatar');
    const $avatarImg = document.getElementById('avatarImg');
    const $userAvatar = document.getElementById('userAvatar');

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


    // 隨機avatar
    $randomAvatar.onclick = function (){
        const formData = new FormData();
        const uid = this.getAttribute('data-uid');
        // formData.append('article-header-image', articleHeaderImageFile);
        formData.append('uid', uid);
        // axios
        axios.post('/personal/upload/random', formData).then(res => {
            // const $articleImg = document.getElementById('articleImg');
            $avatarImg.src = res.data.url;
            $avatarImg.style.width = '128px';
            $avatarImg.style.height = '128px';
            $userAvatar.src = res.data.url;
            $userAvatar.style.width = '150px';
            $userAvatar.style.height = '150px';
        });
    };
};