window.onload = () => {
    const $menu = document.getElementById('menu');
    const $avatarBtn = document.getElementById('avatarBtn');
    const $avatarModal = document.getElementById('avatarModal');
    const $personalModalClose = document.querySelector('.personal-modal-close');
    const $randomAvatar = document.getElementById('randomAvatar');
    const $avatarImg = document.getElementById('avatarImg');
    const $userAvatar = document.getElementById('userAvatar');
    const $xFile = document.getElementById('xFile');
    const $confirm = document.querySelector('.confirm');
    const $tip = document.querySelector('.tip');
    // const $gender = document.querySelector('#gender');

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
    // upload avatar
    $xFile.onchange = (e) => {
        const userImageFile = e.target.files[0];
        const uid = e.target.getAttribute('data-uid');
        const formData = new FormData();
        formData.append('user-header-image', userImageFile);
        formData.append('uid', uid);
        // axios
        axios.post('/personal/upload/cover', formData).then(res => {
            $avatarImg.src = res.data.url;
            $avatarImg.style.width = '128px';
            $avatarImg.style.height = '128px';
            $userAvatar.src = res.data.url;
            $userAvatar.style.width = '150px';
            $userAvatar.style.height = '150px';
        });
    };

    // 隨機avatar
    $randomAvatar.onclick = function () {
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

    $confirm.onclick = () => {
        location.reload();
    };

    let isTipShow = true;

    setInterval(() => {
        if (isTipShow) {
            $tip.style.display = 'none';
        } else {
            $tip.style.display = 'block';
        }
        isTipShow = !isTipShow;
    }, 1000);


    // gender
    const $gender1 = document.getElementById('gender1');
    const $gender2 = document.getElementById('gender2');
    const $genderBtn = document.getElementById('genderBtn');
    const $headerGender = document.getElementById('headerGender');

    let genderValue = '';

    $gender1.onclick = function () {
        if (this.checked) {
            genderValue = this.value;
            // console.log(genderValue);
        }
    };

    $gender2.onclick = function (){
        if (this.checked) {
            genderValue = this.value;
            // console.log(genderValue);
        }
    };

    $genderBtn.onclick = () => {
        if (genderValue === '') return false;
        axios.post('/alter/gender', {
            gender: genderValue.trim()
        }).then(res => {
            if (res.data.status === 8000) {
                if (res.data.data === 'female') {
                    $headerGender.innerHTML = '女';
                }

                if (res.data.data === 'male') {
                    $headerGender.innerHTML = '男';
                }
            }
        });
    };

    // slogan
    let sloganValue = '';
    const $slogan = document.getElementById('slogan');
    const $sloganBtn = document.getElementById('sloganBtn');
    const $headerSlogan = document.getElementById('headerSlogan');

    $sloganBtn.onclick = () => {
        sloganValue = $slogan.value.trim();
        // console.log(sloganValue);
        axios.post('/alter/slogan', {
            slogan: sloganValue
        }).then(res => {
            // console.log(res.data);
            if (res.data.status === 8000) {
                $headerSlogan.innerHTML = res.data.data;
            }
        });
    };

    // password
    const $password1 = document.getElementById('password1');
    const $password2 = document.getElementById('password2');
    const $pwdMsg = document.getElementById('pwdMsg');
    const $passwordBtn = document.getElementById('passwordBtn');

    let isPassword1 = false;
    let isPassword2 = false;

    let password = '';

    $password1.onblur = function() {
        isPassword1 = !(this.value.trim() === '' || this.value.trim().length < 6);
        if (!isPassword1) {
            $pwdMsg.innerHTML = '密碼不得為空，且必須為6位以上喔';
        } else {
            $pwdMsg.innerHTML = '';
        }
    };

    $password2.onblur = function() {
        isPassword2 = !(this.value.trim() === '' || this.value.trim().length < 6);
        if (!isPassword2) {
            $pwdMsg.innerHTML = '密碼不得為空，且必須為6位以上喔';
        } else {
            $pwdMsg.innerHTML = '';
        }
    };

    $passwordBtn.onclick = () => {
        if (!isPassword1 || !isPassword2) return;
        if ($password1.value.trim() !== $password2.value.trim()) {
            $pwdMsg.innerHTML = '兩次密碼不符';
            return;
        } else {
            $pwdMsg.innerHTML = '';
            password = $password1.value.trim();
        }
        // axios
        console.log('password ok', password);
    };
};