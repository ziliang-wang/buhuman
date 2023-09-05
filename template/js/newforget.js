window.onload = () => {
    const $nextBtn = document.getElementById('nextBtn');
    const $email = document.getElementById('email');
    const $vcode = document.getElementById('vcode');
    const $imageCode = document.getElementById('imageCode');
    const $emailMsg = document.getElementById('emailMsg');
    const $vcodeMsg = document.getElementById('vcodeMsg');

    const emailReg = /^\w{2,}\@\w{2,}\.[a-zA-Z]{2,4}(\.[a-zA-Z]{2,4})?$/;
    const vcodeReg = /^[0-9a-zA-Z]{4}$/;

    let emalFlag = false;
    let vcodeFlag = false;
    let isExist = false;

    $email.onblur = () => {
        const username = $email.value.trim()
        if (!emailReg.test(username)) {
            $emailMsg.innerHTML = 'Email格式錯誤';
            emalFlag = false;
        } else {
            $emailMsg.innerHTML = '';
            emalFlag = true;
        }
        // axios check user
        axios.post('/reset/chkuser', {
            username: username
        }).then(res => {
            if (res.data.status === 1001) {
                $emailMsg.innerHTML = 'Email格式錯誤';
                isExist = false;
                return false;
            } else if (res.data.status === 8002) {
                $emailMsg.innerHTML = '此Email帳號不存在';
                isExist = false;
                return false;
            }
            $emailMsg.innerHTML = '';
            isExist = true;
        });
    };

    $vcode.onblur = () => {
        if (!vcodeReg.test($vcode.value.trim())) {
            $vcodeMsg.innerHTML = '驗證碼格式錯誤';
            vcodeFlag = false;
        } else {
            $vcodeMsg.innerHTML = '';
            vcodeFlag = true;
        }
    };

    $imageCode.onclick = function (e) {
        this.src = '/vcode?' + Math.random();
    };

    let isNextClick = false;

    $nextBtn.onclick = () => {

        if (isNextClick) return;

        const username = $email.value.trim()
        const vcode = $vcode.value.trim();

        $emailMsg.style.color = '#ef1300';

        if (username === '' && vcode === '') {
            $emailMsg.innerHTML = 'Email不得為空';
            $vcodeMsg.innerHTML = '驗證碼不得為空';
            return;
        }

        if (username === '') {
            $emailMsg.innerHTML = 'Email不得為空';
            return;
        }

        if (vcode === '') {
            $vcodeMsg.innerHTML = '驗證碼不得為空';
            return;
        }

        if (!emalFlag || !vcodeFlag || !isExist) {
            return;
        }
        // axios
        data = {
            username: username,
            vcode: vcode
        };
        // alert('ok');
        axios.post('/reset/next', data).then(res => {
            if (res.data.status === 1002) {
                $vcodeMsg.innerHTML = '請輸入正確的圖片驗證碼';
                return false;
            } else if (res.data.data === 'userErr') {
                $emailMsg.innerHTML = '此Email帳號不存在';
                return false;
            } else {
                $emailMsg.innerHTML = '';
                $vcodeMsg.innerHTML = '';
                $nextBtn.innerHTML = '正在發送Email驗證碼...';
                // ecode
                axios.post('/reset/ecode', {
                    email: username
                }).then(res => {
                    if (res.data.status === 1000) {
                        $emailMsg.style.color = '#3377ff';
                        $emailMsg.style.fontSize = '14px';
                        $emailMsg.innerHTML = '系統已發送驗證碼到您的email, 請查收並修改密碼';
                        $nextBtn.innerHTML = 'Email驗證碼已發送';
                        isNextClick = true;
                    } else {
                        $emailMsg.style.color = '#ef1300';
                        $emailMsg.innerHTML = '發送失敗，請再試一次';
                        isNextClick = false;
                        $nextBtn.innerHTML = '下一步';
                    }
                });
                // location.href = '/reset/password';
            }
        }).catch(err => {
            $emailMsg.innerHTML = '提交失敗，請再試一次';
        });
    };
};