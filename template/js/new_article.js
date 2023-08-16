window.onload = () => {

    document.onclick = () => {
        $draftedContainer.style.display = 'none';
        $upArrow.style.display = 'none';
        isShowDraftBox = false;
    };

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

    const $editor = document.getElementById('editor');

    const $publishBtn = document.getElementById('publishBtn');
    const $publishArticleModal = document.getElementById('publishArticleModal');
    const $draftNum = document.querySelector('.draft-num');

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
    // let label_name = '';
    let tagsResultList = [];

    const autoSave = (drafted) => {
        tagsResultList = [];
        // e.stopPropagation();
        drafted = 0;
        aid = -1;
        //
        // const tagsList = document.getElementById('tagItems').getElementsByTagName('span');
        // if (tagsList.length >= 1) {
        //     for (let item of tagsList) {
        //         tagsResultList.push(item.getAttribute('data-tag'));
        //     }
        // }
        // console.log(ue.getContent());
        title = $articleTitle.value.trim();
        // if (title.length < 6 || title === '') {
        //     alert('標題不能為空，且必需為6個字以上喔');
        //     return;
        // }
        content = ue.getContent().trim();

        // console.log(content);

        // if (content.length < 32 || content === '') {
        //     alert('內容創作，不能為空，且必需為20個字以上喔');
        //     return;
        // }

        axios.post('/article/save', {
            title: title,
            content: content,
            aid: aid,
            drafted: drafted,
            //
            // article_label: window.article_label_name,
            // article_type: window.article_type_name,
            // article_tag: tagsResultList.join(',')
        }).then(res => {
            if (res.data.status === 2003) {
                aid = res.data.aid;
                // alert(res.data.data);
            } else {
                alert('草稿存檔失敗');
                return false;
            }
        });
        // $publishArticleModal.style.display = 'block';
    };

    $draftDesc = document.querySelector('.draft-desc');

    const $draftedBoxItemList = document.getElementById('draftedBoxItemList');
    const $articleTitle = document.getElementById('articleTitle');


    $articleTitle.oninput = () => {
        $draftDesc.innerHTML = '尚未存檔';
    };

    ue.addListener('selectionchange', function () {
        $draftDesc.innerHTML = '尚未存檔';
    });

    // ue.addListener('input', function () {
    //     console.log("选区已经变化！");
    // });

    // const $view = document.getElementById('edui1_iframeholder').getElementById('ueditor_0');
    // console.log($view);
    // $editor.oninput = () => {
    //     console.log('editor');
    // }


    $publishBtn.onclick = (e) => {
        tagsResultList = [];
        e.stopPropagation();
        drafted = 0;
        //
        const tagsList = document.getElementById('tagItems').getElementsByTagName('span');
        if (tagsList.length >= 1) {
            for (let item of tagsList) {
                tagsResultList.push(item.getAttribute('data-tag'));
            }
        }
        // console.log(ue.getContent());
        title = $articleTitle.value.trim();
        if (title.length < 6 || title === '') {
            alert('標題不能為空，且必需為6個字以上喔');
            return;
        }
        content = ue.getContent().trim();

        // console.log(content);

        if (content.length < 32 || content === '') {
            alert('內容創作，不能為空，且必需為20個字以上喔');
            return;
        }

        axios.post('/article/save', {
            title: title,
            content: content,
            aid: aid,
            drafted: drafted,
            //
            article_label: window.article_label_name,
            article_type: window.article_type_name,
            article_tag: tagsResultList.join(',')
        }).then(res => {
            if (res.data.status === 2003) {
                aid = res.data.aid;
                const draftedList = res.data.list;
                // console.log(draftedList);
                $draftedBoxItemList.innerHTML = '';
                // //
                for (const drafted of draftedList) {
                    // const html = `<h1 style="color: red;">${drafted.aid}</h1>`
                    const html = `
                        <div class="list-item flex-r" id="${drafted.aid}">
                            <div class="draft-item-left">
                                <div class="iconfont icon-caogao05 draft-icon" data-did="${drafted.aid}"></div>
                            </div>
                            <div class="draft-item-middle flex-c" data-did="${drafted.aid}">
                                <span class="draft-item-up" data-did="${drafted.aid}">${drafted.title}</span>
                                <span class="draft-item-down" data-did="${drafted.aid}">${drafted.create_time}</span>
                            </div>
                            <div class="draft-item-right">
                                <i class="iconfont icon-guanbi item-close" data-action="remove" data-did="${drafted.aid}"></i>
                            </div>
                        </div>
                    `;
                    $draftedBoxItemList.innerHTML += html;
                }
                $draftNum.innerHTML = res.data.data;
                $draftDesc.innerHTML = '已存檔';
                // console.log()
                // alert(res.data.data);
            } else {
                console.log(res.data.status);
                alert('草稿存檔失敗');
                return false;
            }
        });
        $publishArticleModal.style.display = 'block';
    };

    $xFile = document.getElementById('xFile');
    $xFile.onchange = (e) => {
        const articleHeaderImageFile = e.target.files[0];
        const formData = new FormData();
        formData.append('article-header-image', articleHeaderImageFile);
        formData.append('aid', aid);
        // axios
        axios.post('/article/upload/cover', formData).then(res => {
            const $articleImg = document.getElementById('articleImg');
            $articleImg.src = res.data.url;
            $articleImg.style.width = '128px';
            $articleImg.style.height = '128px';
        });
    };

    const $randomArticleHeader = document.getElementById('randomArticleHeader');

    $randomArticleHeader.onclick = () => {
        const formData = new FormData();
        // formData.append('article-header-image', articleHeaderImageFile);
        formData.append('aid', aid);
        // axios
        axios.post('/article/upload/random', formData).then(res => {
            const $articleImg = document.getElementById('articleImg');
            $articleImg.src = res.data.url;
            $articleImg.style.width = '128px';
            $articleImg.style.height = '128px';
        });
    };

    // $articleItem = document.getElementById('articleItem');
    // $articleItemList = document.getElementById('articleItemList');
    //
    // $articleItem.onclick = (e) => {
    //     e.stopPropagation();
    //     $articleItemList.style.display = 'block'
    // };

    const $articleItem = document.getElementById('articleItem');
    const $articleItemList = document.getElementById('articleItemList');
    const $itemName = document.getElementById('itemName');
    const $tagInput = document.getElementById('tagInput');
    const $draftActionBox = document.getElementById('draftActionBox');
    const $draftedContainer = document.querySelector('.drafted-container');
    const $upArrow = document.querySelector('.up-arrow');
    // const $publishBtn = document.getElementById('publishBtn');

    const $articleType = document.getElementById('articleType');
    const $articleTypeList = document.getElementById('articleTypeList');
    const $typeName = document.getElementById('typeName');
    const $tagsList = document.getElementById('tagsList');
    const $tagItems = document.getElementById('tagItems');
    const $tagCount = document.getElementById('tagCount');


    let isShowArticleItem = false;
    let isShowArticleType = false;
    let isShowDraftBox = false;
    let tagCount = 0;

    // window.addEventListener('popstate', function (e) {
    //     alert('hello');
    // }, false);

    // let content = '';
    // let title = '';
    // let aid = -1;
    // let drafted = 0;
    //
    // $publishBtn.onclick = () => {
    //     title = $articleTitle.value.trim();
    //     content = ue.getContent();
    //     axios.post('/article/save', {
    //         title: title,
    //         content: content,
    //         aid: aid,
    //         drafted: drafted
    //     }).then(res => {
    //         if (res.data.status === 2003) {
    //             aid = res.data.aid;
    //             alert(res.data.data);
    //         } else {
    //             alert('草稿存檔失敗');
    //         }
    //     });
    // };

    $draftActionBox.onclick = (e) => {
        e.stopPropagation();
        if (!isShowDraftBox) {
            $draftedContainer.style.display = 'block';
            $upArrow.style.display = 'block';
        } else {
            $draftedContainer.style.display = 'none';
            $upArrow.style.display = 'none';
        }
        isShowDraftBox = !isShowDraftBox;
    };

    $upArrow.onclick = function (e) {
        e.stopPropagation();
        if (!isShowDraftBox) {
            $draftedContainer.style.display = 'block';
            this.style.display = 'block';
        } else {
            $draftedContainer.style.display = 'none';
            this.style.display = 'none';
        }
        isShowDraftBox = !isShowDraftBox;
    };

    $articleItem.onclick = function (e) {
        e.stopPropagation();
        if (!isShowArticleItem) {
            $articleItemList.style.display = 'block';
            this.style.boxShadow = '0 0 5px #6f4627';
        } else {
            $articleItemList.style.display = 'none';
            this.style.boxShadow = '';
        }
        isShowArticleItem = !isShowArticleItem;
    };

    // $articleItemList.onclick = function (e) {
    //     e.stopPropagation();
    //     const self = e.target;
    //     $itemName.innerHTML = self.getAttribute('data-value') || '請選擇需要投遞的項目';
    //     this.style.display = 'none';
    //     $articleItem.style.boxShadow = '';
    //     isShowArticleItem = !isShowArticleItem;
    // };

    $articleType.onclick = function (e) {
        e.stopPropagation();
        if (!isShowArticleType) {
            $articleTypeList.style.display = 'block';
            this.style.boxShadow = '0 0 5px #6f4627';
        } else {
            $articleTypeList.style.display = 'none';
            this.style.boxShadow = '';
        }
        isShowArticleType = !isShowArticleType;
    };

    // $articleTypeList.onclick = function (e) {
    //     e.stopPropagation();
    //     const self = e.target;
    //     $typeName.innerHTML = self.getAttribute('data-value') || '請選擇';
    //     this.style.display = 'none';
    //     $articleType.style.boxShadow = '';
    //     isShowArticleType = !isShowArticleType;
    // };

    let chkList = [];
    $tagsList.onclick = (e) => {

        $tagInput.value = '';
        $tagSearchResult.style.display = 'none';

        for (const tagItem of tagItemList) {
            $tagsList.appendChild(tagItem);
        }

        const self = e.target;
        const tagName = self.getAttribute('data-tag');

        if (chkList.length >= 3) return false;

        if (tagName) {
            if (chkList.indexOf(tagName) < 0) {
                chkList.push(tagName);
            } else {
                return false;
            }

            tagCount += 1;
            $tagCount.innerText = tagCount;

            if (tagCount === 3) {
                $tagInput.setAttribute('placeholder', '');
                $tagInput.value = '';
                $tagInput.style.backgroundColor = '#fff';
                $tagInput.disabled = true;
            } else if (tagCount >= 1) {
                $tagInput.setAttribute('placeholder', '請輸入關鍵詞檢索標籤');
                $tagInput.disabled = false;
            }

            const span = document.createElement('span');
            span.innerHTML = tagName;
            span.setAttribute('data-tag', tagName);
            span.className = 'span-tag';
            $tagItems.appendChild(span);
        }
        // if (tagName) {
        //
        // }
    };
    // remove selected item
    $tagItems.onclick = function (e) {
        const self = e.target;
        const tagValue = self.getAttribute('data-tag');

        if (tagValue) {
            const tagIdx = chkList.indexOf(tagValue);
            chkList.splice(tagIdx, 1);
            tagCount -= 1;
            $tagCount.innerText = tagCount;
            $tagInput.disabled = false;

            if (tagCount >= 1) {
                $tagInput.setAttribute('placeholder', '請輸入關鍵詞搜索標籤');
            } else {
                $tagInput.setAttribute('placeholder', '請選擇下列熱門標籤');
            }

            this.removeChild(self);
        }
    };

    // 文章發佈
    const $submit = document.getElementById('submit');
    $submit.onclick = () => {
        drafted = 1;
        tagsResultList = [];
        const tagsList = document.getElementById('tagItems').getElementsByTagName('span');
        if (tagsList.length >= 1) {
            for (let item of tagsList) {
                tagsResultList.push(item.getAttribute('data-tag'));
            }
        } else {
            alert('文章的標籤至少要有一個喔');
            return;
        }
        // console.log(tagsResultList);
        // console.log('aid:', aid);
        // console.log('title:', $articleTitle.value.trim());
        // console.log('content:', ue.getContent())
        // console.log('tag:', tagsResultList.join(','));
        // console.log('drafted:', drafted);
        // console.log('article_label:', window.article_label_name);
        // console.log('article_type:', window.article_type_name);
        // axios
        axios.post('/article/save', {
            aid: aid,
            title: $articleTitle.value.trim(),
            content: ue.getContent(),
            drafted: drafted,
            // 正式article
            article_label: window.article_label_name,
            article_type: window.article_type_name,
            article_tag: tagsResultList.join(',')
        }).then(res => {
            // alert(res.data.data);
            if (drafted === 1) {
                setTimeout(() => {
                    location.href = `/detail?aid=${aid}`;
                }, 1000);
            }
        });
        $publishArticleModal.style.display = 'none';
    };
    //
    // let article_label_name = '';
    // const selectItemList = (label_name_arg, label_value_arg) => {
    //     // console.log('selected');
    //     article_label_name = label_name_arg;
    //     const $dropDown = document.querySelector('#itemName > span');
    //     $dropDown.innerHTML = label_value_arg;
    //     const lis = document.querySelectorAll('#articleItemList > li');
    //
    //     for (let item of lis) {
    //         item.className = 'no-selected';
    //
    //         if (item.getAttribute('data-label') === label_name_arg) {
    //             item.className = 'selected';
    //         }
    //     }
    // }
    //
    // let article_type_name = '';
    // const selectType = (type_name_arg, type_value_arg) => {
    //     article_type_name = type_name_arg;
    //     const $type = document.querySelector('#typeName > span');
    //     $type.innerHTML = type_value_arg;
    //     const lis = document.querySelectorAll('#articleTypeList > li');
    //
    //     for (let item of lis) {
    //         item.className = 'no-selected';
    //
    //         if (item.getAttribute('data-article-type') === type_name_arg) {
    //             item.className = 'selected';
    //         }
    //     }
    // }
    // tag search
    const $articleTagsList = document.querySelectorAll('#tagsList > li');
    const $tagSearchResult = document.querySelector('.tag-search-result');
    const $searchStr = document.getElementById('searchStr');
    const $searchResultNum = document.getElementById('searchResultNum');

    const tagItemList = [];
    for (const tagItem of $articleTagsList) {
        tagItemList.push(tagItem);
    }

    $tagInput.oninput = function () {
        const mySearch = this.value.trim().toLowerCase();
        let searchResultNum = 0;

        if (mySearch.length !== 0) {
            $tagSearchResult.style.display = 'block';
        } else {
            $tagSearchResult.style.display = 'none';
        }

        $tagsList.innerHTML = null;

        for (const tagItem of $articleTagsList) {
            let tagName = tagItem.getAttribute('data-tag').toLowerCase();
            if (tagName.indexOf(mySearch) >= 0) {
                searchResultNum += 1;
                $tagsList.appendChild(tagItem);
            }
        }

        $searchStr.innerHTML = mySearch;
        $searchResultNum.innerHTML = searchResultNum.toString();
        //
        // console.log(`相关${mySearch}的搜索有${searchResultNum}个`);
        // console.log(`分别是${resultStrList.slice(0, resultStrList.length-1)}`);

    };

    const $saveAndCancel = document.getElementById('saveAndCancel');
    $saveAndCancel.onclick = () => {
        drafted = 0;
        $publishBtn.click();
        $publishArticleModal.style.display = 'none';
    };

    // // draftedBox

    // console.log($draftedBoxItemList);
    $draftedBoxItemList.onclick = function (e) {
        e.stopPropagation();
        const self = e.target;
        // const self = e.target.title;
        const draftedId = self.getAttribute('data-did');
        const action = self.getAttribute('data-action');
        $draftDesc.innerHTML = '尚未存檔';
        // console.log('this', this);
        // console.log($draftItem);
        // console.log(this.children);
        // console.log(action);
        if (draftedId && !action) {
            // console.log(draftedId);
            // const title = e.currentTarget.querySelector('.draft-item-up').innerHTML;
            // const title = self.getAttribute('data-title');
            // console.log(title);
            axios.post('/article/drafted', {
                aid: draftedId
            }).then(res => {
                if (res.data.status === 2000) {
                    $articleTitle.value = res.data.data.title;
                    ue.body.innerHTML = res.data.data.article_content;
                    // 此時編輯的是哪個草稿
                    aid = res.data.data.aid;
                } else {
                    alert('獲取失敗');
                }
            });
        } else if (action === 'remove') {
            const $draftItem = document.getElementById(draftedId);
            // console.log($draftItem);
            const result = confirm('確認刪除該筆草稿嗎?');
            if (result) {
                axios.post('/article/remove/draft', {
                    aid: draftedId
                }).then(res => {
                    if (res.data.status === 2000) {
                        // console.log('rest num:', res.data.data);
                        $draftNum.innerHTML = res.data.data;
                        this.removeChild($draftItem);
                    } else {
                        alert('刪除失敗');
                    }
                });
            }
        }
    };
    // remove draft
    // $remoteDraft = document.querySelector('.item-close');
    // $remoteDraft.onclick = function (e) {
    //     e.stopPropagation();
    //     console.log(this);
    // };
};