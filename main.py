from sentence_transformers import SentenceTransformer, util
from rapidfuzz import process

class SymptomMatcher:
    def __init__(self, symptom_list):
        # Initialize the symptom list
        self.symptoms = symptom_list

        # Load the sentence embedding model for semantic similarity
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.symptom_embeddings = self.embedding_model.encode(self.symptoms, convert_to_tensor=True)

    def match_symptom(self, input_text, threshold=0.75):
        """
        Matches the input text to the closest symptom using a hybrid approach:
        1. Fuzzy matching for quick phrase-level matching.
        2. Semantic similarity as a fallback for nuanced matches.
        """
        
        # Debugging: Print the symptoms list
        print("Symptoms List:", self.symptoms)
        
        # Step 1: Fuzzy Matching
        fuzzy_match, fuzzy_score, temp = process.extractOne(input_text, self.symptoms)
        
        # Debugging: Print the result of fuzzy matching
        print("Fuzzy Match:", fuzzy_match, "Score:", fuzzy_score)
        
        fuzzy_threshold_score = 75  # Use 75 as a default threshold score
        if fuzzy_score >= fuzzy_threshold_score:
            return fuzzy_match, fuzzy_score, "fuzzy"

        # Step 2: Semantic Similarity
        input_embedding = self.embedding_model.encode(input_text, convert_to_tensor=True)
        similarities = util.cos_sim(input_embedding, self.symptom_embeddings)
        max_index = similarities.argmax()
        best_match = self.symptoms[max_index]

        # Normalize the similarity score to be consistent with fuzzy scores
        similarity_score = float(similarities[0][max_index]) * 100

        return best_match, similarity_score, "semantic"

# Example usage
if __name__ == "__main__":
    # Define the list of known symptoms
    symptoms = ["stomach ache", "headache", "fever", "nausea", "cough"]

    # Initialize the SymptomMatcher
    matcher = SymptomMatcher(symptoms)

    # Input sentences
    inputs = [
        "I have a headache.",
        "There is pain in my stomach.",
        "Feeling nauseous all day.",
        "I have a fever and a bad cough.",
        "My tummy hurts a lot.",
        "Hello",
        "i hurt in my tummy"
    ]

    # Match each input to the closest symptom
    for input_text in inputs:
        matched_symptom, score, method = matcher.match_symptom(input_text)
        print(f"Input: {input_text}")
        print(f"Matched Symptom: {matched_symptom} (Score: {score:.2f}, Method: {method})")
        print("-" * 50)
