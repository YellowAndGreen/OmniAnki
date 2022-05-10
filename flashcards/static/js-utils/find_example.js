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