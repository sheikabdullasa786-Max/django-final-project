from django.http import HttpResponse

def submit(request):
    return HttpResponse("Exam submitted")

def show_exam_result(request):
    return HttpResponse("Exam result")
