(function(){
  var jquery_version = '3.4.1';
  var site_url = 'https://127.0.0.1:8000/';
  var static_url = site_url + 'static/';
  var min_width = 100;
  var min_height = 100;

  function bookmarklet(msg) {
    // 添加单词查询弹出窗
    let box_html = '<div id="result" style="width: 400px;height: 400px;overflow: auto" ></div>>';
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
    ]
    for(let source of scripts){
        let script = document.createElement('script');
        script.src = source;
        document.head.appendChild(script);
    }

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

    $.get('http://127.0.0.1:8000/flashcards/dict_query_get/'+word.toString(),
    function(data){
      $("#result").html(data["html_result"])
      window.getSelection().empty();
    }
  );

    //在此处可能会占用更多资源，在点开添加单词时再使用
    //translate(exampleInText)
  }

}
$("body").on("click",function(e){
    getWord(e);
});


