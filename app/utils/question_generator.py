

import re
import random
from typing import List, Dict, Optional
from datetime import datetime


class SmartQuestionGenerator:
    
    
    @staticmethod
    def generate_questions_from_topic(topic_title: str, topic_description: str, 
                                    num_questions: int = 5, difficulty: str = 'medium') -> List[Dict]:
        
        questions = []
        
        
        key_concepts = SmartQuestionGenerator._extract_key_concepts(topic_title, topic_description)
        
        
        question_types = ['multiple_choice', 'true_false', 'fill_blank']
        
        for i in range(num_questions):
            question_type = random.choice(question_types)
            
            if question_type == 'multiple_choice':
                question = SmartQuestionGenerator._generate_multiple_choice(
                    topic_title, topic_description, key_concepts, difficulty
                )
            elif question_type == 'true_false':
                question = SmartQuestionGenerator._generate_true_false(
                    topic_title, topic_description, key_concepts, difficulty
                )
            else:  
                question = SmartQuestionGenerator._generate_fill_blank(
                    topic_title, topic_description, key_concepts, difficulty
                )
            
            if question:
                questions.append(question)
        
        return questions[:num_questions]
    
    @staticmethod
    def _extract_key_concepts(topic_title: str, topic_description: str) -> List[str]:
        
        
        content = f"{topic_title} {topic_description}".lower()
        
        
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 
            'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
        }
        
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', content)
        key_concepts = []
        
        for word in words:
            if word not in stop_words and len(word) > 3:
                
                if content.count(word) > 1:
                    key_concepts.append(word.title())
        
        
        return list(set(key_concepts))[:10]
    
    @staticmethod
    def _generate_multiple_choice(topic_title: str, topic_description: str, 
                                key_concepts: List[str], difficulty: str) -> Optional[Dict]:
        
        
        
        question_templates = [
            f"What is the primary purpose of {topic_title.lower()}?",
            f"Which of the following best describes {topic_title.lower()}?",
            f"What is a key characteristic of {topic_title.lower()}?",
            f"Which statement about {topic_title.lower()} is most accurate?",
            f"What is the main benefit of {topic_title.lower()}?",
            f"Which of the following is true about {topic_title.lower()}?",
            f"What is the primary function of {topic_title.lower()}?",
            f"Which best explains {topic_title.lower()}?"
        ]
        
        
        if "process" in topic_description.lower() or "method" in topic_description.lower():
            question_text = f"What is the main process involved in {topic_title.lower()}?"
        elif "benefit" in topic_description.lower() or "advantage" in topic_description.lower():
            question_text = f"What is a key benefit of {topic_title.lower()}?"
        elif "definition" in topic_description.lower() or "define" in topic_description.lower():
            question_text = f"Which of the following best defines {topic_title.lower()}?"
        else:
            question_text = random.choice(question_templates)
        
        
        correct_answer = SmartQuestionGenerator._extract_correct_answer(topic_description)
        
        
        wrong_answers = SmartQuestionGenerator._generate_wrong_answers(
            topic_title, topic_description, key_concepts, correct_answer
        )
        
        
        all_options = [correct_answer] + wrong_answers[:3]  
        random.shuffle(all_options)
        
        
        correct_index = all_options.index(correct_answer)
        
        return {
            'question_text': question_text,
            'question_type': 'multiple_choice',
            'correct_answer': correct_answer,
            'options': [
                {'text': option, 'is_correct': i == correct_index}
                for i, option in enumerate(all_options)
            ],
            'explanation': SmartQuestionGenerator._generate_explanation(topic_title, correct_answer),
            'difficulty': difficulty,
            'points': SmartQuestionGenerator._calculate_points(difficulty)
        }
    
    @staticmethod
    def _generate_true_false(topic_title: str, topic_description: str, 
                           key_concepts: List[str], difficulty: str) -> Optional[Dict]:
        
        
        
        content_analysis = SmartQuestionGenerator._analyze_content_for_tf(topic_description)
        
        if content_analysis['should_be_true']:
            statement = content_analysis['true_statement']
            correct_answer = "True"
        else:
            statement = content_analysis['false_statement']
            correct_answer = "False"
        
        return {
            'question_text': statement,
            'question_type': 'true_false',
            'correct_answer': correct_answer,
            'explanation': SmartQuestionGenerator._generate_explanation(topic_title, correct_answer),
            'difficulty': difficulty,
            'points': SmartQuestionGenerator._calculate_points(difficulty)
        }
    
    @staticmethod
    def _generate_fill_blank(topic_title: str, topic_description: str, 
                           key_concepts: List[str], difficulty: str) -> Optional[Dict]:
        
        
        
        if key_concepts:
            key_concept = random.choice(key_concepts)
            
            
            templates = [
                f"{topic_title} is primarily used for _____.",
                f"The main purpose of {topic_title.lower()} is to _____.",
                f"{topic_title} helps in _____.",
                f"One key benefit of {topic_title.lower()} is _____.",
                f"{topic_title} is important because it _____."
            ]
            
            question_text = random.choice(templates)
            correct_answer = SmartQuestionGenerator._extract_correct_answer(topic_description)
            
            return {
                'question_text': question_text,
                'question_type': 'fill_blank',
                'correct_answer': correct_answer,
                'explanation': SmartQuestionGenerator._generate_explanation(topic_title, correct_answer),
                'difficulty': difficulty,
                'points': SmartQuestionGenerator._calculate_points(difficulty)
            }
        
        return None
    
    @staticmethod
    def _extract_correct_answer(description: str) -> str:
        
        
        sentences = description.split('.')
        
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 100:
                
                answer = sentence.replace('\n', ' ').strip()
                if answer:
                    return answer
        
        
        if sentences:
            return sentences[0].strip()[:50] + "..."
        
        return "This is a key concept in the topic."
    
    @staticmethod
    def _generate_wrong_answers(topic_title: str, topic_description: str, 
                              key_concepts: List[str], correct_answer: str) -> List[str]:
        
        wrong_answers = []
        
        
        generic_wrong = [
            "To increase complexity",
            "To reduce efficiency", 
            "To make things more difficult",
            "To decrease productivity",
            "To complicate the process",
            "To slow down operations",
            "To create confusion",
            "To waste resources"
        ]
        
        
        if "learning" in topic_title.lower() or "study" in topic_title.lower():
            wrong_answers.extend([
                "To avoid studying",
                "To skip important topics",
                "To memorize without understanding"
            ])
        elif "process" in topic_title.lower():
            wrong_answers.extend([
                "To make the process longer",
                "To add unnecessary steps",
                "To complicate the workflow"
            ])
        elif "management" in topic_title.lower():
            wrong_answers.extend([
                "To create chaos",
                "To lose control",
                "To ignore priorities"
            ])
        
        
        wrong_answers.extend(generic_wrong)
        
        
        wrong_answers = list(set(wrong_answers))
        random.shuffle(wrong_answers)
        
        return wrong_answers[:3]
    
    @staticmethod
    def _analyze_content_for_tf(description: str) -> Dict:
        
        description_lower = description.lower()
        
        
        positive_indicators = ['benefit', 'advantage', 'improve', 'enhance', 'help', 'support', 'enable']
        negative_indicators = ['problem', 'issue', 'difficulty', 'challenge', 'limitation', 'disadvantage']
        
        positive_count = sum(1 for indicator in positive_indicators if indicator in description_lower)
        negative_count = sum(1 for indicator in negative_indicators if indicator in description_lower)
        
        if positive_count > negative_count:
            
            true_statements = [
                f"This topic provides valuable benefits for learning.",
                f"This concept helps improve understanding.",
                f"This approach enhances learning outcomes.",
                f"This method supports effective learning.",
                f"This technique is beneficial for students."
            ]
            return {
                'should_be_true': True,
                'true_statement': random.choice(true_statements),
                'false_statement': f"This topic has no benefits for learning."
            }
        else:
            
            false_statements = [
                f"This topic is completely useless for learning.",
                f"This concept has no practical applications.",
                f"This approach never works effectively.",
                f"This method always fails to help students.",
                f"This technique provides no benefits."
            ]
            return {
                'should_be_true': False,
                'true_statement': f"This topic provides valuable learning benefits.",
                'false_statement': random.choice(false_statements)
            }
    
    @staticmethod
    def _generate_explanation(topic_title: str, answer: str) -> str:
        
        explanations = [
            f"This is correct because {topic_title.lower()} is designed to provide this benefit.",
            f"The answer is accurate as {topic_title.lower()} specifically addresses this aspect.",
            f"This is true because {topic_title.lower()} focuses on this particular function.",
            f"The correct answer reflects the primary purpose of {topic_title.lower()}.",
            f"This is accurate as {topic_title.lower()} is known for this characteristic."
        ]
        return random.choice(explanations)
    
    @staticmethod
    def _calculate_points(difficulty: str) -> int:
        
        point_map = {
            'easy': 1,
            'medium': 2,
            'hard': 3
        }
        return point_map.get(difficulty, 2)
    
    @staticmethod
    def generate_flashcards_from_topic(topic_title: str, topic_description: str, 
                                     num_cards: int = 5) -> List[Dict]:
        
        flashcards = []
        
        
        key_concepts = SmartQuestionGenerator._extract_key_concepts(topic_title, topic_description)
        
        
        for i in range(min(num_cards, len(key_concepts))):
            concept = key_concepts[i] if i < len(key_concepts) else f"Key concept {i+1}"
            
            
            question = f"What is {concept} in {topic_title}?"
            answer = SmartQuestionGenerator._extract_correct_answer(topic_description)
            
            flashcards.append({
                'question_text': question,
                'question_type': 'flashcard',
                'correct_answer': answer,
                'explanation': f"This explains the concept of {concept} in {topic_title}.",
                'difficulty': 'medium',
                'points': 1
            })
        
        return flashcards

