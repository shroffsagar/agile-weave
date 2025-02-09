from common.utils import CommonUtils
import logging
from langchain_openai import ChatOpenAI
from agents import BusinessAnalystAgent, SoftwareTesterAgent
from rag.utils import RAGContext, DocumentCreator, TextSplitterType
from fetchers.metabase import MetabaseFetcher
from enum import Enum
import chainlit as cl

# TODOS:
# TODO: Refactor to build statement inside the agents itself or by using Agent-Manager pattern this explicit state manage in the app should go away.
# TODO: Currently the chainlit application has some coupling to Metabase product for demonstration purpose..

##################################################################
# Constants
# Model to use
LLM_MODEL = "gpt-4o-mini-2024-07-18"
# Global state dictionary to track the conversation between agents
class Stage(Enum):
        FEATURE_REQUEST = "feature_request"
        BA = "BA"
        TESTER = "Tester"
        COMPLETED = "Completed"
company = "Metabase"
State = {
    "STAGE": Stage.FEATURE_REQUEST,  # stages supported : FEATURE_REQUEST, BA, TESTER, COMPLETED
    "FEATURE_REQUEST": None,
    "CONTEXT": None,
    "BA_OUTPUT": None,
    "TESTER_OUTPUT": None
}

##################################################################
# Scrape the data and initialize vector database for RAG
# Initialize the llm
try:
    OPENAI_API_KEY = CommonUtils.load_openai_key()
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is missing or could not be loaded.")
    
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name=LLM_MODEL, temperature=0)
    fetcher = MetabaseFetcher()
    scraped_expression_data = fetcher.fetch_expressions_data()
    documents = DocumentCreator(splitter_type=TextSplitterType.RECURSIVE).create_documents(full_text=scraped_expression_data)
    rag = RAGContext(OPENAI_API_KEY, documents=documents)
except Exception as e:
    logging.error(f"Initialization error: {str(e)}", exc_info=False)
    exit(1)

##################################################################
# Initialize agents
# TODO: Refactor the project to use AgentManager design.
business_analyst_agent = BusinessAnalystAgent(company=company, llm=llm)
software_tester_agent = SoftwareTesterAgent(company=company, llm=llm)

##################################################################
# Start chainlit app for workflow
@cl.on_chat_start
@CommonUtils.async_error_handler
async def on_chat_start():
    await cl.Message(content=f"👋 Welcome to the AgileWeave! Please enter your high-level feature request for {company}:").send()

@cl.on_message
@CommonUtils.async_error_handler
async def on_message(message: cl.Message):
    global State
    
    try:
        if State["STAGE"] == Stage.FEATURE_REQUEST:
            State["FEATURE_REQUEST"] = message.content.strip()
            State["CONTEXT"] = rag.retrieve_context(query=State["FEATURE_REQUEST"], k=3)
            await cl.Message(content="⏳ Business Analyst is generating stories, please wait...").send()
            await cl.Message(content="").send()
            State["BA_OUTPUT"] = business_analyst_agent.generate_stories(feature_request=State["FEATURE_REQUEST"], context=State["CONTEXT"])
            State["STAGE"] = Stage.BA
            await cl.Message(content=f"✅ **Business Analyst Output (User Stories):**\n{State['BA_OUTPUT']}").send()
            await cl.Message(content="💬 Please provide feedback to refine the user stories or type 'approved' if satisfied.").send()

        elif State["STAGE"] == Stage.BA:
            feedback = message.content.strip()
            if feedback.upper() == "APPROVED":
                await cl.Message(content="✅ User stories approved.").send()
                await cl.Message(content="⏳ Software Tester is generating Test Plan, please wait...").send()
                await cl.Message(content="").send()
                State["TESTER_OUTPUT"] = software_tester_agent.generate_testplan(user_stories=State["BA_OUTPUT"], context=State["CONTEXT"])
                State["STAGE"] = Stage.TESTER
                await cl.Message(content=f"✅ **Tester Output (Test Plan):**\n{State['TESTER_OUTPUT']}").send()
                await cl.Message(content="💬 Please provide feedback to refine test plan further or type 'approved' if satisfied.").send()
            else:
                await cl.Message(content=f"⏳ Business Analyst is refining the user stories based on user feedback {feedback}, please wait...").send()
                await cl.Message(content="").send()
                State["BA_OUTPUT"] = business_analyst_agent.refine(previous_output=State["BA_OUTPUT"], feedback=feedback)
                State["STAGE"] = Stage.BA
                await cl.Message(content=f"✅ **Business Analyst Output (Refined User Stories):**\n{State['BA_OUTPUT']}").send()
                await cl.Message(content="💬 Please provide feedback to refine the user stories or type 'approved' if satisfied.").send()

        elif State["STAGE"] == Stage.TESTER:
            feedback = message.content.strip()
            if feedback.upper() == "APPROVED":
                State["STAGE"] = Stage.COMPLETED
                await cl.Message(content=f"**✅ Final Approved Test Plan:**\n{State['TESTER_OUTPUT']}").send()
                await cl.Message(content="🎉 All stages are complete. Thank you for using Agile Weave!").send()
            else:
                await cl.Message(content=f"⏳ Software Tester is refining Test Plan based on user feedback {feedback}, please wait...").send()
                await cl.Message(content="").send()
                State["TESTER_OUTPUT"] = software_tester_agent.refine(previous_output=State["TESTER_OUTPUT"], feedback=feedback)
                State["STAGE"] = Stage.TESTER
                await cl.Message(content=f"✅ **Tester Output (Refined Test Plan):**\n{State['TESTER_OUTPUT']}").send()
                await cl.Message(content="💬 Please provide feedback to refine test plan further or type 'approved' if satisfied.").send()
                
    except Exception as e:
        logging.error(f"Error in message handler: {str(e)}", exc_info=True)
        State["STAGE"] = Stage.FEATURE_REQUEST  # Reset state on error
        await cl.Message(content=f"❌ An error occurred: {str(e)}").send()
