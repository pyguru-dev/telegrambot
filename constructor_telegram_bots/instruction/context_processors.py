from django.http import HttpRequest

from instruction.models import InstructionSection


def instruction_sections(request: HttpRequest) -> dict:
    return {'instruction_sections': InstructionSection.objects.all()}
