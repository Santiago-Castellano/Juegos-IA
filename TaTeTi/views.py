from django.shortcuts import render
from django.http import  JsonResponse
from IA.tateti import  play_IA


# Create your views here.
def index(request):
    return render(request,'TaTeTi/Index.html')

def play_ai(request):
    if request.GET and request.is_ajax():
        data = dict(request.GET)
        row_one = list(map(int,  data["board[0][]"]))
        row_two = list(map(int,  data["board[1][]"]))
        row_three= list(map(int, data["board[2][]"]))
        board= row_one , row_two , row_three
        if 0 not in (row_one+row_two+row_three):
            return JsonResponse(
                {
                    "row":-1,
                    "col":-1
                }
            )
        row,col = play_IA(board)
        return JsonResponse(
            {
                "row":row,
                "col":col
            }
        )

