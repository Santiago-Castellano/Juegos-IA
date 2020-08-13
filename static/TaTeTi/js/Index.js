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
    let board = []
    $("#board tbody tr").each(function (){
        let row = [];
        $(this).find("td").each(function (){
            if ($(this).hasClass("ai")){
                row.push(1) 
            }else if ($(this).hasClass("player")){
                row.push(-1) 

            }
            else{
                row.push(0) 
            }
        })
        board.push(row);
    });
    
    $.ajax({
        type: "GET",
        url:"/tateti/play_ai/",
        dataType:'json',
        data: {
            board
        },
        success:function(data){
            $("#board tbody tr").each(function (){
                if ($(this).data("row") == data.row) {
                    $(this).find("td").each(function (){
                        if ($(this).data("col") == data.col){
                            $(this).addClass("ai");
                        }
                    })
                } 
                
            });
        },
        error: function(error){
            console.log(error)
        },
        complete:function(){
            what_show(true);
        }
    });
}

function play_again(){
    $("#board tbody tr td").each(function () {
        if ($(this).hasClass("player")) {
            $(this).removeClass("player")
        }
        if ($(this).hasClass("ai")) {
            $(this).removeClass("ai")
        }
    });
}