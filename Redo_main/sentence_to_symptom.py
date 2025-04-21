def create_list_for_symptoms(s): #takes in a string s as function input and then returns a list with comma seperated potential symtoms for matching.
    ls = []
    try:
        import api_handler as ah
        api_class = ah.GeminiAPIHandler("AIzaSyBkRDmEdtVhVtHHbfvpetHKANTz1EW1qYQ")
        ls = api_class.extract_symptoms(s)
        return ls
    except:
        # print("Gemini failed, going to fallback")
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

if __name__ == "__main__":
    print(create_list_for_symptoms("I have a headache, cough and pain in my tummy"))