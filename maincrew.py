# Import Reqiured Library
import os
import streamlit as st
from crewai import Agent,Task,Crew,Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from crewai_tools import SerperDevTool
# # LLM Monitering
os.environ['LANGCHAIN_TRACING_V2']='true'
os.environ['LANGCHAIN_API_KEY']='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'
os.environ['LANGCHAIN_PROJECT']='Website Content AI Agents'


# Creating Web Page Header
st.subheader('**Multi AI Agents Website Content Generator**')

# Getting Task from Web
with st.form(key='Query',clear_on_submit=True):
    website_content=st.text_input(label='**What Website Content Would you Like me to come up with Today?**')
    llm_model_name=st.selectbox(label='**Select LLM Model:**',
                              options=['Gemini Model','Lamma Model'],index=None)
    submit_button = st.form_submit_button('Submit.')
    if submit_button:
        st.info('Input Details...')
        st.markdown(f'Website Content Name: {website_content} ...')
        st.markdown(f'LLM Model Name: {llm_model_name} ...')

# Creating LLM Variable
def model_selection(value):
    if value == 'Gemini Model':
        os.environ['GOOGLE_API_KEY']='AIzaSyD5ggkVEWVzFE3NaFa73a0MHuJPmkT3U8M'
        llm_model = ChatGoogleGenerativeAI(model='gemini-1.5-flash',api_key=os.getenv('GOOGLE_API_KEY'))
        return llm_model
    else:
        os.environ['GROQ_API_KEY']='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'
        llm_model = ChatGroq(model='llama3-8b-8192',api_key=os.getenv('GROQ_API_KEY'))
        return llm_model

LLM_Model=model_selection(llm_model_name)

os.environ['GOOGLE_API_KEY']='AIzaSyD5ggkVEWVzFE3NaFa73a0MHuJPmkT3U8M'
llm_model = ChatGoogleGenerativeAI(model='gemini-1.5-flash',api_key=os.getenv('GOOGLE_API_KEY'))

# Initialize WebSearch Tool
os.environ['SERPER_API_KEY']='5e91bacd42a33cdf4299197ce6d7e49aaca23310'
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()

# Agents

Content_Planner_Agent = Agent(
    role='''The Content Planner Agent is responsible for strategizing and organizing 
    the structure of website {website_content} content to ensure it aligns with the educational goals 
    and audience needs of AIMentor Lab.''',
    goal='''To develop a comprehensive and strategic {website_content} content plan that outlines the 
    key sections of the website, including educational modules, course offerings, 
    and additional resources.''',
    backstory='''With a background in educational content strategy and digital marketing, 
    this agent excels in understanding the educational landscape and identifying key topics 
    that will resonate with learners interested in generative AI. It draws on experience with 
    curriculum design and user engagement to create a well-structured content roadmap''',
    memory=True,
    verbose=True,
    tools=[search_tool],
    llm=LLM_Model
)
Subject_Matter_Expert_Agent = Agent(
    role='''The Subject Matter Expert Agent provides in-depth knowledge and expertise on 
    generative AI topics to ensure that the website {website_content} content is accurate, relevant, and insightful.''',
    goal='''To generate detailed and authoritative content that covers various aspects of 
    generative AI, including concepts, applications, and case studies''',
    backstory='''An authority in the field of generative AI with extensive experience 
    in both research and practical applications. This agent has a deep understanding of 
    AI technologies and can provide comprehensive explanations and insights that cater 
    to learners at different levels''',
    memory=True,
    verbose=True,
    tools=[search_tool],
    llm=LLM_Model
)
Copy_Editor_Agent = Agent(
    role='''The Copy Editor Agent focuses on refining and enhancing the written on {website_content} content 
    to ensure clarity, coherence, and consistency across the website.''',
    goal=''' To deliver polished and professional content that is free of grammatical errors, 
    typos, and inconsistencies, making it easy for users to understand and engage with.''',
    backstory='''A seasoned editor with expertise in educational and technical writing. 
    This agent is skilled in maintaining a consistent tone and style while ensuring that 
    complex information is presented clearly and effectively.''',
    memory=True,
    verbose=True,
    tools=[search_tool],
    llm=LLM_Model
)
SEO_Specialist_Agent = Agent(
    role=''' The SEO Specialist Agent optimizes the website content to improve 
    its visibility on search engines and attract relevant traffic''',
    goal='''To enhance the {website_content} content with strategic keywords, meta descriptions, 
    and other SEO best practices, ensuring that AIMentor Lab’s website ranks well 
    in search results and reaches its target audience''',
    backstory='''An SEO expert with a strong background in digital marketing and 
    search engine optimization. This agent understands the nuances of search algorithms 
    and has experience in boosting online visibility for educational and technology-related content.''',
    memory=True,
    verbose=True,
    tools=[search_tool],
    llm=LLM_Model
)
Visual_Content_Generator_Agent = Agent(
    role='''The Visual {website_content} Content Generator Agent creates engaging and informative 
    visual content to complement the written material on the website.''',
    goal=''' To design and produce high-quality visuals such as infographics, 
    diagrams, and illustrations that enhance the educational experience and 
    make complex AI concepts more accessible''',
    backstory='''A skilled graphic designer with a focus on educational visuals. 
    This agent combines artistic flair with an understanding of educational content 
    to produce visuals that support and enrich the learning experience.''',
    memory=True,
    verbose=True,
    tools=[search_tool],
    llm=llm_model
)
Final_Content_Assembler_Agent = Agent(
    role='''The Final {website_content} Content Assembler Agent integrates and formats all content 
    elements into a cohesive and well-structured final product ready for publication 
    on the website''',
    goal=''' To ensure that all components, including text, visuals, and interactive 
    elements, are seamlessly combined into a polished and user-friendly final draft.''',
    backstory='''An experienced content producer with expertise in web design and 
    content management. This agent excels at creating a visually appealing and functional 
    layout that enhances the overall user experience on the website.''',
    memory=True,
    verbose=True,
    tools=[search_tool],
    llm=LLM_Model
)

# Define Task
Content_Planner_Task = Task(
    description='''Develop a detailed content plan for the AIMentor Lab website, 
    including the identification of key sections (e.g., Home, Courses, Blog, About Us) 
    and topics to be covered. The plan should align with the company’s educational goals 
    and audience needs.''',
    expected_output='''A comprehensive content plan document that includes: 
    A list of main website sections and sub-sections. 
    Topic ideas and content themes for each section. 
    A suggested content schedule or timeline for publication.''',
    agent=Content_Planner_Agent
)
Subject_Matter_Expert_Task = Task(
    description='''Create detailed content for the topics outlined in the content plan. 
    This includes writing educational articles, course descriptions, and explanatory content 
    related to generative AI.''',
    expected_output='''Well-researched and authoritative content drafts that include: 
    In-depth articles or course modules on generative AI topics. 
    Clear explanations of complex concepts with examples and case studies. 
    Any necessary references or citations to support the content.''',
    agent=Subject_Matter_Expert_Agent
)
Copy_Editor_Task = Task(
    description='''Review and edit the content produced by the Subject Matter Expert Agent. 
    Ensure the text is clear, engaging, and free of grammatical errors, typos, and inconsistencies.''',
    expected_output='''Edited content that is: 
    Grammatically correct and free of spelling mistakes. 
    Consistent in tone and style with a focus on clarity and readability. 
    Structured for easy navigation and understanding.''',
    agent=Copy_Editor_Agent
)
SEO_Specialist_Task = Task(
    description='''Optimize the website content for search engines by incorporating 
    relevant keywords, optimizing meta descriptions, and applying SEO best practices''',
    expected_output='''SEO-optimized content that includes: 
    Strategic use of keywords and phrases. 
    Optimized meta titles and descriptions for each page. 
    Recommendations for improving internal and external linking.''',
    agent=SEO_Specialist_Agent
)
Visual_Content_Generator_Task = Task(
    description='''Design and produce visual content that complements the written material 
    on the website. This includes creating infographics, diagrams, and illustrations that aid 
    in understanding generative AI concepts.''',
    expected_output=''' High-quality visual assets that include: 
    Infographics that summarize key information or concepts. 
    Diagrams or charts that illustrate complex ideas. 
    Illustrations that enhance and support the text.''',
    agent=Visual_Content_Generator_Agent
)
Final_Content_Assembler_Task = Task(
    description=''' Assemble all the content elements (text, visuals, and interactive elements) 
    into a cohesive final draft. Ensure that the layout is user-friendly and visually appealing.''',
    expected_output='''A fully integrated and formatted web page or content section that includes: 
    Combined text and visual content in a structured layout. 
    Proper formatting and design elements for a polished look. 
    A final draft that is ready for publication on the AIMentor Lab website.''',
    agent=Final_Content_Assembler_Agent
)

# Creating Crew
crew = Crew(
    agents=[Content_Planner_Agent,Subject_Matter_Expert_Agent,
            Copy_Editor_Agent,SEO_Specialist_Agent,
            Visual_Content_Generator_Agent,Final_Content_Assembler_Agent],
    tasks=[Content_Planner_Task,Subject_Matter_Expert_Task,
           Copy_Editor_Task,SEO_Specialist_Task,
           Visual_Content_Generator_Task,Final_Content_Assembler_Task],
    verbose=True,
    process=Process.sequential,
    manager_llm=LLM_Model
)

inputs={
    'website_content':website_content
}

if st.button('Generate'):
    with st.spinner('Generate Response...'):
        result=crew.kickoff(inputs=inputs)
        res=str(result)
        st.info('Here is Response')
        st.markdown(result)
        st.download_button(label='Download Text File',
                           file_name=f'{website_content}_website_content.txt',data=res)
