window.onload = () => {
    const ue = UE.getEditor('editor', {
        // ... 更多配置
        shortcutMenu: false,
        elementPathEnabled: false,
        wordCount: false,
        autoHeightEnabled: false,
        // 初始化编辑器宽度,默认 1000
        // initialFrameWidth: 800,
        initialFrameWidth: '100%',
        // 初始化编辑器高度,默认 320
        initialFrameHeight: 500,
        serverUrl: 'http://127.0.0.1:5000/ue',
        toolbars: [
            [
                // "source",
                "insertcode",
                "bold",
                "italic",
                "insertimage",
                "link",
                "insertorderedlist",
                "insertunorderedlist",
                "blockquote",
                "undo",
                "redo",
                "emotion"
            ]
        ]
    });

    const $publishBtn = document.getElementById('publishBtn');
    const $publishArticleModal = document.getElementById('publishArticleModal');
    // const $publishClose = document.getElementById('publishClose');

    // $publishBtn.onclick = () => {
    //     $publishArticleModal.style.display = 'block';
    // };

    // $publishClose.onclick = () => {
    //     $publishArticleModal.style.display = 'none';
    // };

    // const $publishBtn = document.getElementById('publishBtn');

    let content = '';
    let title = '';
    let aid = -1;
    let drafted = 0;

    $publishBtn.onclick = () => {
        // console.log(ue.getContent());
        title = $articleTitle.value.trim();
        content = ue.getContent();
        axios.post('/article/save', {
            title: title,
            content: content,
            aid: aid,
            drafted: drafted
        }).then(res => {
            if (res.data.status === 2003) {
                aid = res.data.aid;
                alert(res.data.data);
            } else {
                alert('草稿存檔失敗');
            }
        });
        $publishArticleModal.style.display = 'block';
    };

    // $articleItem = document.getElementById('articleItem');
    // $articleItemList = document.getElementById('articleItemList');
    //
    // $articleItem.onclick = (e) => {
    //     e.stopPropagation();
    //     $articleItemList.style.display = 'block'
    // };
};