from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# TODO: Make the agent ask questions for vague inputs given by the human to save token cost.
# TODO: Use prompt caching
# TODO: Remove the need for seperate prompt templates for generating stories and refinements.
# TODO: Implement Agent Manager Design pattern
class SoftwareTesterAgent:
    """
    The SoftwareTester Agent is a power-user and a subject matter expert on various functionalities the product
    has to offer. It generates comprehensive test plans and test strategies from the given user stories.
    Tests are written from more end-user perspective keeping aside unit test scenarios.
    It covers posive, negative, and corner cases. It organizes in well defined suites with shift left mindset.

    It keeps Software Test Manager in the loop by reviewing and making further refinements till they are satisfied
    with the generated test plan. This loop allows to have a cross communication between the agent and human allowing 
    to thus cover up any gaps or contradictions.
    """
    
    # Prompt Templates
    prompt_template = """
    You are an expert Software Tester at {company} with subject matter expertise in the application and its features.
Given the product context:
----------------------------------------
{context}
----------------------------------------
And the approved user stories from the business analyst:
----------------------------------------
{user_stories}
----------------------------------------
Generate a comprehensive test plan and test strategy for the feature.
Ensure that following is followed while generating the test plan:
1. Generate comprehensive test plan for the given set of acceptance criteria in stories.
2. The test suites are organized as per functionality.
3. Tests focuses on customer use cases instead of unit testing.
4. Tests cover corner cases, in addition to +ve and -ve cases.
5. Tests are written with shift-left in mind, meaning more tests are writtent to test at API layer and less on E2E UI tests.

The test plan should be a Markdown table with the following columns:
- Test Case ID
- Test Case Objective
- Test Case Description with Test Steps
- Test Type (API or UI)
- Expected Result
- Additional notes: use this column for any open pending questions / pending action items.
"""
    review_testplan_prompt_template = """
You are an expert Software Tester at {company} with subject matter expertise in the application and its features.
Given the previously generated test plan:
----------------------------------------
{previous_output}
----------------------------------------
And the user feedback on the test plan:
----------------------------------------
{user_feedback}
----------------------------------------
Refine the test plan based on the feedback. Return the output in similar format as before.
"""

    def __init__(self, llm, company):
        self.company = company
        self.initial_prompt = PromptTemplate(name="Software Tester", template=self.prompt_template, input_variables=["company", "context", "user_stories"])
        self.initial_chain = LLMChain(llm=llm, prompt=self.initial_prompt)
        self.review_testplan_prompt_template = PromptTemplate(name="Software Tester Refine TestPlan", template=self.review_testplan_prompt_template, input_variables=["company", "previous_output", "user_feedback"])
        self.review_testplan_chain = LLMChain(llm=llm, prompt=self.review_testplan_prompt_template)

    def generate_testplan(self, user_stories: str, context: str) -> str:
        return self.initial_chain.run(company=self.company, context=context, user_stories=user_stories)

    def refine(self, previous_output: str, feedback: str) -> str:
        return self.review_testplan_chain.run(company=self.company, previous_output=previous_output, user_feedback=feedback)
