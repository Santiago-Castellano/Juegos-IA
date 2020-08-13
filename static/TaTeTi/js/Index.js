$("#board tbody tr td").click(function () {
    if ($(this).hasClass("player") ||$(this).hasClass("ai") ) {
        alert("the cell is locked");
        return 
    }
    $(this).addClass("player");
    what_show(false);
    play_ai();
})

function what_show(board) {
    if (board) {
        $("#board").show();
        $("#message").hide();
    }else{
        $("#board").hide();
        $("#message").show();
    }
}
$(what_show(true))

function play_ai(){
    $.ajax({
        type: "GET",
        url:"/tateti/play_ai/",
        dataType:'json',
        data: {},
        success:function(data){
            console.log(data);
        },
        error: function(error){
            console.log(error)
        },
        complete:function(){
            what_show(true);
        }
    });
}