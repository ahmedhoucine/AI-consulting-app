from langchain_core.prompts import ChatPromptTemplate

# Define prompt template
prompt = ChatPromptTemplate.from_template("""
You are a career advisor helping a job seeker improve their profile.

Profile Description:
{profile_description}

Target Job Title:
{target_job_title}

Provide specific, actionable recommendations on how this person can enhance 
their skills, experience, or education to increase their chances of getting hired as a {target_job_title}.
""")

