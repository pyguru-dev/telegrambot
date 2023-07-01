from django.core.handlers.wsgi import WSGIRequest

from instruction.models import InstructionSection


def instruction_sections(request: WSGIRequest) -> dict:
    return {'instruction_sections': InstructionSection.objects.all()}
