(function(){
  var jquery_version = '3.4.1';
  var site_url = 'https://127.0.0.1:8000/';
  var static_url = site_url + 'static/';
  var min_width = 100;
  var min_height = 100;

  function bookmarklet(msg) {
    // 添加单词查询弹出窗
    let box_html = '<div id="result"></div>>';
    jQuery('body').append(box_html);
  }

// 载入jquery和bootstrap等
  if(typeof window.jQuery != 'undefined') {
    bookmarklet();
  } else {
    // Check for conflicts
    let conflict = typeof window.$ != 'undefined';
    // 加入jquery，bootstrap

    let scripts = ['https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js',
      'https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/5.1.3/scss/_accordion.scss',
      'https://cdn.bootcdn.net/ajax/libs/popper.js/2.11.4/cjs/popper.min.js',
      'https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/5.1.3/js/bootstrap.min.js',
      'https://cdn.bootcdn.net/ajax/libs/crypto-js/4.1.1/crypto-js.js'
    ]
    for(let source of scripts){
        let script = document.createElement('script');
        script.src = source;
        document.head.appendChild(script);
    }
    let link = document.createElement('link');
    link.href = 'https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/5.1.3/css/bootstrap.min.css'
    link.rel = 'stylesheet'
    document.head.appendChild(link);
    // Create a way to wait until script loading
    let attempts = 15;
    (function(){
      // Check again if jQuery is undefined
      if(typeof window.jQuery == 'undefined') {
        if(--attempts > 0) {
          // Calls himself in a few milliseconds
          window.setTimeout(arguments.callee, 250)
        } else {
          // Too much attempts to load, send error
          alert('An error occurred while loading jQuery')
        }
      } else {
          bookmarklet();
      }
    })();
  }
})()




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


    $.get('http://127.0.0.1:8000/flashcards/dict_query_get/'+word.toString(),
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
function find_example_and_trans() {
    // 查询的文本
    let dictHtml = $('.query_word_result').html()
    // 过滤出例句和翻译
    let raw_examples = dictHtml.match(/<font color="#008080">.*?<\/font><\/div>/g)
    // 遍历例句放入两个列表中
    let examples = []
    let translations = []
    let meanings = []
    raw_examples.map((raw_example)=>{
        let example_and_tran = raw_example.replace(/(<.*?>|<\/.*?>)/g, "")
        // 分割英文和中文，以中文第一个字切割
        let first_chinese = example_and_tran.match(/[\u4e00-\u9fa5]/).index
        let example = example_and_tran.slice(0,first_chinese)
        let translation = example_and_tran.slice(first_chinese,)
        examples.push(example)
        translations.push(translation)
    })
    // 全局匹配不能使用子表达式，所以只有去除外边的部分
    meanings = dictHtml.match(/<font style="color:navy;margin-left:12pt;" ?>(.*?)<\/font>/g).map((translation)=>translation.replace(/(<.*?>|<\/.*?>)/g, ""))
    return [examples,translations,meanings]
}
let result
function getExample(){
    results = find_example_and_trans()
    for (let index in results[0]) {
        $('#example_select').append('<option value='+String(index)+'>'+results[0][index]+'</option>')
    }
    if (exampleInText !== '') {
        $('#example_select').append('<option value=' + String(-1) + '>' + exampleInText + '</option>')
    }
    for (let index in results[2]) {
        $('#select_word_meaning').append('<option value='+String(index)+'>'+results[2][index]+'</option>')
    }
}

function insertExample() {
    var result_index = $('#example_select option:selected').val()
    if (result_index >= 0) {
        $('#floatingInput3').val(results[0][result_index])
        $('#floatingInput4').val(results[1][result_index])
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
        // console.log(current_meaning + '<br>' + attr +meaning)
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


$('#audio_button').on('click',function () {
    $('#audio').attr('src','http://dict.youdao.com/dictvoice?audio='+data_query_word)
    const audio = document.getElementById("audio")
    audio.play()
})




// //失败的跨域请求
// $.ajax({
//     url: 'http://127.0.0.1:8000/flashcards/dict_query_get/find/',
//     headers: {
//         'Content-Type': 'application/x-www-form-urlencoded',
//     },
//     type: "POST", /* or type:"GET" or type:"PUT" */
//     dataType: "json",
//     data: {
//         query_word: 'find',
//     },
//     success: function (result) {
//         console.log(result);
//     },
//     error: function () {
//         console.log("error");
//     }
// });

