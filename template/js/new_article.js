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

    $publishBtn = document.getElementById('publishBtn');
    $publishArticleModal = document.getElementById('publishArticleModal');
    $publishClose = document.getElementById('publishClose');

    $publishBtn.onclick = () => {
        $publishArticleModal.style.display = 'block';
    };

    $publishClose.onclick = () => {
        $publishArticleModal.style.display = 'none';
    };

    // $articleItem = document.getElementById('articleItem');
    // $articleItemList = document.getElementById('articleItemList');
    //
    // $articleItem.onclick = (e) => {
    //     e.stopPropagation();
    //     $articleItemList.style.display = 'block'
    // };
};