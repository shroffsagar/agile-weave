# Agile Weave

Agile Weave is an multi-agent-driven LLM application that transforms your feature requirements into actionable user stories, comprehensive test plans, and automated tests. It leverages AI agents to streamline the software development lifecycle.

## Features

- 🤖 Intelligent Business Analyst Agent
  - Generates well-scoped user stories
  - Creates GHERKIN format acceptance criteria
  - Supports iterative refinement with PM feedback
  
- 🧪 Software Tester Agent
  - Produces comprehensive test plans
  - Covers positive, negative, and corner cases
  - Organizes tests in functional suites
  - Focuses on API-first (shift-left) testing approach

- 🔄 Automation Agent (Work in Progress)
  - Automated test script generation
  - CI/CD pipeline integration
  - Test execution and reporting

- 📚 RAG-enhanced Context
  - Uses retrieval-augmented generation for domain knowledge
  - Supports various data sources including Metabase documentation
  - Vector store-based similarity search

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/agile-weave.git
cd agile-weave
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Project Structure

```
agile-weave/
├── agents/
│   ├── business_analyst.py    # BA agent for story generation
│   └── software_tester.py     # Tester agent for test plans
├── rag/
│   └── utils/
│       └── rag_context.py     # RAG context management
└── fetchers/
    └── metabase/
        └── fetcher.py         # Metabase Data scrapper for demonstration purpose
```

## Usage

### Library Usage

1. Business Analyst Agent
```python
from agents.business_analyst import BusinessAnalystAgent

ba_agent = BusinessAnalystAgent(llm=your_llm, company="YourCompany")
stories = ba_agent.generate_stories(feature_request, context)
refined_stories = ba_agent.refine(stories, feedback)
```

2. Software Tester Agent
```python
from agents.software_tester import SoftwareTesterAgent

test_agent = SoftwareTesterAgent(llm=your_llm, company="YourCompany")
test_plan = test_agent.generate_testplan(user_stories, context)
refined_plan = test_agent.refine(test_plan, feedback)
```

### Running the Application

1. Start the application
```bash
chainlit run app.py
```

2. The application would automatically open in your browser at `http://localhost:8000`

## Demo

https://github.com/yourusername/agile-weave/assets/video/demo.mp4

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License - see the LICENSE file for details.

## Roadmap

- [ ] Implement TestAutomation Agent
- [ ] Implement agent question-asking for vague inputs
- [ ] Add prompt caching
- [ ] Implement Agent Manager Design pattern
- [ ] Streamline prompt templates
- [ ] Improve UX with animations