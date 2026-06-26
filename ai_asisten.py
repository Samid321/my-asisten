import uuid
import requests
from langchain.agents import create_agent
import langchain
from dotenv import load_dotenv
from tools.wether_cek import get_wether
from tools.code import Buat_file ,check_workspace,Baca_file,tambah_data_setelah,tambah_html_body,update_file
from langgraph.checkpoint.memory  import InMemorySaver
from langgraph.store.memory import InMemoryStore
from promt import prompt
from langchain.tools import ToolRuntime,tool
from dataclasses import dataclass
from tools.memory import simpan_memory,baca_memory
from langgraph.prebuilt import  ToolNode
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain.messages import HumanMessage,AnyMessage
from langchain_ollama.chat_models import ChatOllama

import operator

@dataclass
class context:
    user_id:str
@dataclass
class responsee:
    wind_speed=str
@tool('lokasi', description='melihat kota dimana user berada')
def kota(runtime:ToolRuntime[context]):
    match runtime.context.user_id:
        case "abcd":
            return 'jakarta'
        case 123:
            return 'pekanbaru'
        case "a":
            return 'banda aceh'

load_dotenv()
check_point=InMemorySaver()
memory=InMemoryStore()
chatModel='qwen2.5:7b '
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int
tools=[Buat_file,check_workspace,Baca_file,tambah_data_setelah,tambah_html_body,update_file,]
model=ollama=ChatOllama(model=chatModel)
model=model.bind_tools(tools)

tool_node = ToolNode(tools)
def llm_node(state:MessagesState):
    response=model.invoke(state['messages'])
    return {"messages": [response]}

def Router(state):
    last_message=state['messages'][-1]
    if last_message.tool_calls:
        return 'tool'
    return END
graph_builder=StateGraph(MessagesState)
graph_builder.add_node(
    'llm',
    llm_node,
)
graph_builder.add_node(
    'tool',
    tool_node,
)
graph_builder.add_edge(START, 'llm')
graph_builder.add_edge('tool', 'llm')
graph_builder.add_conditional_edges('llm', Router)
graph_builder.add_edge('llm', END)
graph=graph_builder.compile(checkpointer=check_point)
confik={"configurable":{'thread_id':'1'}}
while True:
    user_input=input("masukan perintah: ")
    try:
        result=graph.invoke({'messages': [{'role': 'user', 'content': user_input}]}, config=confik)
    except Exception as e:        print(f"error: {str(e)}")
    print(result['messages'][-1].content)
    print("Tool\n" + result['messages'][1].tool_calls[0]['name'])