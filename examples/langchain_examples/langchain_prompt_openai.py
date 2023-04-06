import os

import openai
import time
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain

from gptcache.adapter.langchain_llms import LangChainLLMs
from gptcache.core import Cache
from gptcache.processor.pre import get_prompt
from gptcache.processor.post import nop as postnop

openai.api_key = os.getenv("OPENAI_API_KEY")

before = time.time()


template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

llm = OpenAI()

question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

llm_cache = Cache()
llm_cache.init(
    pre_embedding_func=get_prompt,
    post_process_messages_func=postnop,
)

before = time.time()
cached_llm = LangChainLLMs(llm)
answer = cached_llm(question, cache_obj=llm_cache)
print(answer)
print("Read through Time Spent =", time.time() - before)
before = time.time()

answer = cached_llm(question, cache_obj=llm_cache)
print("Cache Hit Time Spent =", time.time() - before)
before = time.time()

before = time.time()
answer = cached_llm("What is your hobby", cache_obj=llm_cache)
print("Read through Time Spent =", time.time() - before)
before = time.time()

question = "What is the winner Super Bowl in the year Justin Bieber was born?"
answer = cached_llm(question, cache_obj=llm_cache)
print("Cache Hit Time Spent =", time.time() - before)
before = time.time()
