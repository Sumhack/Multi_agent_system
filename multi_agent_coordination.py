from typing import Literal, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph, START
from pprint import pprint
import os

# Data model for routing
class RouteQuery(BaseModel):
    """Route a user query to the most relevant agent."""
    agent_type: Literal["technical_support_agent", "marketing_data_agent", "generic_agent"] = Field(
        ...,
        description="Route user queries to either technical support agent for technical/product issues, "
                   "marketing agent for market/sales related queries,  generic agent for other queries.",
    )

# State definition
class GraphState(TypedDict):
    """Represents the state of our graph."""
    question: str
    response: str | None
    source: str | None

# Set up LLM configuration
groq_api_key = "groq-api-key"
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma2-9b-It")
structured_llm_router = llm.with_structured_output(RouteQuery)

# Router prompt
system = """You are an expert at routing user questions to the appropriate agent.

Route queries to:
1. technical_support_agent: For questions about technical issues, errors, installation, account problems, or system functionality
2. marketing_data_agent: For questions about pricing, products, features, deals, services, or sales inquiries
3. Generic Agent: For any queries that don't clearly fit technical support or marketing categories

Examples for technical_support_agent:
"How do I fix a device that keeps disconnecting from the Wi-Fi network?"
"What does error code 404 on the streaming app indicate, and how do I resolve it?"
"What should I do if my smart home hub fails to connect to devices?"
"How can I resolve issues with software updates failing on my tablet?"
"What steps should be taken to troubleshoot a printer that's not responding?"
"How can I reset my router to factory settings safely?"
"What are the causes of frequent overheating in a laptop, and how can it be resolved?"
"How do I replace a faulty hard drive without losing data?"
"What steps should be followed to diagnose and fix a slow boot-up process on a desktop?"
"What should I check if my mobile app keeps crashing upon launch?"

Examples for marketing_data_agent:
"What was the conversion rate for campaigns targeting millennials last quarter?"
"How much revenue was generated from email marketing campaigns in September 2024?"
"Which social media platform yielded the highest ROI in Q3 2024?"
"What is the average cost per lead for campaigns in the healthcare sector?"
"How did the launch of [Product Name] impact sales growth in the first month?"
"What was the performance of video ads versus banner ads in Q2 2023?"
"How did Black Friday campaigns influence overall revenue in November 2024?"
"What percentage of ad spend was allocated to retargeting campaigns last year?"
"Which region saw the highest engagement in campaigns promoting seasonal offers?"
"How did competitor pricing changes affect our sales during Q4 2024?"
"How much is the total sales?"
"What is the total sales?"

Examples for generic_agent:

"Hello, how are you?"
"Can you assist me?"
"Tell me a fun fact!"
"How’s the weather today?"
"What’s new?"
"Have a great day ahead!"



"""

route_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "{question}"),
])

# Create router chain
question_router = route_prompt | structured_llm_router

# Define the routing function
def router(state: GraphState):
    """Route the query to the appropriate agent"""
    # Get the routing result
    result = question_router.invoke({"question": state["question"]})
    # Return just the agent_type string
    return result.agent_type

# Agent functions
def technical_support_agent(state: GraphState) -> GraphState:
    """Handle technical support queries"""
    print("---TECHNICAL SUPPORT---")
    question = state["question"]
    response, source = chatbot(question)  # Assuming chatbot is imported
    return {"question": question, "response": response, "source": source}

def marketing_data_agent(state: GraphState) -> GraphState:
    """Handle marketing data queries"""
    print("---MARKETING DATA---")
    question = state["question"]
    response, source = user_query(question)  # Assuming user_query is imported
    return {"question": question, "response": response, "source": source}

def generic_agent(state: GraphState) -> GraphState:
    """Handle generic queries"""
    print("---GENERIC---")
    question = state["question"]
    response = "This query is neither for marketing_data_agent or technical_support_agent"
    source = "No source for the same"
    return {"question": question, "response": response, "source": source}

# Create the workflow
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("technical_support_agent", technical_support_agent)
workflow.add_node("marketing_data_agent", marketing_data_agent)
workflow.add_node("generic_agent", generic_agent)

# Add edges with the router function
workflow.add_conditional_edges(
    START,
    router,  # Use the router function directly
    {
        "technical_support_agent": "technical_support_agent",
        "marketing_data_agent": "marketing_data_agent",
        "generic_agent": "generic_agent",
    }
)

# Add end edges
workflow.add_edge("technical_support_agent", END)
workflow.add_edge("marketing_data_agent", END)
workflow.add_edge("generic_agent", END)

# Compile the workflow
app = workflow.compile()
