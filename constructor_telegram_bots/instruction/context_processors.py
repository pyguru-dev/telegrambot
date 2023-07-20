from .models import InstructionSection


def instruction_sections(*args, **kwargs) -> dict:
    return {'instruction_sections': InstructionSection.objects.all()}
