window.onload = () => {
    const $nextBtn = document.getElementById('nextBtn');
    const $email = document.getElementById('email');
    const $vcode = document.getElementById('vcode');
    const $emailMsg = document.getElementById('emailMsg');
    const $vcodeMsg = document.getElementById('vcodeMsg');

    const emailReg = /^\w{2,}\@\w{2,}\.[a-zA-Z]{2,4}(\.[a-zA-Z]{2,4})?$/;
    const vcodeReg = /^[0-9a-zA-Z]{4}$/;

    let emalFlag = false;
    let vcodeFlag = false;

    // $email.focus();

    $email.onblur = () => {
        if (!emailReg.test($email.value.trim())) {
            $emailMsg.innerHTML = 'Email格式錯誤';
            emalFlag = false;
        } else {
            $emailMsg.innerHTML = '';
            emalFlag = true;
        }
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

    $nextBtn.onclick = () => {
        if ($email.value.trim() === '' || $vcode.value.trim() === '') {
            $emailMsg.innerHTML = 'Email不得為空';
            $vcodeMsg.innerHTML = '請輸入正確的驗證碼';
            return;
        }

        if (!emalFlag || !vcodeFlag) {
            return;
        }
        // axios
        alert('ok');
    };
};