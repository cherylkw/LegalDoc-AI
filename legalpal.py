import openai
from langchain import LLMChain, PromptTemplate

def generate_legal_document(document_type):
    initial_prompt = f"Generate a {document_type} document."
    critique_prompt = "Critique prompt enter here"
    validate_prompt = "Validate prompt enter here"

    # Initialize the chain with the initial prompt
    chain = LLMChain(
        llm=openai.ChatCompletion.create,
        prompt=PromptTemplate.from_string(initial_prompt),
        max_tokens=500
    )

    # Generate initial draft
    draft = chain.run()

    # Loop for critique and revision
    for _ in range(3):  # Adjust the number of iterations as needed
        # Critique the draft
        critique_chain = LLMChain(
            llm=openai.ChatCompletion.create,
            prompt=PromptTemplate.from_string(critique_prompt),
            max_tokens=500
        )
        critique = critique_chain.run(draft)

        # Revise the draft based on critique
        revise_chain = LLMChain(
            llm=openai.ChatCompletion.create,
            prompt=PromptTemplate.from_string(f"Revise prompt here: {critique}"),
            max_tokens=500
        )
        draft = revise_chain.run(draft)

    # Validate the final document
    validate_chain = LLMChain(
        llm=openai.ChatCompletion.create,
        prompt=PromptTemplate.from_string(validate_prompt),
        max_tokens=500
    )
    final_document = validate_chain.run(draft)

    return final_document

def main():
    document_type = input("Enter the type of legal document you want to generate: ")
    document = generate_legal_document(document_type)
    print("\nGenerated Document:\n")
    print(document)

if __name__ == "__main__":
    main()