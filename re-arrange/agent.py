from pydantic import BaseModel, Field
from langchain_deepseek.chat_models import ChatDeepSeek
from config import settings
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send

# model
llm_model = ChatDeepSeek(
    api_key=settings.DS_API_KEY,
    model_name=settings.DS_MODEL,
    max_tokens=8192,
    temperature=1.5,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=2
)


# States

class Subjects(BaseModel):
    subjects: list[{
        "title":Field(description="")
    }]


class OverallState(BaseModel):
    raw_content: str
    outline: str
    subjects: Subjects


# Nodes
def generate_outline(state: OverallState):
    _prompt_template = """你需要先理解以下提供的内容,从专业的角度对你认为必要的部分进行合并或拆分,按照你对该内容的理解按照一定逻辑顺序重新进行编排,然后再将你的结果以列表的形式返回。
------
{raw_content}
------
"""
    _prompt = _prompt_template.format(raw_content=state["raw_content"])
    response = llm_model.with_structured_output(Subjects).invoke(_prompt)
    return {"subjects": response.subjects}


def outline_deliver(state: OverallState):
    return [Send("generate_content_from_outline", {"subject": s}) for s in state["subjects"]]


def generate_content_from_outline(state: OverallState):
    _prompt = """你需要在以下内容中提炼出与{subject}相关的内容,并进行整理
------
{raw_content}
------
    
"""

    pass


# Graph
builder = StateGraph(OverallState)
builder.add_node(generate_outline)
builder.add_node(generate_content_from_outline)

builder.add_edge(START, 'generate_outline')
builder.add_conditional_edges("generate_topics", outline_deliver, ["generate_content_from_outline"])
builder.add_edge('generate_content_from_outline', END)

graph = builder.compile()

if __name__ == '__main__':
    with open('input.md', 'r', encoding="utf-8") as f:
        raw_content = f.read()

    print(generate_outline({"raw_content": {raw_content}}))
