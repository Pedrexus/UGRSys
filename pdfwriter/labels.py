from django.template.loader import get_template

"""
def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
"""

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    return html
    #result = io.BytesIO()
    #pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)

    #if 'pdf' in request.GET:
    #    return render_to_pdf_response(request, 'label.html', {})

    #if not pdf.err:
     #   return HttpResponse(result.getvalue(), content_type="application/pdf")
    #return None