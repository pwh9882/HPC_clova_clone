# 목표

LLM을 이용해 입력받은 텍스트 회의록을 요약합니다.

# 사용한 스택

LangChain

# 작동 방법

from llm_summerizer import summarize_by_llm
으로 summarize_by_llm을 사용합니다.

input: text string
output: {"summary": response} 형식의 dict
