# data_processor.py
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_deepseek import ChatDeepSeek
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
import os


class DataInfo(BaseModel):
    Summary : str = Field(description="Summary of the dataset", required=True)
    important_cols : List[str] = Field(description="Important columns of the dataset according to you", required=True)


class   DataProcessor:
    def __init__(self):
        # self.llm = ChatGoogleGenerativeAI(
        #     model="gemini-1.5-pro",
        #     google_api_key=os.environ["GOOGLE_API_KEY"]
        # )
        
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            #model="llama-3.1-405b-reasoning",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=os.environ["GROQ_API_KEY"]
            # other params...
        )
    
    def generate_summary(self, df : pd.DataFrame) -> DataInfo:
        """Generate data summary using LLM"""
        prompt = """You are a data analysis expert.
         Analyze this dataset and provide a comprehensive and intelligent summary **without relying on specific rows from the sample data**. Focus on general structural and statistical characteristics of the dataset.

### Dataset Overview:
- **Shape**: {shape}
- **Columns**: {columns}
- **Column Data Types**: {dtypes}
- **Missing Values Count**: {missing}
- **Descriptive Statistics**:
{desc}

### Instructions:
Please analyze the dataset holistically and provide the following:
1. **Overview** of the dataset structure and content.
2. **Key statistics**, such as numerical distributions, missing data, and categorical spread.
3. **Important patterns**, potential quality issues, or preprocessing considerations.
4. **Columns likely to be most important** for downstream tasks like model training or visualization.
5. Present the result in the following **valid JSON format**:

```json
{{{{ 
  "Summary": "Markdown-formatted summary of the dataset",
  "important_cols": ["list", "of", "important", "columns"]
}}}}
```
note - provide the summary in a markdown format, intelligent using points and highlights whereever necessary.
"""
        prompt_template =  ChatPromptTemplate.from_template(prompt)
        
        parser = PydanticOutputParser(pydantic_object=DataInfo)
        chain =prompt_template | self.llm | parser
        print(f"before response")
        response = chain.invoke({
    "shape": df.shape,
    "columns": df.columns.tolist(),
    "dtypes": df.dtypes.to_dict(),
    "missing": df.isnull().sum().to_dict(),
    "desc": df.describe(include='all').transpose()
})
        print(f"response from summary llm: {response}")
        response = response.dict()
        response["shape"] = str(df.shape)
        return response