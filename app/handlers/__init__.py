from .chat import chat_comand
from .messages import start
from .messages.event import doc_comand, state_comand, subscription_command, main
from .messages.ai import ai_comand

labelers = [
    doc_comand.labeler,
    state_comand.labeler,
    start.labeler,
    main.labeler,
    subscription_command.labeler,
    chat_comand.chat_labeler,
    ai_comand.labeler
]

__all__ = ["labelers"]
