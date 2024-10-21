import pandas as pd

# Read useful Answer file 
ans_data = pd.read_excel(r'C:\\Users\\Desktop\\TM-prj\\senti-data\\useful-Answers.xlsx') 
ans_df = pd.DataFrame(ans_data, columns= ['Id','ParentId(QuestionId)','Body'])

# Read useful Question file
que_data = pd.read_excel(r'C:\\Users\\Desktop\\TM-prj\\senti-data\\useful-Questions.xlsx') 
que_df = pd.DataFrame(que_data, columns= ['Id','AcceptedAnswerId','Body'])

# Read Comment file (senti4sd output file)
com_data = pd.read_excel(r'C:\\Users\\Desktop\\TM-prj\\senti-data\\senti4sd_output.xlsx') 
com_df = pd.DataFrame(com_data, columns= ['Id','PostId(AnswerId)','Text','Predicted'])



# merge comments and answers dataframe
merged_com_ans = com_df.merge(ans_df, left_on='PostId(AnswerId)', right_on='Id')
merged_com_ans = merged_com_ans.append({'Id_x' : 0}, ignore_index = True)



# find answer score for each answer by its corresponding comments sense, *Score: [(num_of_pos_cm + num_of_neutral_cm) - num_of_neg_cm]*
answer_score= pd.DataFrame(columns = ['ans_id' , 'answer_score', 'ParentId(QuestionId)'])
pos_num = 0 
neg_num = 0
for i in range(len(merged_com_ans.index)):
    if i!=0:
        if merged_com_ans.iloc[[i]]['PostId(AnswerId)'].values[0] != merged_com_ans.iloc[[i-1]]['PostId(AnswerId)'].values[0]:
            answer_score = answer_score.append({'ans_id' : merged_com_ans.iloc[[i-1]]['PostId(AnswerId)'].values[0] 
            , 'answer_score': pos_num-neg_num , 'ParentId(QuestionId)': merged_com_ans.iloc[[i-1]]['ParentId(QuestionId)'].values[0] }
            , ignore_index = True)
            pos_num = 0 
            neg_num = 0
        
        if merged_com_ans.iloc[[i]]['Predicted'].values[0] == 'positive' or merged_com_ans.iloc[[i]]['Predicted'].values[0] == 'neutral':
            pos_num+=1
        elif merged_com_ans.iloc[[i]]['Predicted'].values[0] == 'negative':
            neg_num +=1
    else:
        if merged_com_ans.iloc[[i]]['Predicted'].values[0] == 'positive' or merged_com_ans.iloc[[i]]['Predicted'].values[0] == 'neutral':
            pos_num+=1
        elif merged_com_ans.iloc[[i]]['Predicted'].values[0] == 'negative':
            neg_num +=1
# answer_score.to_excel('C:\\Users\\Desktop\\TM-prj\\senti-data\\answer_score_by_comment_sense.xlsx', index=False)



# merge amswers and questions dataframe
merged_ans_que = answer_score.merge(que_df, left_on='ParentId(QuestionId)', right_on='Id')


# find best answer for each question by answer score
senti_chosen_answer = pd.DataFrame(columns = ['question_id', 'accepted_answer' , 'senti_chosen_answer'])
max_sense_score = float('-inf')
max_sense_id = 0
for i in range(len(merged_ans_que.index)):
    if i != 0:
        if merged_ans_que.iloc[[i]]['ParentId(QuestionId)'].values[0] != merged_ans_que.iloc[[i-1]]['ParentId(QuestionId)'].values[0]:
            senti_chosen_answer = senti_chosen_answer.append({'question_id' : merged_ans_que.iloc[[i-1]]['ParentId(QuestionId)'].values[0] , 
            'accepted_answer': merged_ans_que.iloc[[i-1]]['AcceptedAnswerId'].values[0] , 'senti_chosen_answer': max_sense_id }, ignore_index = True)
            max_sense_score = float('-inf')
            max_sense_id = 0
                
        if merged_ans_que.iloc[[i]]['answer_score'].values[0] > max_sense_score:
            max_sense_score = merged_ans_que.iloc[[i]]['answer_score'].values[0]
            max_sense_id = merged_ans_que.iloc[[i]]['ans_id'].values[0]
    else:
        if merged_ans_que.iloc[[i]]['answer_score'].values[0] > max_sense_score:
            max_sense_score = merged_ans_que.iloc[[i]]['answer_score'].values[0]
            max_sense_id = merged_ans_que.iloc[[i]]['ans_id'].values[0]
# senti_chosen_answer.to_excel('C:\\Users\\Desktop\\TM-prj\\senti-data\\senti_chosen_answer.xlsx', index=False)


# calculate accuracy by answer score
correct_ans = 0
for i in range(len(senti_chosen_answer.index)):
    if senti_chosen_answer.iloc[[i]]['accepted_answer'].values[0] == senti_chosen_answer.iloc[[i]]['senti_chosen_answer'].values[0]:
        correct_ans += 1
senti_acc = correct_ans/len(senti_chosen_answer.index)

print("\n/*******************************************/\n")
print('Senti4SD-chosen-answer-Accuracy: ' , senti_acc)
print("\n/*******************************************/\n")


    
        
    


        
        




