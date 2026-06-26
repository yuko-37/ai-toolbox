from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

from image_agent import ImageAgent

class ImageAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent = ImageAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        prompt = context.get_user_input()
        response = self.agent.process_request(prompt)
        message = new_agent_text_message(response)
        await event_queue.enqueue_event(message)


    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError('Cancel is not supported')
