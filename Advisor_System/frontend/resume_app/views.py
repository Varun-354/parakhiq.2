from django.shortcuts import render
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../')
    )
)

from phase_3 import full_resume_analysis

def home(request):
    if request.method == "POST":

        uploaded_file = request.FILES['resume']

        save_path = uploaded_file.name

        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        result = full_resume_analysis(save_path)
        request.session["report_data"] = result
        os.remove(save_path)

        print(result)

        return render(request, 'resume_app/result.html', {
            'result': result
        })

    return render(request, 'resume_app/index.html')


from django.http import HttpResponse
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def download_report(request):

    report = request.session.get("report_data")

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("ParakhIQ Resume Report", styles["Title"])
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Predicted Role: {report['predicted_role']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Resume Score: {report['final_resume_evaluation']['final_score']}%",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            "Skills: " + ", ".join(report["skills"]),
            styles["Normal"]
        )
    )

    doc.build(content)

    buffer.seek(0)

    return HttpResponse(
        buffer,
        content_type="application/pdf"
    )