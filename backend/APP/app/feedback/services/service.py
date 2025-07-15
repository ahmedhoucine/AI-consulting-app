from feedback.repositories import repository
import ollama  # ou un wrapper de ton choix vers Ollama Mistral

def lister_feedbacks():
    return repository.get_all_feedbacks()
