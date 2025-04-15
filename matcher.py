import re
from sentence_transformers import SentenceTransformer, util

class SymptomMatcher:
    '''This is a class which has 1 function match_symptom, it uses the initialised symptoms when defining the class, and matches them (it can also match synonyms)'''
    def __init__(self, symptom_list):
        self.symptoms = symptom_list
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.symptom_embeddings = self.embedding_model.encode(self.symptoms, convert_to_tensor=True)

    def normalize_text(self, text):

        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return_text = ""

        for char in text.split():
            temp = self.embedding_model.encode(char,convert_to_tensor=True)
            similarities = util.cos_sim(temp,self.symptom_embeddings)
            for idx, score in enumerate(similarities[0]):
                # print(char,self.symptoms[idx],score.item())
                if score.item() > 0.5:
                    return_text+=char + " "
                    break
        # print(return_text)
        # print("The return text is above")
        return return_text

    # uses cos function with vector mapping to compare words and scentences 
    def match_symptoms(self, input_r):
        matched_symptoms = []
        for input_text in input_r:
            normalized_input = (input_text)
            input_embedding = self.embedding_model.encode(normalized_input, convert_to_tensor=True)
            similarities = util.cos_sim(input_embedding, self.symptom_embeddings)
            temp = []
            # print(similarities[0])
            flg = False
            for idx, score in enumerate(similarities[0]):
                temp.append((score.item(),self.symptoms[idx]))
                if score.item() > 0.70: 
                    flg = True
                    # matched_symptoms.append(self.symptoms[idx])
                    # print(normalized_input,self.symptoms[idx],score.item())
            if(flg):
                temp.sort(reverse=True)
                matched_symptoms.append(temp[0][1])
            # for a,b in temp:
            #     print(a,b)
        # print(input_r,matched_symptoms)
        return matched_symptoms,"",""
