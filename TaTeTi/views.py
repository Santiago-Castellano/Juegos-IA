from django.shortcuts import render
from django.http import  JsonResponse
from IA.tateti import  play_IA


# Create your views here.
def index(request):
    return render(request,'TaTeTi/Index.html')

def play_ai(request):
    board= [0,0,0],[0,0,0],[0,0,0]
    row,col = play_IA(board)
    board[row][col] = 1
    
    return JsonResponse(
        {
            "row":row,
            "col":col
        }
    )

