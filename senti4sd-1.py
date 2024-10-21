import pandas as pd
import re


# Read Answer file 
ans_data = pd.read_excel(r'C:\\Users\\Desktop\\text-mining-project\\data\\Answer.xlsx') 
ans_df = pd.DataFrame(ans_data, columns= ['Id','ParentId(QuestionId)','Body'])

# Read Question file
que_data = pd.read_excel(r'C:\\Users\\Desktop\\text-mining-project\\data\\Question.xlsx') 
que_df = pd.DataFrame(que_data, columns= ['Id','AcceptedAnswerId','Body'])

# Read Comment file
com_data = pd.read_excel(r'C:\\Users\\Desktop\\text-mining-project\\data\\comment.xlsx') 
com_df = pd.DataFrame(com_data, columns= ['Id','PostId(AnswerId)','Text'])



# Remove rows with Nan values
ans_df = ans_df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
que_df = que_df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
com_df = com_df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)



# Separate useful data
ans_df = ans_df.loc[ans_df['ParentId(QuestionId)'].isin(que_df['Id'].values)]
que_df = que_df.loc[que_df['Id'].isin(ans_df["ParentId(QuestionId)"].values)]
com_df = com_df.loc[com_df['PostId(AnswerId)'].isin(ans_df['Id'].values)]
# print("Answers_count: " + str(len(ans_df.index)))
# print("Questions_count: " + str(len(que_df.index)))
# print("Comments_count: " + str(len(com_df.index)))


# save useful data
# que_df.to_excel('C:\\Users\\Ava\\Desktop\\TM-prj\\senti-data\\useful-Questions.xlsx', index=False)
# ans_df.to_excel('C:\\Users\\Ava\\Desktop\\TM-prj\\senti-data\\useful-Answers.xlsx', index=False)
# com_df.to_excel('C:\\Users\\Ava\\Desktop\\TM-prj\\senti-data\\useful-Comments.xlsx', index=False)


# save comments which remains after removing Nan values
# com_df.to_excel('C:\\Users\\Ava\\Desktop\\TM-prj\\senti-data\\comments_removed_Nan.xlsx', index=False)


# remove id and parentid columns for comments file 
comments_without_id = com_df.drop(['Id','PostId(AnswerId)'] ,1)
# comments_without_id.to_excel('C:\\Users\\Ava\\Desktop\\TM-prj\\senti-data\\comments_without_id.xlsx', index=False)



# comments preprocessing and preparing them as senti4sd input
processed_comments_df = pd.DataFrame(columns = ['Text'])
for i in range(len(comments_without_id.index)):
    comment = comments_without_id.iloc[[i]]['Text'].values
    # remove \n
    processed_cm = comment[0].replace("\n" , "")
    # convert to lowercase
    processed_cm = processed_cm.lower()
    # remove digits
    processed_cm = ''.join([w for w in processed_cm if not w.isdigit()])
    # remove usernames
    processed_cm = re.sub('@\w+' , '' ,processed_cm)
    # remove html special entities (e.g. &amp;)
    processed_cm = re.sub('\&\w*;', '', processed_cm)
    # remove hyperlinks
    processed_cm = re.sub('https?://\S*' , '' ,processed_cm)
    # remove html tags
    processed_cm = re.sub('<.*?>' , '' ,processed_cm)
    # remove additional whitespaces
    processed_cm = re.sub(' +', ' ', processed_cm)
    # remove single space remaining at the front of the sentence
    processed_cm = processed_cm.lstrip(' ')
    # replace empty rows with 'emp'
    if processed_cm == '':
        processed_cm = 'emp'
    processed_comments_df = processed_comments_df.append({'Text' : processed_cm}, ignore_index = True)  
# processed_comments_df.to_excel('C:\\Users\\Desktop\\TM-prj\\senti-data\\comments_preprocessed.xlsx', index=False)
   

