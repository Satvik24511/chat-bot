from sentence_transformers import SentenceTransformer,util


class SymptomMatcher:
    '''This is a class which has 1 function match_symptom, it uses the initialised symptoms when defining the class, and matches them (it can also match synonyms)'''
    def __init__(self, symptom_list):
        self.symptoms = symptom_list
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.symptom_embeddings = self.embedding_model.encode(self.symptoms, convert_to_tensor=True) #encode changes the sentence into a 384 dimensional vector
        # print("These are the symptom_emmbeddingsa or wtv:", self.symptom_embeddings)
        # print("This is the 2nd thing,",self.embedding_model.encode("Daksh", convert_to_tensor=True))
    def normalize_text(self, text):

        return_text = []
        # print(return_text)
        # print("The return text is above")
        return return_text

    # uses cos function with vector mapping to compare words and scentences 
    def match_symptoms(self, input_text):
        normalized_input = self.normalize_text(input_text) # normalized_input is a list here with potential phrases that can be symptoms
        matched_symptoms = []

        # for symptom in self.symptoms:
        #     if symptom in normalized_input:
        #         matched_symptoms.append(symptom) #this loop is for checking if the exact symptom is present in the symptoms list.
        # print(matched_symptoms,normalized_input)
        
        
        input_embedding = self.embedding_model.encode(normalized_input, convert_to_tensor=True)
        similarities = util.cos_sim(input_embedding, self.symptom_embeddings)
        temp = []
        flg = False
        for i in range(len(normalized_input)):
            for idx, score in enumerate(similarities[i]):
                temp.append((score.item(),self.symptoms[idx]))
                if score.item() > 0.70: 
                    if self.symptoms[idx] not in matched_symptoms:
                        matched_symptoms.append(self.symptoms[idx])
                    flg = True
                    break
        temp.sort(reverse=True)
        return matched_symptoms
