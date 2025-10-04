
import re
import random
import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


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
    
    @staticmethod
    def get_openai_client():
        """Get OpenAI client if available"""
        if not OPENAI_AVAILABLE:
            return None
            
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return None
            
        try:
            return openai.OpenAI(api_key=api_key)
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
            return None
    
    @staticmethod
    def generate_smart_quiz_from_topic(topic_title: str, topic_description: str, 
                                     num_questions: int = 5, difficulty: str = 'mixed',
                                     question_types: List[str] = None) -> Dict:
        """
        Generate a complete quiz using AI from topic description
        """
        if question_types is None:
            question_types = ['multiple_choice', 'true_false', 'fill_blank']
        
        # Try AI generation first
        ai_quiz = SmartQuestionGenerator._generate_ai_quiz(
            topic_title, topic_description, num_questions, difficulty, question_types
        )
        
        if ai_quiz:
            return ai_quiz
        
        # Fallback to enhanced rule-based generation
        return SmartQuestionGenerator._generate_enhanced_quiz(
            topic_title, topic_description, num_questions, difficulty, question_types
        )
    
    @staticmethod
    def _generate_ai_quiz(topic_title: str, topic_description: str, 
                         num_questions: int, difficulty: str, question_types: List[str]) -> Optional[Dict]:
        """Generate quiz using OpenAI API"""
        
        client = SmartQuestionGenerator.get_openai_client()
        if not client:
            return None
        
        try:
            # Create the prompt for AI
            prompt = SmartQuestionGenerator._create_quiz_generation_prompt(
                topic_title, topic_description, num_questions, difficulty, question_types
            )
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator specializing in quiz generation. Create high-quality, educational quiz questions based on the given topic."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            quiz_content = response.choices[0].message.content
            
            # Parse the JSON response
            try:
                quiz_data = json.loads(quiz_content)
                return SmartQuestionGenerator._validate_and_format_ai_quiz(quiz_data, topic_title)
            except json.JSONDecodeError:
                # Try to extract JSON from the response
                json_match = re.search(r'\{.*\}', quiz_content, re.DOTALL)
                if json_match:
                    quiz_data = json.loads(json_match.group())
                    return SmartQuestionGenerator._validate_and_format_ai_quiz(quiz_data, topic_title)
                
        except Exception as e:
            print(f"AI quiz generation failed: {e}")
        
        return None
    
    @staticmethod
    def _create_quiz_generation_prompt(topic_title: str, topic_description: str, 
                                     num_questions: int, difficulty: str, question_types: List[str]) -> str:
        """Create a detailed prompt for AI quiz generation"""
        
        question_types_str = ", ".join(question_types)
        
        prompt = f"""
Generate a quiz with {num_questions} questions based on this topic:

Topic: {topic_title}
Description: {topic_description}

Requirements:
- Create {num_questions} questions
- Use these question types: {question_types_str}
- Difficulty level: {difficulty}
- Questions should test understanding, not just memorization
- Include clear explanations for each answer
- Make questions relevant and educational
- Ensure variety in question types

Return your response as a JSON object with this exact structure:
{{
    "quiz_title": "Quiz about {topic_title}",
    "quiz_description": "Test your knowledge of {topic_title}",
    "difficulty": "{difficulty}",
    "questions": [
        {{
            "question_text": "Question text here",
            "question_type": "multiple_choice",
            "options": [
                {{"text": "Option 1", "is_correct": false}},
                {{"text": "Option 2", "is_correct": true}},
                {{"text": "Option 3", "is_correct": false}},
                {{"text": "Option 4", "is_correct": false}}
            ],
            "correct_answer": "Option 2",
            "explanation": "Explanation of why this answer is correct",
            "difficulty": "medium",
            "points": 2
        }}
    ]
}}

For multiple choice: include 4 options with exactly one correct answer.
For true/false: set question_type to "true_false" and correct_answer to "True" or "False".
For fill-in-blank: set question_type to "fill_blank" and provide the correct answer text.
"""
        
        return prompt
    
    @staticmethod
    def _validate_and_format_ai_quiz(quiz_data: Dict, topic_title: str) -> Optional[Dict]:
        """Validate and format AI-generated quiz data"""
        
        try:
            if not isinstance(quiz_data, dict) or 'questions' not in quiz_data:
                return None
            
            questions = quiz_data.get('questions', [])
            if not questions:
                return None
            
            # Validate and format each question
            formatted_questions = []
            for q in questions:
                formatted_q = SmartQuestionGenerator._format_ai_question(q)
                if formatted_q:
                    formatted_questions.append(formatted_q)
            
            if not formatted_questions:
                return None
            
            return {
                'quiz_title': quiz_data.get('quiz_title', f'Quiz: {topic_title}'),
                'quiz_description': quiz_data.get('quiz_description', f'Test your knowledge of {topic_title}'),
                'difficulty': quiz_data.get('difficulty', 'medium'),
                'questions': formatted_questions,
                'generation_method': 'ai'
            }
            
        except Exception as e:
            print(f"Error validating AI quiz: {e}")
            return None
    
    @staticmethod
    def _format_ai_question(question_data: Dict) -> Optional[Dict]:
        """Format a single AI-generated question"""
        
        try:
            question_text = question_data.get('question_text', '').strip()
            question_type = question_data.get('question_type', 'multiple_choice')
            correct_answer = question_data.get('correct_answer', '').strip()
            explanation = question_data.get('explanation', '').strip()
            difficulty = question_data.get('difficulty', 'medium')
            points = question_data.get('points', 2)
            
            if not question_text or not correct_answer:
                return None
            
            formatted_question = {
                'question_text': question_text,
                'question_type': question_type,
                'correct_answer': correct_answer,
                'explanation': explanation or f"This is the correct answer for the question.",
                'difficulty': difficulty,
                'points': points if isinstance(points, int) else 2
            }
            
            # Handle different question types
            if question_type == 'multiple_choice':
                options = question_data.get('options', [])
                if not options:
                    return None
                
                formatted_options = []
                for opt in options:
                    if isinstance(opt, dict):
                        formatted_options.append({
                            'text': opt.get('text', '').strip(),
                            'is_correct': opt.get('is_correct', False)
                        })
                
                if len(formatted_options) >= 2:
                    formatted_question['options'] = formatted_options
                else:
                    return None
            
            elif question_type == 'true_false':
                if correct_answer not in ['True', 'False']:
                    return None
            
            elif question_type == 'fill_blank':
                # Fill in blank questions don't need options
                pass
            
            else:
                # Unknown question type
                return None
            
            return formatted_question
            
        except Exception as e:
            print(f"Error formatting AI question: {e}")
            return None
    
    @staticmethod
    def _generate_enhanced_quiz(topic_title: str, topic_description: str, 
                               num_questions: int, difficulty: str, question_types: List[str]) -> Dict:
        """Enhanced fallback quiz generation using improved rule-based methods"""
        
        questions = []
        
        # Extract enhanced key concepts
        key_concepts = SmartQuestionGenerator._extract_enhanced_concepts(topic_title, topic_description)
        
        # Determine question distribution
        question_distribution = SmartQuestionGenerator._calculate_question_distribution(
            num_questions, question_types
        )
        
        # Generate questions based on distribution
        for question_type, count in question_distribution.items():
            for _ in range(count):
                question = None
                
                if question_type == 'multiple_choice':
                    question = SmartQuestionGenerator._generate_enhanced_multiple_choice(
                        topic_title, topic_description, key_concepts, difficulty
                    )
                elif question_type == 'true_false':
                    question = SmartQuestionGenerator._generate_enhanced_true_false(
                        topic_title, topic_description, key_concepts, difficulty
                    )
                elif question_type == 'fill_blank':
                    question = SmartQuestionGenerator._generate_enhanced_fill_blank(
                        topic_title, topic_description, key_concepts, difficulty
                    )
                
                if question:
                    questions.append(question)
        
        return {
            'quiz_title': f'Quiz: {topic_title}',
            'quiz_description': f'Test your knowledge of {topic_title}',
            'difficulty': difficulty,
            'questions': questions[:num_questions],
            'generation_method': 'enhanced_rule_based'
        }
    
    @staticmethod
    def _extract_enhanced_concepts(topic_title: str, topic_description: str) -> List[str]:
        """Enhanced concept extraction with better NLP techniques"""
        
        content = f"{topic_title} {topic_description}".lower()
        
        # Enhanced stop words list
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 
            'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their',
            'also', 'very', 'really', 'just', 'like', 'get', 'go', 'come', 'make', 'take',
            'use', 'used', 'using', 'way', 'ways', 'thing', 'things', 'part', 'parts'
        }
        
        # Extract words with better regex
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content)
        
        # Count word frequency
        word_freq = {}
        for word in words:
            if word not in stop_words and len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and relevance
        key_concepts = []
        for word, freq in sorted(word_freq.items(), key=lambda x: x[1], reverse=True):
            if freq > 1:  # Only words that appear multiple times
                key_concepts.append(word.title())
        
        # Also extract phrases (2-3 word combinations)
        phrases = re.findall(r'\b[a-zA-Z]{3,}\s+[a-zA-Z]{3,}(?:\s+[a-zA-Z]{3,})?\b', content)
        for phrase in phrases:
            if len(phrase.split()) <= 3:  # Only short phrases
                key_concepts.append(phrase.title())
        
        return list(set(key_concepts))[:15]  # Return top 15 concepts
    
    @staticmethod
    def _calculate_question_distribution(num_questions: int, question_types: List[str]) -> Dict[str, int]:
        """Calculate how many questions of each type to generate"""
        
        distribution = {}
        
        if 'multiple_choice' in question_types:
            distribution['multiple_choice'] = max(1, num_questions // 2)
        
        if 'true_false' in question_types:
            distribution['true_false'] = max(1, num_questions // 3)
        
        if 'fill_blank' in question_types:
            remaining = num_questions - sum(distribution.values())
            distribution['fill_blank'] = max(0, remaining)
        
        # Ensure we don't exceed the requested number
        total = sum(distribution.values())
        if total > num_questions:
            # Reduce from the most common type
            if 'multiple_choice' in distribution:
                distribution['multiple_choice'] -= (total - num_questions)
        
        return {k: v for k, v in distribution.items() if v > 0}
    
    @staticmethod
    def _generate_enhanced_multiple_choice(topic_title: str, topic_description: str, 
                                         key_concepts: List[str], difficulty: str) -> Optional[Dict]:
        """Enhanced multiple choice question generation"""
        
        # More sophisticated question templates
        templates = [
            f"Which of the following best describes the primary function of {topic_title.lower()}?",
            f"What is the main advantage of using {topic_title.lower()}?",
            f"Which statement accurately reflects the purpose of {topic_title.lower()}?",
            f"What is a key characteristic that defines {topic_title.lower()}?",
            f"Which of the following is most important when considering {topic_title.lower()}?",
            f"What makes {topic_title.lower()} effective in its application?",
            f"Which factor contributes most to the success of {topic_title.lower()}?",
            f"What is the primary goal when implementing {topic_title.lower()}?"
        ]
        
        question_text = random.choice(templates)
        
        # Extract better correct answer
        correct_answer = SmartQuestionGenerator._extract_enhanced_answer(topic_description)
        
        # Generate better wrong answers
        wrong_answers = SmartQuestionGenerator._generate_enhanced_wrong_answers(
            topic_title, topic_description, key_concepts, correct_answer
        )
        
        # Ensure we have enough options
        all_options = [correct_answer] + wrong_answers[:3]
        if len(all_options) < 4:
            all_options.extend([
                "This option is not applicable",
                "None of the above",
                "Cannot be determined"
            ])
        
        all_options = all_options[:4]  # Limit to 4 options
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
            'explanation': SmartQuestionGenerator._generate_enhanced_explanation(topic_title, correct_answer),
            'difficulty': difficulty,
            'points': SmartQuestionGenerator._calculate_points(difficulty)
        }
    
    @staticmethod
    def _generate_enhanced_true_false(topic_title: str, topic_description: str, 
                                    key_concepts: List[str], difficulty: str) -> Optional[Dict]:
        """Enhanced true/false question generation"""
        
        # Analyze content more intelligently
        content_analysis = SmartQuestionGenerator._analyze_content_for_enhanced_tf(topic_description)
        
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
            'explanation': SmartQuestionGenerator._generate_enhanced_explanation(topic_title, correct_answer),
            'difficulty': difficulty,
            'points': SmartQuestionGenerator._calculate_points(difficulty)
        }
    
    @staticmethod
    def _generate_enhanced_fill_blank(topic_title: str, topic_description: str, 
                                    key_concepts: List[str], difficulty: str) -> Optional[Dict]:
        """Enhanced fill-in-the-blank question generation"""
        
        if not key_concepts:
            return None
        
        # Better templates
        templates = [
            f"The primary purpose of {topic_title.lower()} is to _____.",
            f"One key benefit of {topic_title.lower()} is that it _____.",
            f"{topic_title} is important because it _____.",
            f"The main advantage of using {topic_title.lower()} is _____.",
            f"{topic_title} helps students by _____.",
            f"The effectiveness of {topic_title.lower()} depends on _____.",
            f"{topic_title} works best when _____.",
            f"The core concept behind {topic_title.lower()} is _____."
        ]
        
        question_text = random.choice(templates)
        correct_answer = SmartQuestionGenerator._extract_enhanced_answer(topic_description)
        
        return {
            'question_text': question_text,
            'question_type': 'fill_blank',
            'correct_answer': correct_answer,
            'explanation': SmartQuestionGenerator._generate_enhanced_explanation(topic_title, correct_answer),
            'difficulty': difficulty,
            'points': SmartQuestionGenerator._calculate_points(difficulty)
        }
    
    @staticmethod
    def _extract_enhanced_answer(description: str) -> str:
        """Extract better answers from descriptions"""
        
        # Split into sentences and clean them
        sentences = [s.strip() for s in description.split('.') if s.strip()]
        
        # Look for key sentences
        for sentence in sentences:
            # Skip very short or very long sentences
            if 15 <= len(sentence) <= 120:
                # Look for sentences with key words
                if any(word in sentence.lower() for word in ['primary', 'main', 'key', 'important', 'benefit', 'advantage', 'purpose', 'function']):
                    return sentence
        
        # Fallback to first reasonable sentence
        for sentence in sentences:
            if 20 <= len(sentence) <= 100:
                return sentence
        
        # Final fallback
        return "This concept is important for understanding the topic."
    
    @staticmethod
    def _generate_enhanced_wrong_answers(topic_title: str, topic_description: str, 
                                       key_concepts: List[str], correct_answer: str) -> List[str]:
        """Generate better wrong answers"""
        
        wrong_answers = []
        
        # Context-aware wrong answers
        topic_lower = topic_title.lower()
        desc_lower = topic_description.lower()
        
        if 'learning' in topic_lower or 'study' in topic_lower:
            wrong_answers.extend([
                "To avoid studying effectively",
                "To make learning more difficult",
                "To skip important concepts",
                "To memorize without understanding"
            ])
        elif 'process' in topic_lower or 'method' in topic_lower:
            wrong_answers.extend([
                "To complicate the process unnecessarily",
                "To add redundant steps",
                "To slow down the workflow",
                "To create confusion"
            ])
        elif 'management' in topic_lower or 'organize' in topic_lower:
            wrong_answers.extend([
                "To create disorganization",
                "To lose track of important items",
                "To ignore priorities",
                "To waste time and resources"
            ])
        else:
            # Generic wrong answers
            wrong_answers.extend([
                "To increase complexity unnecessarily",
                "To reduce efficiency",
                "To create more problems",
                "To waste time and effort"
            ])
        
        # Remove duplicates and shuffle
        wrong_answers = list(set(wrong_answers))
        random.shuffle(wrong_answers)
        
        return wrong_answers[:3]
    
    @staticmethod
    def _analyze_content_for_enhanced_tf(description: str) -> Dict:
        """Enhanced true/false analysis"""
        
        desc_lower = description.lower()
        
        # More sophisticated analysis
        positive_indicators = {
            'benefit': 3, 'advantage': 3, 'improve': 2, 'enhance': 2, 'help': 2, 
            'support': 2, 'enable': 2, 'effective': 2, 'successful': 2, 'valuable': 2,
            'important': 1, 'useful': 1, 'good': 1, 'better': 1, 'increases': 1
        }
        
        negative_indicators = {
            'problem': 3, 'issue': 3, 'difficulty': 2, 'challenge': 2, 'limitation': 2, 
            'disadvantage': 2, 'fails': 2, 'ineffective': 2, 'waste': 2, 'harmful': 2,
            'bad': 1, 'worse': 1, 'decreases': 1, 'reduces': 1
        }
        
        positive_score = sum(score for word, score in positive_indicators.items() if word in desc_lower)
        negative_score = sum(score for word, score in negative_indicators.items() if word in desc_lower)
        
        if positive_score > negative_score:
            # Generate true statement
            true_statements = [
                f"This topic provides valuable benefits for learning and understanding.",
                f"This approach is effective for improving knowledge retention.",
                f"This method helps students learn more efficiently.",
                f"This technique enhances the learning experience.",
                f"This concept is important for educational success."
            ]
            return {
                'should_be_true': True,
                'true_statement': random.choice(true_statements),
                'false_statement': f"This topic has no educational value or benefits."
            }
        else:
            # Generate false statement
            false_statements = [
                f"This topic is completely useless for learning purposes.",
                f"This approach never works and always fails.",
                f"This method has no benefits whatsoever.",
                f"This technique is harmful to learning progress.",
                f"This concept should be avoided in education."
            ]
            return {
                'should_be_true': False,
                'true_statement': f"This topic provides valuable learning benefits.",
                'false_statement': random.choice(false_statements)
            }
    
    @staticmethod
    def _generate_enhanced_explanation(topic_title: str, answer: str) -> str:
        """Generate better explanations"""
        
        explanations = [
            f"This is correct because {topic_title.lower()} is specifically designed to provide this benefit.",
            f"The answer is accurate as {topic_title.lower()} focuses on this particular aspect.",
            f"This is true because {topic_title.lower()} addresses this important concept.",
            f"The correct answer reflects the primary purpose of {topic_title.lower()}.",
            f"This is accurate as {topic_title.lower()} is known for this characteristic.",
            f"This answer is correct because it aligns with the core principles of {topic_title.lower()}.",
            f"The statement is true as {topic_title.lower()} specifically emphasizes this point."
        ]
        return random.choice(explanations)

