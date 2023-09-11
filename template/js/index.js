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

    // const $writeArticle = document.getElementById('writeArticle');
    const $writeArticle = document.querySelector('.write');

    const $imageCode = document.getElementById('imageCode');

    const $regEmail = document.getElementById('regEmail')

    const $regPassword = document.getElementById('regPassword')

    const $regRePassword = document.getElementById('regRePassword')

    const $regEmailErrMsg = document.getElementById('regEmailErrMsg');

    const $regPwdErrMsg = document.getElementById('regPwdErrMsg');

    const $regCode = document.getElementById('regCode');

    const $regCodeErrMsg = document.getElementById('regCodeErrMsg');
    const $regBtn = document.getElementById('regBtn');
    const $loginBtn = document.getElementById('loginBtn')
    const $loginAccount = document.getElementById('loginAccount');
    const $loginAccountMsg = document.getElementById('loginAccountMsg');
    const $loginPwd = document.getElementById('loginPwd');
    const $loginPwdMsg = document.getElementById('loginPwdMsg');
    const $vcode = document.getElementById('vcode');
    const $vcodeMsg = document.getElementById('vcodeMsg');
    const $keepLogin = document.getElementById('keepLogin');
    const $logout = document.getElementById('logout');

    // const $notificationList = document.getElementById('notificationList');
    // const $resetPwdBtn = document.getElementById('resetPwdBtn');


    // 註冊/登入表單 正則表達式
    const emailReg = /^\w{2,}\@\w{2,}\.[a-zA-Z]{2,4}(\.[a-zA-Z]{2,4})?$/;
    const passwdReg = /^\w{6,}/;
    const regCodeReg = /^[0-9a-zA-Z]{6}$/;
    const vcodeReg = /^[0-9a-zA-Z]{4}$/;
    // flags
    let isRegEmail = false;
    let isRegPwd = false;
    let isRegRePwd = false;
    let isRegCode = false;

    let isLoginAccount = false;
    let isLoginPwd = false;
    let isVcode = false;
    let keepDays = 0;
    let action = '';

    const $top1AvatarList = document.getElementById('top1AvatarList');

    // 通知列表
    // console.log($reminder);
    //
    if (window.isLogin === 'true') {
        const $reminder = document.getElementById('reminder');
        const $notificationLayout = document.getElementById('notificationLayout');

        let reminderSwitch = false;
        let notificationData = [];

        axios.get('/notification').then(res => {
            notificationData = res.data.data;
            console.log(notificationData);
        });

        if ($reminder) {
            $reminder.onclick = function (e) {
                e.stopPropagation();

                if (notificationData.length !== 0) {
                    const $notificationList = document.getElementById('notificationList');
                    $notificationList.onclick = function (e) {
                        const self = e.target;
                        const fans = self.getAttribute('data-fans');
                        const faid = self.getAttribute('data-faid');

                        if (fans === 'fans') {
                            location.href = `/detail?aid=${faid}`;
                        }
                    };

                    function parseDate(date) {
                        // console.log(typeof date);
                        const year = new Date(date).getFullYear();
                        const month = (new Date(date).getMonth() + 1) < 10 ? '0' + (new Date(date).getMonth() + 1) : new Date(date).getMonth() + 1;
                        const d = (new Date(date).getDate()) < 10 ? '0' + (new Date(date).getDate()) : new Date(date).getDate();
                        const h = (new Date(date).getHours()) < 10 ? '0' + (new Date(date).getHours()) : new Date(date).getHours();
                        const m = (new Date(date).getMinutes()) < 10 ? '0' + (new Date(date).getMinutes()) : new Date(date).getMinutes();
                        const s = (new Date(date).getSeconds()) < 10 ? '0' + (new Date(date).getSeconds()) : new Date(date).getSeconds();

                        const result = `${year}-${month}-${d} ${h}:${m}:${s}`
                        console.log(result)
                        return result;
                    }

                    if (!reminderSwitch) {
                        axios.get('/notification').then(res => {
                            if (res.data.status === 9000) {
                                notificationData = res.data.data;
                                console.log(notificationData);
                                $notificationList.innerHTML = '';
                                for (const item of notificationData) {
                                    let html = ``;
                                    if (item.type === 'fans') {
                                        html = `
                                            <li class="list-item flex-r" data-fans="${item.type}" data-faid="${item.aid}">
                                                <a class="item-left"></a>
                                                <div class="item-middle" data-fans="${item.type}" data-faid="${item.aid}">
                                                    <div class="content flex-r" data-fans="${item.type}" data-faid="${item.aid}">
                                                            您關注的&nbsp;<a href="/u?user=${item.uid }" style="color: #6f4627">${item.nickname}</a>&nbsp;發表了文章
                                                    </div>
                                                    <div class="datetime" data-fans="${item.type}" data-faid="${item.aid}">${parseDate(item.create_time)}</div>
                                                </div>
                                                <a href="/detail?aid=${item.aid}">
                                                    <img class="item-right img2" src="${item.article_avatar}" alt="">
                                                </a>
                                            </li>
                                        `;
                                    } else if (item.type === 'concerned') {
                                        html = `
                                            <li class="list-item flex-r"">
                                                <a class="item-left" href="/u?user=${item.uid}"><img class="img1" src="${item.avatar}" alt=""></a>
                                                <a href="/u?user=${item.uid}">
                                                   <div class="item-middle">
                                                     <div class="content flex-r">
                                                        <span>${item.nickname}</span>
                                                        <span>關注</span>了您
                                                     </div>
                                                     <div class="datetime">${parseDate(item.create_time)}</div>
                                                   </div>
                                                </a>
                                                <span class="item-right zhanwei"></span>
                                            </li>
                                        `;
                                    } else {
                                        html = `
                                            <li class="list-item flex-r"">
                                                <a class="item-left" href="/u?user=${item.uid}"><img class="img1" src="${item.avatar}" alt=""></a>
                                                <a href="/detail?aid=${item.aid}">
                                                    <div class="item-middle">
                                                        <div class="content flex-r">
                                                            <span>${item.nickname}</span>
                                                            <span>${item.type}</span>了您的文章
                                                        </div>
                                                        <div class="datetime">${parseDate(item.create_time)}</div>
                                                    </div>
                                                </a>
                                                <a href="/detail?aid=${item.aid}">
                                                    <img class="item-right img2" src="${item.article_avatar}" alt="">
                                                </a>
                                            </li>
                                        `;
                                    }
                                    $notificationList.innerHTML += html;
                                }
                            } else {
                                // error handler
                            }
                        });
                        $notificationLayout.style.opacity = '1';
                        $notificationLayout.style.height = '300px';
                        reminderSwitch = !reminderSwitch;
                    } else {
                        $notificationLayout.style.opacity = '0';
                        $notificationLayout.style.height = '0';
                        reminderSwitch = !reminderSwitch;
                    }
                } else {
                    const $noneNotificationLayout = document.getElementById('noneNotificationLayout');
                    if (!reminderSwitch) {
                        $noneNotificationLayout.style.opacity = '1';
                        reminderSwitch = !reminderSwitch;
                    } else {
                        $noneNotificationLayout.style.opacity = '0';
                        reminderSwitch = !reminderSwitch;
                    }
                    document.onclick = () => {
                        $noneNotificationLayout.style.opacity = '0';
                        reminderSwitch = false;
                    };
                }
            }

            document.onclick = () => {
                $notificationLayout.style.opacity = '0';
                $notificationLayout.style.height = '0';
                reminderSwitch = false;
            };
        }
    }


    // get top1 concerning avatar
    axios.get('/get/top1').then(res => {
        let leftOffset = 0;
        const span = document.createElement('span');
        span.innerHTML = '正在關注';
        span.className = 'viewers';

        if (res.data.status === 9000) {
            let avatarList = res.data.data;
            for (let i = 0; i < avatarList.length; i++) {
                const img = document.createElement('img');
                img.src = avatarList[i];

                if (i === 0) {
                    leftOffset += 0;
                } else {
                    leftOffset += 15;
                }

                img.style.left = leftOffset + 'px';
                $top1AvatarList.appendChild(img);
            }
            span.style.marginLeft = (leftOffset * 3) + 'px';
            $top1AvatarList.appendChild(span);
        }
    });

    // const $top1 = document.getElementById('top1');
    // $top1.onclick = () => {
    //     location.href = ''
    // };


    if (window.isLogin === 'true') {
        const $avatar = document.querySelector('.avatar');
        $avatar.onclick = () => {
            location.href = '/personal';
        };
    }

    // $logout.onclick = (e) => {
    //     $writeArticle.setAttribute('data-isLogin', 'false');
    // };

    $loginAccount.onblur = function () {
        const loginAccount = this.value;
        if (!emailReg.test(loginAccount)) {
            $loginAccountMsg.innerHTML = 'Email格式錯誤';
            // $regEmail.focus()
            isLoginAccount = false;
            return false;
        } else {
            $loginAccountMsg.innerHTML = '';
            isLoginAccount = true;
        }
    };

    $loginPwd.onblur = function () {
        const loginPwd = this.value.trim();
        if (!passwdReg.test(loginPwd)) {
            $loginPwdMsg.innerHTML = '密碼格式錯誤';
            // this.focus();
            isLoginPwd = false;
            return false;
        } else {
            $loginPwdMsg.innerHTML = '';
            isLoginPwd = true;
        }
    };

    $vcode.onblur = function () {
        const vcode = this.value;
        if (!vcodeReg.test(vcode)) {
            $vcodeMsg.innerHTML = '請輸入圖片驗證碼';
            // $regCode.focus();
            isVcode = false;
            return false;
        } else {
            $vcodeMsg.innerHTML = '';
            isVcode = true;
        }
    };

    $keepLogin.onclick = function () {
        keepDays = this.checked ? 7 : 0;
        console.log(keepDays);
    };


    $loginBtn.onclick = () => {
        const loginAccount = $loginAccount.value;
        if (!emailReg.test(loginAccount)) {
            $loginAccountMsg.innerHTML = 'Email格式錯誤';
            // $regEmail.focus()
            isLoginAccount = false;
            return false;
        } else {
            $loginAccountMsg.innerHTML = '';
            isLoginAccount = true;
        }

        const loginPwd = $loginPwd.value.trim();
        if (!passwdReg.test(loginPwd)) {
            $loginPwdMsg.innerHTML = '密碼格式錯誤';
            // this.focus();
            isLoginPwd = false;
            return false;
        } else {
            $loginPwdMsg.innerHTML = '';
            isLoginPwd = true;
        }

        const vcode = $vcode.value;
        if (!vcodeReg.test(vcode)) {
            $vcodeMsg.innerHTML = '請輸入圖片驗證碼';
            // $regCode.focus();
            isVcode = false;
            return false;
        } else {
            $vcodeMsg.innerHTML = '';
            isVcode = true;
        }

        if (!isLoginAccount || !isLoginPwd || !isVcode) {
            return false;
        }

        data = {
            username: loginAccount,
            password: loginPwd,
            vcode: vcode,
            keepdays: keepDays,
            action: action
        }
        $loginBtn.innerHTML = '登錄中.....';
        // axios
        axios.post('/login', data).then(res => {
            // console.log(res.data.data);
            if (res.data.action === 'write') {
                setTimeout(() => {
                    location.reload();
                }, 500);
                location.href = '/article/new';
            } else if (res.data.data === 'loginok') {
                setTimeout(() => {
                    location.reload();
                }, 500);
            } else if (res.data.data === 'vcodeErr') {
                $vcodeMsg.innerHTML = '請輸入正確的圖片驗證碼';
                $loginBtn.innerHTML = '登錄';
                return;
            } else {
                $loginAccountMsg.innerHTML = '帳號或密碼錯誤';
                $loginBtn.innerHTML = '登錄';
                return;
            }
            action = '';
            // $writeArticle.setAttribute('data-isLogin', 'true');
            $loginClose.click();
        });
    };

    $imageCode.onclick = function (e) {
        this.src = '/vcode?' + Math.random();
    };

    $search.onkeyup = (e) => {
        if (e.keyCode === 13) {
            e.preventDefault();
            $searchBtn.click();
        }
    };

    $searchBtn.onclick = () => {
        const keyword = $search.value.trim();
        if (keyword === '') return false;
        // location.href = `?keyword=${keyword}`;
        location.href = `/?keyword=${keyword}`;
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
        $loginAccount.focus();
        $loginAccountMsg.innerHTML = '';
        $loginPwdMsg.innerHTML = '';
        $vcodeMsg.innerHTML = '';
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

    $regEmail.onblur = function () {
        const regEmail = this.value;
        if (!emailReg.test(regEmail)) {
            $regEmailErrMsg.innerHTML = 'Email格式錯誤';
            // $regEmail.focus()
            isRegEmail = false;
            return false;
        } else {
            $regEmailErrMsg.innerHTML = '';
            isRegEmail = true;
            axios.post('/chkuser', {
                username: regEmail.toLowerCase()
            }).then(res => {
                if (res.data.data === 'exist') {
                    $regEmailErrMsg.innerHTML = '此帳號已存在';
                    isRegEmail = false;
                } else {
                    isRegEmail = true;
                }
            })
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
        const regRePassword = $regRePassword.value.trim();
        const regCode = $regCode.value;

        if (!isRegEmail) {
            return false;
        }

        if (!passwdReg.test(regPassword)) {
            $regPwdErrMsg.innerHTML = '密碼必須為至少6位的英文字母和數字';
            // $regPassword.focus()
            isRegPwd = false;
            return false;
        } else {
            $regPwdErrMsg.innerHTML = '';
            isRegPwd = true;
        }

        if (regPassword !== regRePassword) {
            $regPwdErrMsg.innerHTML = '兩次數入的密碼不一致';
            // $regPassword.focus()
            isRegRePwd = false;
            return false;
        } else {
            $regEmailErrMsg.innerHTML = '';
            isRegRePwd = true;
        }

        if (!regCodeReg.test(regCode)) {
            $regCodeErrMsg.innerHTML = '請輸入正確的Email驗證碼';
            // $regCode.focus();
            isRegCode = false;
            return false;
        } else {
            $regCodeErrMsg.innerHTML = '';
            isRegCode = true;
        }

        if (!isRegEmail || !isRegPwd || !isRegRePwd || !isRegCode) {
            return false;
        }

        $regBtn.innerHTML = '帳號註冊中.....';
        // console.log(regEmail);
        // console.log(regPassword);
        // console.log(regCode);
        // axios
        axios.post('/reg', {
            username: regEmail.toLowerCase(),
            password: regPassword,
            ecode: regCode.toLowerCase()
        }).then(res => {
            console.log(res.data);

            if (res.data.data === 'exist') {
                $regCodeErrMsg.style.color = '#ef1300';
                $regEmailErrMsg.innerHTML = '此帳號已存在';
            } else {
                $regEmailErrMsg.innerHTML = '';
            }

            if (res.data.data === 'ecodefail') {
                $regCodeErrMsg.style.color = '#ef1300';
                $regCodeErrMsg.innerHTML = '驗證碼錯誤，請重新獲取';
            }


            if (res.data.data === 'added') {
                $regCodeErrMsg.style.color = 'blue';
                $regCodeErrMsg.innerHTML = '帳號註冊成功';
            }

            if (res.data.data === 'fail') {
                $regCodeErrMsg.style.color = '#ef1300';
                $regCodeErrMsg.innerHTML = '帳號註冊失敗';
            }

            $regBtn.innerHTML = '立即註冊';
        })
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
            email: regEmail.toLowerCase()
        }).then(res => {
            if (res.data.status !== 1000) {
                $regCodeErrMsg.style.color = '#ef1300';
                $regCodeErrMsg.innerHTML = '獲取驗證碼失敗，請重新獲取';
                this.innerText = `重新獲取`;
                this.disabled = false;
                count = 5;
                clearInterval(timer);

            } else if (res.data.data === 'sentcode') {
                $regCodeErrMsg.style.color = 'blue';
                $regCodeErrMsg.innerHTML = '驗證碼發送成功，請至您的Email收取驗證碼';
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
        $loginAccountMsg.innerHTML = '';
        $loginPwdMsg.innerHTML = '';
        $vcodeMsg.innerHTML = '';
        $imageCode.src = '/vcode?' + Math.random();
        $loginAccount.focus();
    };

    $backReg.onclick = (e) => {
        // $loginPwdMsg.innerHTML = '';
        // e.stopPropagation();
        // $loginAccountMsg.innerHTML = '';
        // $loginAccount.onblur = null;
        $maskLoginModal.style.display = 'none';
        $maskRegModal.style.display = 'block';
        $regEmailErrMsg.innerHTML = '';
        $regPwdErrMsg.innerHTML = '';
        $regCodeErrMsg.innerHTML = '';
        $regEmail.focus();
    };

    // let writeIsLogin = null;

    // console.log($writeArticle);

    $writeArticle.onclick = function (e) {
        e.stopPropagation();
        // $loginClose.click();
        // if (action !== 'write') return;
        const writeIsLogin = this.getAttribute('data-isLogin');
        action = this.getAttribute('data-action');

        console.log(writeIsLogin);

        if (writeIsLogin !== 'true' || writeIsLogin === 'None') {
            $maskLoginModal.style.display = 'block';
            $loginAccount.focus();
            $loginAccountMsg.innerHTML = '';
            $loginPwdMsg.innerHTML = '';
            $vcodeMsg.innerHTML = '';
            $imageCode.src = '/vcode?' + Math.random();
        } else {
            location.href = '/article/new';
        }
    };

    const $articleList = document.getElementById('articleList');

    // 登入前
    $articleList.onclick = (e) => {
        e.stopPropagation();
        const isLogin = e.currentTarget.getAttribute('data-isLogin');
        const aid = e.target.getAttribute('data-aid');
        if (aid) {
            if (isLogin !== 'true') {
                console.log(isLogin, aid);
                $maskLoginModal.style.display = 'block';
                $loginAccount.focus();
                $loginAccountMsg.innerHTML = '';
                $loginPwdMsg.innerHTML = '';
                $vcodeMsg.innerHTML = '';
                $imageCode.src = '/vcode?' + Math.random();
            }
        }
    };

    const $collection = document.getElementsByClassName('collection');

    for (item of $collection) {
        if (item.getAttribute('data-collected') === '0') {
            item.style.width = '5%';
        } else {
            item.style.width = '10%';
        }
    }

    // 首頁動態關注modal
    const $concertModal = document.getElementById('concertModal');
    // const $nicknamePosition = document.querySelector('.nickname-position');

    $articleList.onmouseover = (e) => {
        const self = e.target;
        const mid = self.getAttribute('data-mid');

        if (mid) {
            const $nicknamePosition = document.getElementById(`nicknamePosition${mid}`);
            console.log(mid);
            const modalTop = $nicknamePosition.offsetTop;
            const modalLeft = $nicknamePosition.offsetLeft;
            console.log(modalTop, modalLeft);
            $nicknamePosition.style.cursor = 'pointer';
            $concertModal.style.top = (modalTop - 165) + 'px';
            $concertModal.style.left = modalLeft + 'px';
            $concertModal.style.display = 'block';
            $concertModal.innerHTML = mid;
        }
    };
};