from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Course, Question, Choice, Submission, Enrollment


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

    submission = Submission.objects.create(enrollment=enrollment)
    total_score = 0

    questions = Question.objects.filter(course=course)

    for question in questions:
        selected_choice_id = request.POST.get(str(question.id))

        if selected_choice_id:
            choice = Choice.objects.get(id=selected_choice_id)
            submission.choices.add(choice)

            if choice.is_correct:
                total_score += question.grade

    submission.score = total_score
    submission.save()

    return redirect(
        'show_exam_result',
        course_id=course.id,
        submission_id=submission.id
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, id=course_id)
    submission = get_object_or_404(Submission, id=submission_id)

    context = {
        'course': course,
        'submission': submission,
        'score': submission.score,
        'choices': submission.choices.all()
    }

    return render(request, 'onlinecourse/exam_result.html', context)

