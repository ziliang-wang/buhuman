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

    $imageCode.onclick = function(e) {
        this.src = '/vcode?' + Math.random();
    };

    $searchBtn.onclick = () => {
        const keyword = $search.value.trim();
        location.href = `?keyword=${keyword}`;
    };

    $register.onclick = (e) => {
        e.stopPropagation();
        $maskRegModal.style.display = 'block';
        $sendCode.innerText = '發送';
        clearInterval(timer);
        count = 60;
        $sendCode.disabled = false;
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
    let count = 60;

    $sendCode.onclick = function () {
        this.disabled = true;
        // count = 59;
        this.innerText = `重新發送 (${count})`;
        timer = setInterval(() => {
            count -= 1;
            this.innerText = `重新發送 (${count})`;
            if (count == 0) {
                this.innerText = `重新發送`;
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