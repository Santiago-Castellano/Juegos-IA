$("#board tbody tr td").click(function () {
    $(this).addClass("player");
    what_show(false);
    setInterval(function () {
        what_show(true)
    },3000);
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