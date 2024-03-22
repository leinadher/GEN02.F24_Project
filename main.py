from dotenv import load_dotenv
import os
import pandas as pd
from llama_index.core.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str, context        # our prompts script
from note_engine import note_engine                             # our note_engine script
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from pdf import module_descriptions_engine
import openai

openai.api_key = "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"

# Loading OpenAI API Key from .env
load_dotenv()

## Structured data: csv as a source of data
universities_path = os.path.join("data", "cwurData.csv")
universities_df = pd.read_csv(universities_path)

# Setting up a query engine
# verbose = True provides some information about the "thinking process"
# We are using the PandasQueryEngine from llama_index.core to query through the pandas data frame
universities_query_engine = PandasQueryEngine(df=universities_df,
                                              verbose=True,
                                              instruction_str=instruction_str)
universities_query_engine.update_prompts({"pandas_prompt": new_prompt})

# We test with a query prompt
# universities_query_engine.query("What is the national_rank of Harvard University?")

## TOOLS TO BE USED
# Additional tools can be added (sources of data)

tools = [
    note_engine,
    # 1) CSV QueryEngineTool
    QueryEngineTool(query_engine=universities_query_engine, metadata=ToolMetadata(
        name="universities_data",
        description="this gives information of the university data and rankings"
        )
    ),
    # 2) PDF QueryEngineTool
    QueryEngineTool(query_engine=module_descriptions_engine, metadata=ToolMetadata(
        name="module_descriptions_data",
        description="this gives information about the module descriptions of MSc Information and Data Science"
        )
    )
]

# Set up the LLM and let the agent choose the right tool
llm = OpenAI(model = "gpt-3.5-turbo-0613")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

## Set up the open while loop which allows for user inputs
# Notice the walrus operator
while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    result = agent.query(prompt)
    print(result)