window.onload = () => {
    const $search = document.getElementById('search');
    const $searchBtn = document.getElementById('searchBtn');

    const $leftMenuList = document.getElementById('leftMenuList');
    const $leftMenuListItems = $leftMenuList.querySelectorAll('li a');

    const $register = document.getElementById('register');
    const $maskRegModal = document.getElementById('maskRegModal');
    const $regForm = document.getElementById('regForm');

    const $login = document.getElementById('login');
    const $maskLoginModal = document.getElementById('maskLoginModal');

    const $regClose = document.getElementById('regClose');

    const $sendCode = document.getElementById('sendCode');

    const $backLogin = document.getElementById('backLogin');

    const $loginForm = document.getElementById('loginForm');

    const $loginClose = document.getElementById('loginClose');

    const $backReg = document.getElementById('backReg');

    const $writeArticle = document.getElementById('writeArticle');

    const $imageCode = document.getElementById('imageCode');

    const $regEmail = document.getElementById('regEmail')

    const $regPassword = document.getElementById('regPassword')

    const $regRePassword = document.getElementById('regRePassword')

    const $regEmailErrMsg = document.getElementById('regEmailErrMsg');

    const $regPwdErrMsg = document.getElementById('regPwdErrMsg');

    const $regCodeErrMsg = document.getElementById('regCodeErrMsg')

    $imageCode.onclick = function (e) {
        this.src = '/vcode?' + Math.random();
    };

    $searchBtn.onclick = () => {
        const keyword = $search.value.trim();
        location.href = `?keyword=${keyword}`;
    };

    $register.onclick = (e) => {
        e.stopPropagation();
        $maskRegModal.style.display = 'block';
        $sendCode.innerText = '獲取驗證碼';
        clearInterval(timer);
        count = 60;
        $sendCode.disabled = false;
        $regEmailErrMsg.innerHTML = '';
        $regPwdErrMsg.innerHTML = ''
    };

    $regForm.onclick = (e) => {
        e.stopPropagation();
    };

    $regClose.onclick = () => {
        $maskRegModal.style.display = 'none';
        clearInterval(timer);
        $sendCode.disabled = false;
        count = 60;
    };

    $login.onclick = (e) => {
        e.stopPropagation();
        $maskLoginModal.style.display = 'block';
        $imageCode.src = '/vcode?' + Math.random();
    };

    $loginForm.onclick = (e) => {
        e.stopPropagation();
    };

    $loginClose.onclick = () => {
        $maskLoginModal.style.display = 'none';
        // clearInterval(timer);
        // $sendCode.disabled = false;
        // count = 60;
    };

    document.onclick = () => {
        $maskRegModal.style.display = 'none';
        $maskLoginModal.style.display = 'none';
    }

    $leftMenuList.onclick = (e) => {
        for (let item of $leftMenuListItems) {
            item.classList.remove('selected');
        }
        e.target.classList.add('selected');
    };

    let timer;
    // let count = 5;

    $sendCode.onclick = function () {
        const targetEmail = $regEmail.value.trim()
        const firstPassword = $regPassword.value.trim()
        const secondPassword = $regRePassword.value.trim()

        $regCodeErrMsg.innerHTML = '';


        if (!targetEmail.match('.+@.+\..+')) {
            // alert('Email格式錯誤');
            $regEmailErrMsg.innerHTML = 'Email格式錯誤';
            $regEmail.focus()
            return false;
        } else {
            $regEmailErrMsg.innerHTML = '';
        }

        if (firstPassword !== secondPassword) {
            $regPwdErrMsg.innerHTML = '兩次數入的密碼不一致'
            $regPassword.focus()
            return false;
        } else {
            $regEmailErrMsg.innerHTML = ''
        }

        axios.post('/ecode', {
            email: targetEmail
        }).then(res => {
            console.log(res.data)
            if (res.data.status !== 1000) {
                $regCodeErrMsg.innerHTML = '獲取驗證碼失敗，請重新獲取';
            } else {
                $regCodeErrMsg.innerHTML = '';
            }
        }).catch(err => {
            console.log(err);
        });


        this.disabled = true;
        let count = 5;
        this.innerText = `重新獲取 (${count})`;
        timer = setInterval(() => {
            count -= 1;
            this.innerText = `重新獲取 (${count})`;
            if (count == 0) {
                this.innerText = `重新獲取`;
                this.disabled = false;
                count = 5;
                clearInterval(timer);
            }
        }, 1000);
    };

    $backLogin.onclick = () => {
        $maskRegModal.style.display = 'none';
        $maskLoginModal.style.display = 'block';
    };

    $backReg.onclick = () => {
        $maskLoginModal.style.display = 'none';
        $maskRegModal.style.display = 'block';
    };

    $writeArticle.onclick = () => {
        location.href = './new_article.html';
    };
};