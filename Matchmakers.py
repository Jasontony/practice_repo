
# coding: utf-8

# In[215]:

import numpy, pandas
from operator import itemgetter
class Makematches:
    """This class generates matches and a match percentage based on similarly answered questions of two groups. The answers 
    to the questions have to be binary such that if two users have the same answer then their inputs are equal to each other"""

    def __init__(self, dframeA, dframeB, dframeC, dframeD, number_preferred, multiple_matches):
        self.dframeA= dframeA
        self.dframeB= dframeB
        self.dframeC= dframeC
        self.dframeD= dframeD
        self.number_preferred=number_preferred
        self.multiple_matches=multiple_matches
        self.labels=[]
        self.df_match_percentage=pandas.DataFrame(data=numpy.zeros((0,len(self.labels))), columns=self.labels)
        self.df_sorted_matches_f=pandas.DataFrame(data=numpy.zeros((0,len(self.labels))), columns=self.labels)

    def points(self): 
        number_of_question= len(self.dframeA.columns)-1 #how many questions are there excluding the identifier(names)
        match_percentage=[]
        self.labels.append('User1')
        self.labels.append('User2')
        self.labels.append('Match_Percentage')
        self.labels= self.labels + list(self.dframeB.columns.values)[1:]
        for user1_number in range(len(self.dframeA)): #number of user1's where user1_number is each user1's number
            for user2_number in range(len(self.dframeB)): #number of user2' where user2_number is each user2's number
                user1 = str(self.dframeA.iloc[user1_number][0]) #each user1
                user2 = str(self.dframeB.iloc[user2_number][0]) #each user2
                points_awarded = 0 
                points_possible = 0
                percentage = 0
                question_matches=[]
                question_matches_new=[]
                for question_number in range(number_of_question): 
                    user1_preference = self.dframeA.iloc[user1_number][question_number + 1]
                    user2_preference = self.dframeB.iloc[user2_number][question_number + 1]
                    if user1_preference == user2_preference:
                        points_awarded += self.dframeC.iloc[question_number][1] #assigning points based on if they match preferences
                        question_match = 1
                        question_matches.append(question_match)
                    else: 
                        points_awarded += 0.0
                        question_match = 0
                        question_matches.append(question_match)
                    points_possible += self.dframeC.iloc[question_number][1] 
                percentage = ((points_awarded)/points_possible)*100 # match_percentage 
                question_matches_new.append(user1)
                question_matches_new.append(user2)
                question_matches_new.append(percentage)
                for answer_match in question_matches:
                    question_matches_new.append(answer_match)
                match_percentage.append(question_matches_new)
        df_match_percentage = pandas.DataFrame(match_percentage, columns=self.labels) #convert match_percentage into a dataframe
        self.df_match_percentage=df_match_percentage
        return df_match_percentage
    
    def new_matches(self):
        match_percentage_new=[]
        match_percentage=[]
        for user1_number in range(len(self.df_match_percentage)):  
            count_already_matched=0
            for user1_number_prev_match in range(len(self.dframeD)):
                if self.df_match_percentage.iloc[user1_number][0]==self.dframeD.iloc[user1_number_prev_match][0]:
                    if self.df_match_percentage.iloc[user1_number][1]==self.dframeD.iloc[user1_number_prev_match][1]:
                        count_already_matched+=1             
            if count_already_matched<1:
                for label in range(len(self.labels)):
                    match_percentage.append(self.df_match_percentage.iloc[user1_number][label])
                match_percentage_new.append(match_percentage)
                match_percentage=[]
                
            else:
                match_percentage.append(self.df_match_percentage.iloc[user1_number][0])
                match_percentage.append(self.df_match_percentage.iloc[user1_number][1])
                match_percentage.append(-1)
                for other_label in range(3, len(self.labels)):
                    match_percentage.append(self.df_match_percentage.iloc[user1_number][other_label])
                match_percentage_new.append(match_percentage)
                match_percentage=[]
            
        df_match_percentage = pandas.DataFrame(match_percentage_new, columns=self.labels) 
        self.df_match_percentage=df_match_percentage
        return df_match_percentage
                             
    
    def secondary_matches(self): 
        unsorted_matches=[]
        sorted_matches_new=[]
        secondary_matches=[]
        sorted_matches_new_f=[]
        sorted_matches_f=[]
        for user1_number in range(0, len(self.df_match_percentage), len(self.dframeB)): #looping through each possible user1 match with a user2 and ranking them based on match percentage the step included is the number of user2's
            unsorted_matches_new=[]
            if user1_number < len(self.df_match_percentage):
                for user2_number in range(len(self.dframeB)):
                    for label in range(len(self.labels)):
                        unsorted_matches.append(self.df_match_percentage.iloc[user2_number+user1_number][label])
                    unsorted_matches_new.append(unsorted_matches)
                    unsorted_matches=[]
                    sorted_matches=sorted(unsorted_matches_new, key=itemgetter(2), reverse=True) 
                    df_sorted_matches= pandas.DataFrame(sorted_matches, columns=self.labels)
                    
                for sorted_user_f in range(len(self.dframeB)):
                    for sorted_label in range(len(self.labels)):
                        sorted_matches_new_f.append(df_sorted_matches.iloc[sorted_user_f][sorted_label])
                    sorted_matches_f.append(sorted_matches_new_f)
                    sorted_matches_new_f=[]
                
                for sorted_user in range(self.number_preferred):
                    for sorted_label in range(len(self.labels)):
                        sorted_matches_new.append(df_sorted_matches.iloc[sorted_user][sorted_label])
                    secondary_matches.append(sorted_matches_new)
                    sorted_matches_new=[]
            else:
                break
        df_secondary_matches= pandas.DataFrame(secondary_matches, columns=self.labels) #converting secondary matches into a dataframe
        df_sorted_matches_f =pandas.DataFrame(sorted_matches_f, columns=self.labels)
        self.df_sorted_matches_f=df_sorted_matches_f
        return df_secondary_matches
    
    def final_matches(self):
        sorted_matches=[]
        final_matches=[]
        for rounds in range(0, len(self.df_sorted_matches_f), len(self.dframeB)):
            for user1_number in range(0, len(self.dframeB)):
                count_already_in_match=0
                already_in_match = False
                for match_num in range(len(final_matches)):
                    if self.df_sorted_matches_f.iloc[user1_number+rounds][2]==-1:
                        already_in_match = True
                    if self.df_sorted_matches_f.iloc[user1_number+rounds][0]==final_matches[match_num][0]:
                        already_in_match = True
                        
                if not already_in_match:
                    for user1_number_f in range(len(final_matches)):
                        if self.df_sorted_matches_f.iloc[user1_number+rounds][1]==final_matches[user1_number_f][1]:
                            count_already_in_match+=1

                            
                    if count_already_in_match< self.multiple_matches:
                        for label in range(len(self.labels)):
                            sorted_matches.append(self.df_sorted_matches_f.iloc[user1_number+rounds][label])
                        final_matches.append(sorted_matches)
                        sorted_matches=[]
                        already_in_match = True 
                        
                if user1_number== len(self.dframeB)-1:
                    if not already_in_match:
                        sorted_matches.append(self.df_sorted_matches_f.iloc[user1_number+rounds][0])
                        for other_label in range(len(self.labels)-1):
                            sorted_matches.append("N/A")   
                        final_matches.append(sorted_matches)
                        sorted_matches=[]     
            
        df_final_matches=pandas.DataFrame(final_matches, columns=self.labels) 
        return df_final_matches
    



# In[283]:

import numpy, pandas
from operator import itemgetter
class Makematch:
    """This class generates matches and a match percentage based on similarly answered questions of two groups. The answers 
    to the questions have to be binary such that if two users have the same answer then their inputs are equal to each other"""

    def __init__(self, dframeA, dframeB, dframeC, dframeD, number_preferred, multiple_matches):
        self.dframeA= dframeA
        self.dframeB= dframeB
        self.dframeC= dframeC
        self.dframeD= dframeD
        self.number_preferred=number_preferred
        self.multiple_matches=multiple_matches
        self.labels=[]
        self.df_match_percentage=pandas.DataFrame(data=numpy.zeros((0,len(self.labels))), columns=self.labels)
        self.df_sorted_matches_f=pandas.DataFrame(data=numpy.zeros((0,len(self.labels))), columns=self.labels)

    def points(self): 
        number_of_question= len(self.dframeA.columns)-1 #how many questions are there excluding the identifier(names)
        match_percentage=[]
        self.labels.append('User1')
        self.labels.append('User2')
        self.labels.append('Match_Percentage')
        self.labels= self.labels + list(self.dframeB.columns.values)[1:]
        for user2_number in range(len(self.dframeB)): #number of user2' where user2_number is each user2's number
            user1 = self.dframeA.iloc[0][0] #each user1
            user2 = self.dframeB.iloc[user2_number][0] #each user2
            points_awarded = 0 
            points_possible = 0
            percentage = 0
            question_matches=[]
            question_matches_new=[]
            for question_number in range(number_of_question): 
                user1_preference = self.dframeA.iloc[0][question_number + 1]
                user2_preference = self.dframeB.iloc[user2_number][question_number + 1]
                if user1_preference == user2_preference:
                    points_awarded += self.dframeC.iloc[question_number][1] #assigning points based on if they match preferences
                    question_match = 1
                    question_matches.append(question_match)
                else: 
                    points_awarded += 0.0
                    question_match = 0
                    question_matches.append(question_match)
                points_possible += self.dframeC.iloc[question_number][1] 
            percentage = ((points_awarded)/points_possible)*100 # match_percentage 
            question_matches_new.append(user1)
            question_matches_new.append(user2)
            question_matches_new.append(percentage)
            for answer_match in question_matches:
                question_matches_new.append(answer_match)
            match_percentage.append(question_matches_new)
        df_match_percentage = pandas.DataFrame(match_percentage, columns=self.labels) #convert match_percentage into a dataframe
        self.df_match_percentage=df_match_percentage
        return df_match_percentage
    
    def new_matches(self):
        match_percentage_new=[]
        match_percentage=[]
        for user1_number in range(len(self.df_match_percentage)): 
            count_already_matched=0
            for user1_number_prev_match in range(len(self.dframeD)):
                if self.df_match_percentage.iloc[user1_number][0]==self.dframeD.iloc[user1_number_prev_match][0]:
                    if self.df_match_percentage.iloc[user1_number][1]==self.dframeD.iloc[user1_number_prev_match][1]:
                        count_already_matched+=1 
                
            if count_already_matched<1:
                for label in range(len(self.labels)):
                    match_percentage.append(self.df_match_percentage.iloc[user1_number][label])
                match_percentage_new.append(match_percentage)
                match_percentage=[]
                
            else:
                match_percentage.append(self.df_match_percentage.iloc[user1_number][0])
                match_percentage.append(self.df_match_percentage.iloc[user1_number][1])
                match_percentage.append(-1)
                for other_label in range(3, len(self.labels)):
                    match_percentage.append(self.df_match_percentage.iloc[user1_number][other_label])
                match_percentage_new.append(match_percentage)
                match_percentage=[]
            
        df_match_percentage = pandas.DataFrame(match_percentage_new, columns=self.labels) 
        self.df_match_percentage=df_match_percentage
        return df_match_percentage
                             
    
    def secondary_matches(self): 
        unsorted_matches=[]
        sorted_matches_new=[]
        secondary_matches=[]
        sorted_matches_new_f=[]
        sorted_matches_f=[]
        for user1_number in range(0, len(self.df_match_percentage), len(self.dframeB)): #looping through each possible user1 match with a user2 and ranking them based on match percentage the step included is the number of user2's
            unsorted_matches_new=[]
            if user1_number < len(self.df_match_percentage):
                for user2_number in range(len(self.dframeB)):
                    for label in range(len(self.labels)):
                        unsorted_matches.append(self.df_match_percentage.iloc[user2_number+user1_number][label])
                    unsorted_matches_new.append(unsorted_matches)
                    unsorted_matches=[]
                    sorted_matches=sorted(unsorted_matches_new, key=itemgetter(2), reverse=True) 
                    df_sorted_matches= pandas.DataFrame(sorted_matches, columns=self.labels)
                    
                for sorted_user_f in range(len(self.dframeB)):
                    for sorted_label in range(len(self.labels)):
                        sorted_matches_new_f.append(df_sorted_matches.iloc[sorted_user_f][sorted_label])
                    sorted_matches_f.append(sorted_matches_new_f)
                    sorted_matches_new_f=[]
                
                for sorted_user in range(self.number_preferred):
                    for sorted_label in range(len(self.labels)):
                        sorted_matches_new.append(df_sorted_matches.iloc[sorted_user][sorted_label])
                    secondary_matches.append(sorted_matches_new)
                    sorted_matches_new=[]
            else:
                break
        df_secondary_matches= pandas.DataFrame(secondary_matches, columns=self.labels) #converting secondary matches into a dataframe
        df_sorted_matches_f =pandas.DataFrame(sorted_matches_f, columns=self.labels)
        self.df_sorted_matches_f=df_sorted_matches_f
        return df_secondary_matches
    
    def final_matches(self):
        sorted_matches=[]
        final_matches=[]
        already_in_match = False
        for user1_number in range(0, len(self.dframeB)):
            count_already_in_match=0
            if self.df_sorted_matches_f.iloc[user1_number][2]==-1:
                already_in_match = True
                
            if not already_in_match:
                for match_num in range(len(self.dframeD)):
                    if self.df_sorted_matches_f.iloc[user1_number][1]==self.dframeD.iloc[match_num][1] and not self.dframeD.iloc[match_num][2]:
                        count_already_in_match+=1


                if count_already_in_match < self.multiple_matches:
                    for label in range(len(self.labels)):
                        sorted_matches.append(self.df_sorted_matches_f.iloc[user1_number][label])
                    final_matches.append(sorted_matches)
                    sorted_matches=[]
                    already_in_match = True 

            if user1_number== len(self.dframeB)-1:
                if not already_in_match:
                    sorted_matches.append(self.df_sorted_matches_f.iloc[user1_number][0])
                    for other_label in range(len(self.labels)-1):
                        sorted_matches.append("N/A")   
                    final_matches.append(sorted_matches)
                    sorted_matches=[]     
            
        df_final_matches=pandas.DataFrame(final_matches, columns=self.labels) 
        return df_final_matches
    


# In[100]:

import numpy, pandas 
import os
print(os.getcwd()) #to see where the items are being saved
data = pandas.ExcelFile('Matching_Data.xlsx') #read excel file using panda
User_Data = pandas.read_excel("Matching_Data.xlsx", sheetname='Users') #reading excel file into a dataframe
Tester_Data = pandas.read_excel("Matching_Data.xlsx", sheetname='Testers') 
Points_Data = pandas.read_excel("Matching_Data.xlsx", sheetname='Points') 
Matched_Data = pandas.read_excel("Matching_Data.xlsx", sheetname='Matched') 


# In[301]:

import numpy, pandas 
import os
print(os.getcwd()) #to see where the items are being saved
data = pandas.ExcelFile('Matching_Data2.xlsx') #read excel file using panda
User_Data = pandas.read_excel("Matching_Data2.xlsx", sheetname='Users') #reading excel file into a dataframe
Tester_Data = pandas.read_excel("Matching_Data2.xlsx", sheetname='Testers') 
Points_Data = pandas.read_excel("Matching_Data2.xlsx", sheetname='Points') 
Matched_Data = pandas.read_excel("Matching_Data2.xlsx", sheetname='Matched')


# In[101]:

matches= Makematches(User_Data, Tester_Data, Points_Data, Matched_Data, 9, 1)


# In[302]:

match= Makematch(User_Data, Tester_Data, Points_Data, Matched_Data, 9, 2)


# In[102]:

matches.points()


# In[303]:

match.points()


# In[103]:

matches.new_matches()


# In[304]:

match.new_matches()


# In[104]:

matches.secondary_matches()


# In[305]:

match.secondary_matches()


# In[191]:

matches.final_matches()


# In[306]:

match.final_matches()


# In[ ]:



