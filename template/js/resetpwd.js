window.onload = () => {
    $recode = document.getElementById('recode');
    $password1 = document.getElementById('password1');
    $password2 = document.getElementById('password2');
    $confirmBtn = document.getElementById('confirmBtn');

    $recodeMsg = document.getElementById('recodeMsg');
    $pwd1Msg = document.getElementById('pwd1Msg');
    $pwd2Msg = document.getElementById('pwd2Msg');

    const passwdReg = /^\w{6,}/;
    const reCodeReg = /^[0-9a-zA-Z]{6}$/;

    let isReCode = false;
    let isPwd1 = false;

    $recode.onblur = function () {
        const recode = this.value.trim();

        if (!reCodeReg.test(recode)) {
            $recodeMsg.innerHTML = 'Email驗證碼格式錯誤';
            isReCode = false;
        } else {
            $recodeMsg.innerHTML = '';
            isReCode = true;
        }
    };

    $password1.onblur = function ()  {
        const password1 = this.value.trim();

        if (!passwdReg.test(password1)) {
            isPwd1 = false;
            $pwd1Msg.innerHTML = '密碼格式錯誤';
        } else {
            isPwd1 = true;
            $pwd1Msg.innerHTML = '';
        }
    };

    $password2.onblur = function () {
        const password1 = $password1.value.trim();
        const password2 = this.value.trim();

        if (password1 !== password2) {
            $pwd2Msg.innerHTML = '兩次密碼不符';
            isPwd1 = false;
        } else {
            $pwd2Msg.innerHTML = '';
            isPwd1 = true;
        }
    };

    $confirmBtn.onclick = () => {
        const recode = $recode.value.trim();
        const password = $password1.value.trim();

        if (!isReCode || !isPwd1) {
            return;
        }
        axios.post('/reset/password', {
            recode,
            password
        }).then(res => {
            console.log(res);
            if (res.data.status === 9001) {
                $recodeMsg.innerHTML = '請輸入正確的email驗證碼';
            } else if (res.data.status === 9002) {
                $recodeMsg.innerHTML = '參數錯誤';
            } else {
                $recodeMsg.style.color = 'blue';
                $recodeMsg.innerHTML = '密碼修改成功!';
                setTimeout(() => {
                    location.href = '/';
                }, 1000);
            }
        });
    };
};