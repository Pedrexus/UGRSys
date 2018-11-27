from django.core.validators import RegexValidator

message_phone_regex = "O número de telefone deve estar no formato:" \
                      " '+999999999'." \
                      " Até 15 dígitos são permitidos."
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message=message_phone_regex)

message_percentages_regex = "Liste percentuais inteiros" \
                            " separando-os por vírgulas, " \
                            "e.g., 20%, 30%, 5%"
percentages_regex = RegexValidator(
    regex=r'(^$)|(^(\d+?%)(,\s*\d+?%)*$)',
    message=message_percentages_regex)
