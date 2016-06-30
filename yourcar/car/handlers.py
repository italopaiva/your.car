
class HelpView(TemplateCommandView):
    template_text = "bot/messages/command_help_text.txt"

urlpatterns = [command('help', HelpView.as_command_view()),
]