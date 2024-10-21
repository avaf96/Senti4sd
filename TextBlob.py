import pandas as pd
from textblob import TextBlob
import re


# Read Answer file and convert it to dataframe
ans_data = pd.read_excel (r'C:\\Users\\Desktop\\Stack_Data\\Answer.xlsx') 
ans_df = pd.DataFrame(ans_data, columns= ['Id','ParentId(QuestionId)','Body'])

# Read Question file and convert it to dataframe
que_data = pd.read_excel (r'C:\\Users\\Desktop\\Stack_Data\\Question.xlsx') 
que_df = pd.DataFrame(que_data, columns= ['Id','AcceptedAnswerId','Body'])

# Read Comment file and convert it to dataframe
com_data = pd.read_excel (r'C:\\Users\\Desktop\\Stack_Data\\comment.xlsx') 
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



# comments preprocessing and find textblob sentiment polarity for each comment
comment_sense = pd.DataFrame(columns = ['Id', 'PostId(AnswerId)' , 'cm_sense'])
for i in range(len(com_df.index)):
    comment = com_df.iloc[[i]]['Text'].values
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
    # calculate sentiment score 
    cm_sense = TextBlob(processed_cm)
    cm_sense = cm_sense.sentiment.polarity
    comment_sense = comment_sense.append({'Id' : com_df.iloc[[i]]['Id'].values[0] , 
        'PostId(AnswerId)': com_df.iloc[[i]]['PostId(AnswerId)'].values[0] , 'cm_sense':cm_sense  }, ignore_index = True)
# comment_sense.to_excel('C:\\Users\\Desktop\\TM-prj\\txtblob-data\\comments_with_sense.xlsx', index=False)



# merge comments and answers dataframe
merged_com_ans = comment_sense.merge(ans_df, left_on='PostId(AnswerId)', right_on='Id')
merged_com_ans = merged_com_ans.append({'Id_x' : 0}, ignore_index = True)



# find answer score for each answer by its corresponding comments sense,
# *Score1: [(num_of_pos_cm + num_of_neutral_cm) - num_of_neg_cm]*, *Score2: sum_of_cm_polarity*
answer_score = pd.DataFrame(columns = ['ans_id' , 'ans_sense_by_num', 'ans_sense_by_sum' , 'ParentId(QuestionId)'])
pos_num = 0 
neg_num = 0
ans_sns = 0
for i in range(len(merged_com_ans.index)):
    if i!=0:
        if merged_com_ans.iloc[[i]]['PostId(AnswerId)'].values[0] != merged_com_ans.iloc[[i-1]]['PostId(AnswerId)'].values[0]:
            answer_score = answer_score.append({'ans_id' : merged_com_ans.iloc[[i-1]]['PostId(AnswerId)'].values[0] ,
             'ans_sense_by_num': pos_num-neg_num ,'ans_sense_by_sum': ans_sns,'ParentId(QuestionId)': merged_com_ans.iloc[[i-1]]['ParentId(QuestionId)'].values[0] }
            , ignore_index = True)
            pos_num = 0 
            neg_num = 0
            ans_sns = 0

        ans_sns += merged_com_ans.iloc[[i]]['cm_sense'].values[0]
        if merged_com_ans.iloc[[i]]['cm_sense'].values[0] >= 0:
            pos_num+=1
        elif merged_com_ans.iloc[[i]]['cm_sense'].values[0] < 0:
            neg_num +=1
    else:
        ans_sns += merged_com_ans.iloc[[i]]['cm_sense'].values[0]
        if merged_com_ans.iloc[[i]]['cm_sense'].values[0] >= 0:
            pos_num+=1
        elif merged_com_ans.iloc[[i]]['cm_sense'].values[0] < 0:
            neg_num +=1
# answer_score.to_excel('C:\\Users\\Desktop\\TM-prj\\txtblob-data\\answer_score.xlsx', index=False)


# merge amswers and questions dataframe
merged_ans_que = answer_score.merge(que_df, left_on='ParentId(QuestionId)', right_on='Id')


# find best answer for each question by answer score1 and answer score2
textblob_answer_by_num = pd.DataFrame(columns = ['question_id', 'accepted_answer' , 'txtblob_answer'])
textblob_answer_by_sum = pd.DataFrame(columns = ['question_id', 'accepted_answer' , 'txtblob_answer'])
max_sense_score_num = float('-inf')
max_sense_score_sum = float('-inf')
max_sense_id_num = 0
max_sense_id_sum = 0
for i in range(len(merged_ans_que.index)):
    if i != 0:
        if merged_ans_que.iloc[[i]]['ParentId(QuestionId)'].values[0] != merged_ans_que.iloc[[i-1]]['ParentId(QuestionId)'].values[0]:
            textblob_answer_by_num = textblob_answer_by_num.append({'question_id' : merged_ans_que.iloc[[i-1]]['ParentId(QuestionId)'].values[0] , 
            'accepted_answer': merged_ans_que.iloc[[i-1]]['AcceptedAnswerId'].values[0] ,
             'txtblob_answer': max_sense_id_num }, ignore_index = True)

            textblob_answer_by_sum = textblob_answer_by_sum.append({'question_id' : merged_ans_que.iloc[[i-1]]['ParentId(QuestionId)'].values[0] , 
            'accepted_answer': merged_ans_que.iloc[[i-1]]['AcceptedAnswerId'].values[0] ,
             'txtblob_answer': max_sense_id_sum }, ignore_index = True)

            max_sense_score_num = float('-inf')
            max_sense_score_sum = float('-inf')
            max_sense_id_num = 0
            max_sense_id_sum = 0
                
        if merged_ans_que.iloc[[i]]['ans_sense_by_num'].values[0] > max_sense_score_num:
            max_sense_score_num = merged_ans_que.iloc[[i]]['ans_sense_by_num'].values[0]
            max_sense_id_num = merged_ans_que.iloc[[i]]['ans_id'].values[0]

        if merged_ans_que.iloc[[i]]['ans_sense_by_sum'].values[0] > max_sense_score_sum:
            max_sense_score_sum = merged_ans_que.iloc[[i]]['ans_sense_by_sum'].values[0]
            max_sense_id_sum = merged_ans_que.iloc[[i]]['ans_id'].values[0]
    else:
        if merged_ans_que.iloc[[i]]['ans_sense_by_num'].values[0] > max_sense_score_num:
            max_sense_score_num = merged_ans_que.iloc[[i]]['ans_sense_by_num'].values[0]
            max_sense_id_num = merged_ans_que.iloc[[i]]['ans_id'].values[0]

        if merged_ans_que.iloc[[i]]['ans_sense_by_sum'].values[0] > max_sense_score_sum:
            max_sense_score_sum = merged_ans_que.iloc[[i]]['ans_sense_by_sum'].values[0]
            max_sense_id_sum = merged_ans_que.iloc[[i]]['ans_id'].values[0]
# textblob_answer_by_num.to_excel('C:\\Users\\Desktop\\TM-prj\\txtblob-data\\textblob_answer_by_num.xlsx', index=False)
# textblob_answer_by_sum.to_excel('C:\\Users\\Desktop\\TM-prj\\txtblob-data\\textblob_answer_by_sum.xlsx', index=False)


# calculate accuracy by answer score1
correct_ans_num = 0
for i in range(len(textblob_answer_by_num.index)):
    if textblob_answer_by_num.iloc[[i]]['accepted_answer'].values[0] == textblob_answer_by_num.iloc[[i]]['txtblob_answer'].values[0]:
        correct_ans_num += 1
txtblob_acc_num = correct_ans_num/len(textblob_answer_by_num.index)

# calculate accuracy by answer score2
correct_ans_sum = 0
for i in range(len(textblob_answer_by_sum.index)):
    if textblob_answer_by_sum.iloc[[i]]['accepted_answer'].values[0] == textblob_answer_by_sum.iloc[[i]]['txtblob_answer'].values[0]:
        correct_ans_sum += 1
txtblob_acc_sum = correct_ans_sum/len(textblob_answer_by_sum.index)


print("\n/*******************************************/\n")
print('TextBlob-Accuracy-by-Score1(num) : ' , txtblob_acc_num)
print("\n/-------------------------------------------/\n")
print('TextBlob-Accuracy-by-Score2(sum) : ' , txtblob_acc_sum)
print("\n/*******************************************/\n")












