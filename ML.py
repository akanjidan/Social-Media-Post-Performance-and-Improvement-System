
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
client = OpenAI(api_key = '') # To run this code, create an api key for this code.....

def getresult(post, metric):
    if metric=='tone':
        prompt = f"""from the following choices: Casual/Conversational , Informative/Educational, Inspirational/Motivational  What is the {metric} used in this Facebook Post {post} and associate a score in 1 to 10, return the tone and score only in this format: tone:score"""
    else:
        prompt = f""" on a score in 1 to 10 for the following metric {metric}  for the following post {post}, return the score and only the score don't include anything else"""

  

  
    # Define model versions in the order they should be tried
    model_versions = [
        "gpt-4-turbo-2",  # Assuming "gpt-4-turbo-2" is a placeholder for the actual model identifier
        "gpt-4-turbo",
        "gpt-4-base",  # Assuming "gpt-4-base" is a placeholder for the actual model identifier
        "gpt-3.5"
    ]

    for model_version in model_versions:
        try:
            # Determine the appropriate model based on the current iteration
            if model_version == "gpt-4-turbo-2":
                model = "gpt-4-0125-preview"  # Placeholder
            elif model_version == "gpt-4-turbo":
                model = "gpt-4-1106-preview"  # Adjusted for the example provided; replace as needed
            elif model_version == "gpt-4-base":
                model = "gpt-4"  # Placeholder for GPT-4 Base model identifier
            else:
                model = "gpt-3.5-turbo-0125"  # Placeholder for GPT-3.5 model identifier; replace as needed

            # Attempt to use the selected model for translation
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"{prompt}"},
                    {"role": "user", "content": post}
                ]
            )
           
            total_tokens=completion.usage.total_tokens
            result = completion.choices[0].message.content
            if metric=='tone':
                return ("success", result.split(":")[0],result.split(":")[1],total_tokens)  # Success
            else:
                return ("success", result,total_tokens)
        except Exception as exc:
            if "rate limit" in str(exc).lower():
                continue  # Try the next model in the list
            else:
                raise  # Raise the exception if it's not a rate limit issue
    # If all models hit their rate limit, requeue the request
    return ("requeue", None)
def getscore(post):
    L=['tone','Message Clarity','Narrative','effective use of tagging','Use of Controversial Topics','How well Call to actions are implemented','how well the post is engaging']
    H=[]
    for i in L:
                P=[]
                P.append(i)
                
                if i=='tone':
                    tst1=int(getresult(post, i)[2])
                    tst2=int(getresult(post, i)[2])
                    tst3=int(getresult(post, i)[2])
                    sc=0
                    sc=(tst1+tst2+tst3)/3
                    P.append(round(sc,2))
                else:
                    tst1=int(getresult(post, i)[1])
                    tst2=int(getresult(post, i)[1])
                    tst3=int(getresult(post, i)[1])
                    sc=0
                    sc=(tst1+tst2+tst3)/3
                    P.append(round(sc,2))
                H.append(P)      
    return(H)
#Generate suggestions
def suggestion(post):
    prompt=promptfor_suggestions(ColorMetricsLessThanFive('after.xlsx'))+' include examples as well as reformulation related to the original post whihc is '+post
     # Define model versions in the order they should be tried
    model_versions = [
        "gpt-4-turbo-2",  # Assuming "gpt-4-turbo-2" is a placeholder for the actual model identifier
        "gpt-4-turbo",
        "gpt-4-base",  # Assuming "gpt-4-base" is a placeholder for the actual model identifier
        "gpt-3.5"
    ]

    for model_version in model_versions:
        try:
            # Determine the appropriate model based on the current iteration
            if model_version == "gpt-4-turbo-2":
                model = "gpt-4-0125-preview"  # Placeholder
            elif model_version == "gpt-4-turbo":
                model = "gpt-4-1106-preview"  # Adjusted for the example provided; replace as needed
            elif model_version == "gpt-4-base":
                model = "gpt-4"  # Placeholder for GPT-4 Base model identifier
            else:
                model = "gpt-3.5-turbo-0125"  # Placeholder for GPT-3.5 model identifier; replace as needed

            # Attempt to use the selected model for translation
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"{prompt}"},
                    {"role": "user", "content": post}
                ]
            )
           
            total_tokens=completion.usage.total_tokens
            result = completion.choices[0].message.content
            return (result)
        except Exception as exc:
            if "rate limit" in str(exc).lower():
                continue  # Try the next model in the list
            else:
                raise  # Raise the exception if it's not a rate limit issue
    # If all models hit their rate limit, requeue the request
    return ("requeue", None)
def promptfor_suggestions(L):
    prompt = f""" You'll be provided a list of metrics as well as their coresponding score on a scale of 10,  your goal is to provide suggestions while emphasizing points where'the score is weak, the metrics are """
    for i in L:
        prompt+= i[0] +' '+i[1]
    return(prompt)
def ColorMetricsLessThanFive(OutputPath):
    # Load the Excel file
    df = pd.read_excel(OutputPath)
    post_ids = df['post_id'].tolist()

    # List of columns to check
    columns_to_check = ['Tone', 'Message', 'Narrative', 'Hashtag_Effectiveness', 'Controversial_Topics', 'Call_To_Action', 'Engagement']

    # Initialize the list to store the results
    results = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Initialize a list to store the values less than 5 for the current row
        row_result = []
        
        # Check each specified column
        for col in columns_to_check:
            if row[col] < 5:
                row_result.append(f"{col}: {row[col]}")
        
        # Add the result to the list (empty or not)
        results.append(row_result)


    return results

print(suggestion("Enjoying the sunset #sunset #nature"))
