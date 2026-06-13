from typing import Annotated, TypedDict, List, Any
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


class CoachGraph:
    class State(TypedDict):
        messages: Annotated[List[Any], add_messages]
        model: str

    def __init__(self):
        self._graph = self._build_graph()

    def invoke(self, message, model, thread_id):
        state = {
            "messages": [HumanMessage(content=message)],
            "model": model
        }
        config = {"configurable": {"thread_id": thread_id}}
        response_state = self._graph.invoke(state, config=config)
        return response_state['messages'][-1]


    def _build_graph(self):
        graph_builder = StateGraph(CoachGraph.State)

        def ask_llm(state: CoachGraph.State) -> CoachGraph.State:
            llm = ChatOpenAI(model=state['model'])
            reply = llm.invoke(state['messages'])
            new_state = {
                "messages": [reply]
            }
            return new_state

        graph_builder.add_node('ask_llm', ask_llm)
        graph_builder.add_edge(START, 'ask_llm')

        memory = MemorySaver()
        return graph_builder.compile(checkpointer=memory)