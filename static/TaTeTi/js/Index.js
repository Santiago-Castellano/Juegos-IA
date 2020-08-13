$(start())
function start(){
    let n =  Math.random();
    if (n > 0.5){
        play_ai()
    }else{
        what_show(true)
    }
}
$("#board tbody tr td").click(function () {
    if ($(this).hasClass("player") ||$(this).hasClass("ai") ) {
        alert("the cell is locked");
        return 
    }
    $(this).addClass("player");
    if (!end_game()) {
        what_show(false);
        play_ai();
    }
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


function get_board(){
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
    return board
}

function play_ai(){
    let board = get_board()
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
            end_game();
            
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
    start();
}

function end_game(){
    $("#board tbody tr").each(function () {
        if ($(this).find(".player").length == 3) {
            alert("You WIN!!");
            return true;
        }
        if ($(this).find(".ai").length == 3) {
            alert("You LOST!!");
            return true;
        }
    });
    let board = get_board();
    let main = board[0][0] + board[1][1] + board[2][2]; 
    for (let col = 0; col < 3; col++) {
        let sum_col = board[0][col] + board[1][col] + board[2][col];
        if (sum_col == 3) {
            alert("You LOST!!");
            return true;
        }
        if (sum_col == -3) {
            alert("You WIN!!");
            return true;
        }
    }
    if (main == 3) {
        alert("You LOST!!");
        return true;
    }
    if (main == -3) {
        alert("You WIN!!");
        return true;
    }
    let secondary = board[0][2] + board[1][1] + board[2][0]; 
    if (secondary == 3) {
        alert("You LOST!!");
        return true;
    }
    if (secondary == -3) {
        alert("You WIN!!");
        return true;
    }

    return false;
}