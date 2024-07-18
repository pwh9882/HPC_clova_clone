from llm_summerizer import summarize_by_llm
import asyncio


def test_summarize_by_llm():
    answer = asyncio.run(summarize_by_llm(
        text="Hello, my name is John Doe. I am a software engineer.", language="korean"))
    print(answer)


if __name__ == "__main__":
    test_summarize_by_llm()
