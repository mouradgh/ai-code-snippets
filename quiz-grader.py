from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser

# define chatbot
chat_model = ChatOpenAI(openai_api_key="you API key", temperature=0)

# define prompt template
prompt_template_text = """You are a high school history teacher grading homework assignments. \
Based on the homework question indicated by “**Q:**” and the correct answer indicated by “**A:**”, your task is to determine whether the student's answer is correct. \
Grading is binary; therefore, student answers can be correct or wrong. \
Simple misspellings are okay.

**Q:** {question}
**A:** {correct_answer}

**Student's Answer:** {student_answer}
"""

prompt = PromptTemplate(input_variables=["question", "correct_answer", "student_answer"], template = prompt_template_text)

# define chain
chain = LLMChain(
    llm=chat_model,
    prompt=prompt,
)

# define inputs
question = "Who was the 35th president of the United States of America?"
correct_answer = "John F. Kennedy"
student_answer =  "JFK"

# run chain
chain.run({'question':question, 'correct_answer':correct_answer, 'student_answer':student_answer})


# run chain in for loop
student_answer_list = ["John F. Kennedy", "JFK", "FDR", "John F. Kenedy", "John Kennedy", "Jack Kennedy", "Jacqueline Kennedy", "Robert F. Kenedy"]

for student_answer in student_answer_list:
    print(student_answer + " - " + str(chain.run({'question':question, 'correct_answer':correct_answer, 'student_answer':student_answer})))
    print('\n')

# define output parser
class GradeOutputParser(BaseOutputParser):
    """Determine whether grade was correct or wrong"""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return "wrong" not in text.lower()

# update chain
chain = LLMChain(
    llm=chat_model,
    prompt=prompt,
    output_parser=GradeOutputParser()
)

# grade student answers
for student_answer in student_answer_list:
    print(student_answer + " - " + str(chain.run({'question':question, 'correct_answer':correct_answer, 'student_answer':student_answer})))