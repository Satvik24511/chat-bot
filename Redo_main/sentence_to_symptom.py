from imp_funcs import * 
import logger
def create_list_for_symptoms(s): #takes in a string s as function input and then returns a list with comma seperated potential symtoms for matching.
    ls = []
    try:
        import api_handler as ah
        api_class = ah.GeminiAPIHandler("AIzaSyBkRDmEdtVhVtHHbfvpetHKANTz1EW1qYQ")
        ls = api_class.extract_symptoms(s)
        return ls
    except:
        # print("Gemini failed, going to fallback")
        logger.log_error(f"Gemini Failed to load", exc_info=True)
        a = s.split()
        n = len(a)
        ap = ""
        for i in range(n):
            for j in range(n-i):
                for k in range(i+1):
                    ap += a[j+k] + " "
                ls.append(ap)
                ap = ""
        return ls
    
def get_symptoms(s):
    ls = create_list_for_symptoms(s)
    rt = set()
    if(len(ls) == 0 or ls[0] == 'no'):
        logger.symptom_logger.debug("----"+s)
        return False,"No symptoms found"
    else:
        for i in ls:
            present = False
            embeddingA = model.encode(i)
            for j in range(len(embedding_symptom)):
                similarity = float(cosine_similarity([embeddingA[0]], [embedding_symptom[j]]))
                if(similarity > 0.75):
                    present = True
                    rt.add(symptom_list[j])
                    break
            if(present == False):
                logger.symptom_logger.debug(i)
    return list(rt)


if __name__ == "__main__":
    print(get_symptoms("Hi, this is a test"))