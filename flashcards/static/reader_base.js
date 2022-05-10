//字典及弹窗
var toastTrigger = document.getElementById('liveToastBtn')
var toastLiveExample = document.getElementById('liveToast')
var exampleInText = ''
var data_query_word


function getWord(e){
  var word = window.getSelection?    window.getSelection():    document.selection.createRange().text
  if (word.toString()!=="") {
    //若选中的不是英文则结束函数
    //在单词添加输入框内选中也结束函数
    if (word.toString().match('[\u4e00-\u9fa5]') !== null||e.target.nodeName === 'INPUT'||e.target.nodeName === 'TEXTAREA') {
        return
    }
    /*
    word.getRangeAt(0).commonAncestorContainer.textContent获取点击块的文本
    以.分割，通过filter函数找到有对应词的句子，最后加上.
     */
    exampleInText = word.getRangeAt(0).commonAncestorContainer.textContent.split(/[.;]/).filter((ele)=>{return ele.indexOf(word.toString())>=0})+'.'


    $.post('{% url "flashcards:dict_query" %}',
    {
      query_word: word.toString()
    },
    function(data){
      $(".query_word_result").html(data["html_result"])
      var toast = new bootstrap.Toast(toastLiveExample)
      toast.show()
      $(".toast-window").css("display",'inline')
      data_query_word = data["query_word"]
      $("#floatingInput1").val(data_query_word)
      $('#audio_text').text(data_query_word)
      window.getSelection().empty();
    }
  );
    $('#floatingInput3').val(exampleInText)
    //在此处可能会占用更多资源，在点开添加单词时再使用
    //translate(exampleInText)
  }

}
    // 防止阻挡到其他元素
$(".toast-window-close").click(function(){
    $(".toast-window").css("display",'none')
})


$("body").on("click",function(e){

    getWord(e);

});

$("body").on('click',function (e) {
    // 在弹出框之外点击删除弹出框，添加单词以及退出添加不删除
    if($(".toast-window").css("display") !== 'none'&&e.target.className!==' query_word_result '
        &&e.target.className!=='toast-body'&&e.target.className!==''&&e.target.className!=='ms-auto'
        &&e.target.className!=='offcanvas-backdrop fade' && e.target.nodeName !== 'BUTTON'
        && e.target.nodeName !== 'INPUT' && e.target.nodeName !== 'SELECT' && e.target.nodeName !== 'TEXTAREA'
    ){
        $(".toast-window").css("display",'none');
        //console.log(e.target.className)
    }
})

$("body").on("touchstart",function(e){
    setTimeout(function (){
        getWord(e);
    }, 1000);
    window.getSelection().empty();

});

//添加表单
var results
var meanings
function getExample(){
  var word = $("#floatingInput1").val()
  if (word!=="") {
    $.post('{% url "flashcards:get_example" %}',
    {
      query_word: word
    },
    function(data){
        results = $.parseJSON(data['example'])
        meanings = $.parseJSON(data['meanings'])
        console.log(meanings)
        $('#example_select option').remove()
        $('#select_word_meaning option').remove()
        for (var index in results) {
            $('#example_select').append('<option value='+String(index)+'>'+results[index][0]+'</option>')
        }
        if (exampleInText !== '') {
            $('#example_select').append('<option value=' + String(-1) + '>' + exampleInText + '</option>')
        }

        for (var index2 in meanings) {
            $('#select_word_meaning').append('<option value='+String(index2)+'>'+meanings[index2]+'</option>')
        }
    }
  );
  }
}

    function insertExample() {
        var result_index = $('#example_select option:selected').val()
        if (result_index >= 0) {
            $('#floatingInput3').val(results[result_index][0])
            $('#floatingInput4').val(results[result_index][1])
        }
        else {
            $('#floatingInput3').val(exampleInText)
            translate(exampleInText)
        }
    }
    function insertMeaning() {
        let meaning = $('#select_word_meaning option:selected').text()
        let attr = $('#select_word_attr option:selected').text()
        //此处应为追加，而不是覆盖
        let current_meaning = $('#floatingInput2').val()
        //若存在释义，则先换行
        if (current_meaning!=='') {
            console.log(current_meaning + '\n' + attr +meaning)
            $('#floatingInput2').val(current_meaning + '\n' + attr +meaning)
        }
        else {
            $('#floatingInput2').val(attr+meaning)
        }
    }
$('#find_example').on("click",function(){
    getExample()
});
$('#insert_example').on("click",function(){
    insertExample()
});
//插入词义
$('#insert_attr_meaning').on('click',function () {
    insertMeaning()
})
// 提交添加单词表单
function addWordForm() {
    $.post('{% url "flashcards:word_add" %}',
        {
            group: $('input[name=group]').val(),
            question: $('input[name=question]').val(),
            answer: $('textarea[name=answer]').val(),
            example: $('textarea[name=example]').val(),
            translation: $('textarea[name=translation]').val(),
            extra: $('input[name=extra]').val(),
            tag: $('input[name=tag]').val(),
        },
        function (data) {
            $("#close_add_word").trigger("click")
            if (data['status']==='ok'){
                $("#word_add_info").css('display','block')
            }
            else {
                $('#word_add_text').text('添加失败')
            }
            $('#floatingInput2').val('')
        }
    );
}
$('#word_add_submit').on("click",function(){
    addWordForm()
});

$('#AddWordButton').on('click',function () {
    translate(exampleInText)
})


//获取划词句子翻译
var appKey = '3e1685d354478356';
var key = '6SdjUOzdnN3QWZAQ4vS5nFTnJdO168jr';//注意：暴露appSecret，有被盗用造成损失的风险

// 多个query可以用\n连接  如 query='apple\norange\nbanana\npear'
var from = 'en';
var to = 'zh-CHS';

// 词表id不能相同，时间不能相同
var vocabId =  1;

function translate(query) {
    var salt = (new Date).getTime();
    var curtime = Math.round(new Date().getTime()/1000);
    var str1 = appKey + truncate(query) + salt + curtime + key;
    var sign = CryptoJS.SHA256(str1).toString(CryptoJS.enc.Hex);
    var vocabIdStr = String(vocabId)
    vocabId++
    $.ajax({
    url: 'https://openapi.youdao.com/api',
    type: 'post',
    dataType: 'jsonp',
    data: {
        q: query,
        appKey: appKey,
        salt: salt,
        from: from,
        to: to,
        sign: sign,
        signType: "v3",
        curtime: curtime,
        vocabId: vocabIdStr,
    },
    success: function (data) {
        console.log(data);
        $('#floatingInput4').val(data['translation'][0])
    }
});
}
function truncate(q){
    var len = q.length;
    if(len<=20) return q;
    return q.substring(0, 10) + len + q.substring(len-10, len);
}

//图片加载
var t_img; // 定时器
var isLoad = true; // 控制变量

// 判断图片加载状况，加载完成后回调
isImgLoad(function(){
    // 加载完成的回调函数
    $('img').removeClass('placeholder')
});

// 判断图片加载的函数
function isImgLoad(callback){
    // 注意我的图片类名都是cover，因为我只需要处理cover。其它图片可以不管。
    // 查找所有封面图，迭代处理
    $('img').each(function(){
        // 找到为0就将isLoad设为false，并退出each
        if(this.height === 0){
            isLoad = false;
            return false;
        }

    });
    // 为true，没有发现为0的。加载完毕
    if(isLoad){
        clearTimeout(t_img); // 清除定时器
        // 回调函数
        callback();
    // 为false，因为找到了没有加载完成的图，将调用定时器递归
    }else{
        isLoad = true;
        t_img = setTimeout(function(){
            isImgLoad(callback); // 递归扫描
        },500); // 我这里设置的是500毫秒就扫描一次，可以自己调整
    }
}

$('#audio_button').on('click',function () {
    $('#audio').attr('src','http://dict.youdao.com/dictvoice?audio='+data_query_word)
    const audio = document.getElementById("audio")
    audio.play()
})