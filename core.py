from gluon import SELECT, OPTION, TAG
from models import OPCIONES

def validate(Table, values):
    errors = {}

    for key in values.keys():
        if Table[key].requires:
            if isinstance(Table[key].requires, list):
                for validator in Table[key].requires:
                    result = validator(values[key])
                    if result[1]:
                        errors[key] = result[1]
                        break
            
            if callable(Table[key].requires):
                result = Table[key].requires(values[key])
                if result[1]:
                    errors[key] = result[1]

    if errors:
        return errors


def select(value, opts):
    options = OPCIONES.get(opts)
    result = TAG[''](*[OPTION(item,
                            _value=item.lower(),
                            _selected=value.lower() == item.lower())
                            for item in options])
    return result