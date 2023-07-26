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

    const $regCode = document.getElementById('regCode');

    const $regCodeErrMsg = document.getElementById('regCodeErrMsg');
    const $regBtn = document.getElementById('regBtn');
    // 註冊/登入表單 正則表達式
    const emailReg = /^\w{2,}\@\w{2,}\.[a-z]{2,4}(\.[a-z]{2,4})?$/;
    const passwdReg = /^\w{6,}/;
    const regCodeReg = /^[0-9a-zA-Z]{6}$/;
    // flags
    let isRegEmail = false;
    let isRegPwd = false;
    let isRegRePwd = false;
    let isRegCode = false;

    $imageCode.onclick = function (e) {
        this.src = '/vcode?' + Math.random();
    };

    $searchBtn.onclick = () => {
        const keyword = $search.value.trim();
        if (keyword === '') return false;
        location.href = `?keyword=${keyword}`;
    };

    $register.onclick = (e) => {
        e.stopPropagation();
        $maskRegModal.style.display = 'block';
        // isRegEmail = false;
        // isRegPwd = false;
        // isRegRePwd = false;
        // isRegCode = false;
        $regEmail.focus();
        $sendCode.innerText = '獲取驗證碼';
        clearInterval(timer);
        // count = 60;
        $sendCode.disabled = false;
        $regEmailErrMsg.innerHTML = '';
        $regPwdErrMsg.innerHTML = '';
        $regCodeErrMsg.innerHTML = '';
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

    $regEmail.onblur = function (){
        const regEmail = this.value;
        if (!emailReg.test(regEmail)) {
            $regEmailErrMsg.innerHTML = 'Email格式錯誤';
            // $regEmail.focus()
            isRegEmail = false;
            return false;
        } else {
            $regEmailErrMsg.innerHTML = '';
            isRegEmail = true;
        }
    };

    $regPassword.onblur = function () {
        const firstPassword = this.value.trim();
        if (!passwdReg.test(firstPassword)) {
            $regPwdErrMsg.innerHTML = '密碼必須為至少6位的英文字母和數字';
            // $regPassword.focus()
            isRegPwd = false;
            return false;
        } else {
            $regPwdErrMsg.innerHTML = '';
            isRegPwd = true;
        }
    };

    $regRePassword.onblur = function () {
        const firstPassword = $regPassword.value.trim();
        const secondPassword = this.value.trim();
        if (firstPassword !== secondPassword) {
            $regPwdErrMsg.innerHTML = '兩次數入的密碼不一致';
            // $regPassword.focus()
            isRegRePwd = false;
            return false;
        } else {
            $regEmailErrMsg.innerHTML = '';
            isRegRePwd = true;
        }
    };

    $regCode.onblur = function () {
        const regCode = this.value;
        if (!regCodeReg.test(regCode)) {
            $regCodeErrMsg.innerHTML = '請輸入正確的Email驗證碼';
            // $regCode.focus();
            isRegCode = false;
            return false;
        } else {
            $regCodeErrMsg.innerHTML = '';
            isRegCode = true;
        }
    };
    // do 註冊
    $regBtn.onclick = () => {
        const regEmail = $regEmail.value;
        const regPassword = $regPassword.value.trim();
        const regCode = $regCode.value;

        if (!isRegEmail || !isRegPwd || !isRegRePwd || !isRegCode) {
            // alert('資料缺失');
            return false;
        }
        // axios
    };

    $sendCode.onclick = function () {
        const regEmail = $regEmail.value.trim();
        const firstPassword = $regPassword.value;
        const secondPassword = $regRePassword.value.trim();
        // const regCode = $regCode.value.trim()

        $regCodeErrMsg.innerHTML = '';


        if (!emailReg.test(regEmail)) {
            $regEmailErrMsg.innerHTML = 'Email格式錯誤';
            $regEmail.focus();
            isRegEmail = false;
            return false;
        } else {
            $regEmailErrMsg.innerHTML = '';
            isRegEmail = true;
        }

        if (!passwdReg.test(firstPassword)) {
            $regPwdErrMsg.innerHTML = '密碼必須為至少6位的英文字母和數字';
            $regPassword.focus();
            isRegPwd = false;
            return false;
        } else {
            $regPwdErrMsg.innerHTML = '';
            isRegPwd = true;
        }

        if (firstPassword !== secondPassword) {
            $regPwdErrMsg.innerHTML = '兩次數入的密碼不一致'
            $regPassword.focus();
            isRegRePwd = false;
            return false;
        } else {
            $regEmailErrMsg.innerHTML = '';
            isRegRePwd = true;
        }

        axios.post('/ecode', {
            email: regEmail
        }).then(res => {
            if (res.data.status !== 1000) {
                $regCodeErrMsg.innerHTML = '獲取驗證碼失敗，請重新獲取';
                this.innerText = `重新獲取`;
                this.disabled = false;
                count = 5;
                clearInterval(timer);
            } else {
                $regCodeErrMsg.innerHTML = '';
                // console.log(res.data);
            }
        })


        this.disabled = true;
        let count = 5;
        this.innerText = `重新獲取 (${count})`;
        timer = setInterval(() => {
            count -= 1;
            this.innerText = `重新獲取 (${count})`;
            if (count === 0) {
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
        $regEmailErrMsg.innerHTML = '';
        $regPwdErrMsg.innerHTML = '';
        $regCodeErrMsg.innerHTML = '';
    };

    $writeArticle.onclick = () => {
        location.href = './new_article.html';
    };
};