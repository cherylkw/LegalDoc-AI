from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.agents import Tool, initialize_agent, AgentType

# Step 1: Initialize the LLM
llm = OpenAI(model="text-davinci-003", temperature=0.7)

# Step 2: Define Prompts for Each Step
draft_prompt = PromptTemplate(
    input_variables=["topic"],
    template="Draft a legal document about {topic}."
)

critique_prompt = PromptTemplate(
    input_variables=["draft"],
    template="Critique the following draft for clarity, completeness, and errors:\n\n{draft}"
)

revise_prompt = PromptTemplate(
    input_variables=["draft", "critique"],
    template=(
        "Revise the draft based on the critique below to improve clarity and accuracy.\n"
        "Draft:\n{draft}\n\nCritique:\n{critique}"
    )
)

validate_prompt = PromptTemplate(
    input_variables=["revised_draft"],
    template=(
        "Validate the following draft against legal standards and highlight any remaining issues:\n\n{revised_draft}"
    )
)

# Step 3: Create LLMChains for Each Task
draft_chain = LLMChain(llm=llm, prompt=draft_prompt)
critique_chain = LLMChain(llm=llm, prompt=critique_prompt)
revise_chain = LLMChain(llm=llm, prompt=revise_prompt)
validate_chain = LLMChain(llm=llm, prompt=validate_prompt)

# Step 4: Define Tools Using LLMChains
draft_tool = Tool(
    name="Drafting Agent",
    func=draft_chain.run,
    description="Drafts a legal document based on the topic provided."
)

critique_tool = Tool(
    name="Critique Agent",
    func=critique_chain.run,
    description="Critiques the draft for clarity, completeness, and errors."
)

revise_tool = Tool(
    name="Revision Agent",
    func=revise_chain.run,
    description="Revises the draft based on the critique provided."
)

validate_tool = Tool(
    name="Validation Agent",
    func=validate_chain.run,
    description="Validates the final draft against legal standards."
)

# Step 5: Initialize the Agent Orchestrator
tools = [draft_tool, critique_tool, revise_tool, validate_tool]

agent = initialize_agent(
    tools=tools,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# Step 6: Execute the Workflow
if __name__ == "__main__":
    topic = "software licensing agreement"
    
    # Drafting
    draft = draft_tool.func({"topic": topic})
    print("Draft:\n", draft)
    
    # Critiquing
    critique = critique_tool.func({"draft": draft})
    print("\nCritique:\n", critique)
    
    # Revising
    revised_draft = revise_tool.func({"draft": draft, "critique": critique})
    print("\nRevised Draft:\n", revised_draft)
    
    # Validating
    validation = validate_tool.func({"revised_draft": revised_draft})
    print("\nValidation:\n", validation)
