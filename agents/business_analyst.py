from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# TODO: Make the agent ask questions for vague inputs given by the human to save token cost.
# TODO: Use prompt caching
# TODO: Remove the need for seperate prompt templates for generating stories and refinements.
# TODO: Implement Agent Manager Design pattern
class BusinessAnalystAgent:
    """
    The BusinessAnalyst Agent goal is to act as a tool for Product Manager to generate 
    comprehensive user stories with well defined scoped acceptance criteria for a given set 
    of feature requirement(s).
    
    It keeps PM in the loop by reviewing and making further refinements till the PM is satisfied
    with the generated set of stories and acceptance criteria. This loop allows to have a cross communication
    between the agent and human allowing to thus cover up any gaps or contradictions.
    """
    
    
    # Prompt Templates
    prompt_template = """
You are a seasened Business Analyst at {company} with deep product knowledge.
Given the product context:
----------------------------------------
{context}
----------------------------------------
And the feature request:
----------------------------------------
{feature_request}
----------------------------------------
Generate detail user stories with acceptance criteria. The stories should follow following instructions:
1. The user stories should stick to the functionality and should not related to doc or testing tasks.
2. Each story should not be oversized and should be scoped logically to fit in 1 sprint.
3. The story acceptance criteria are written in GHERKIN format.

Review your output to ensure for any gaps or contractictions.

The Response Format/Output:
Story 1: <User Story 1>
Acceptance Criteria:
- <AC 1.1>
- <AC 1.2>
- ...

... 

Story n: <User Story n>
Acceptance Criteria:
- <AC n.1>
- <AC n.2>
- ...
"""

    review_stories_prompt_template = """
You are a seasened Business Analyst at {company} with deep product knowledge.
Given the previously generated user stories:
----------------------------------------
{previous_output}
----------------------------------------
And the user feedback on those stories:
----------------------------------------
{user_feedback}
----------------------------------------
Refine the user stories based on the feedback. Return the output in similar format as before.
"""

    def __init__(self, llm, company):
        self.company = company
        self.initial_prompt = PromptTemplate(name="Business Analyst", template=self.prompt_template, input_variables=["company", "context", "feature_request"])
        self.initial_chain = LLMChain(llm=llm, prompt=self.initial_prompt)
        self.review_stories_prompt = PromptTemplate(name="Business Analyst Refine Stories", template=self.review_stories_prompt_template, input_variables=["company", "previous_output", "user_feedback"])
        self.review_stories_chain = LLMChain(llm=llm, prompt=self.review_stories_prompt)

    def generate_stories(self, feature_request: str, context: str) -> str:
        return self.initial_chain.run(company=self.company, context=context, feature_request=feature_request)

    def refine(self, previous_output: str, feedback: str) -> str:
        return self.review_stories_chain.run(company=self.company, previous_output=previous_output, user_feedback=feedback)
