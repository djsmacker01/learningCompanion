

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, BooleanField, RadioField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from wtforms.widgets import TextArea


class CreateQuizForm(FlaskForm):
    
    title = StringField('Quiz Title', validators=[DataRequired(), Length(min=1, max=255)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    quiz_type = SelectField('Quiz Type', 
                           choices=[
                               ('multiple_choice', 'Multiple Choice'),
                               ('flashcards', 'Flashcards'),
                               ('practice_test', 'Practice Test'),
                               ('assessment', 'Assessment')
                           ],
                           validators=[DataRequired()])
    difficulty_level = SelectField('Difficulty Level',
                                  choices=[
                                      ('easy', 'Easy'),
                                      ('medium', 'Medium'),
                                      ('hard', 'Hard')
                                  ],
                                  default='medium',
                                  validators=[DataRequired()])
    time_limit_minutes = IntegerField('Time Limit (minutes)', 
                                     validators=[Optional(), NumberRange(min=1, max=300)],
                                     render_kw={'placeholder': 'Leave empty for no time limit'})
    passing_score = IntegerField('Passing Score (%)', 
                                default=70,
                                validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Create Quiz')


class CreateQuestionForm(FlaskForm):
    
    question_text = TextAreaField('Question', 
                                 validators=[DataRequired(), Length(min=1, max=2000)],
                                 render_kw={'rows': 4, 'placeholder': 'Enter your question here...'})
    question_type = SelectField('Question Type',
                               choices=[
                                   ('multiple_choice', 'Multiple Choice'),
                                   ('true_false', 'True/False'),
                                   ('fill_blank', 'Fill in the Blank'),
                                   ('flashcard', 'Flashcard')
                               ],
                               validators=[DataRequired()])
    correct_answer = TextAreaField('Correct Answer',
                                  validators=[DataRequired(), Length(min=1, max=500)],
                                  render_kw={'rows': 2, 'placeholder': 'Enter the correct answer...'})
    explanation = TextAreaField('Explanation (Optional)',
                               validators=[Optional(), Length(max=1000)],
                               render_kw={'rows': 3, 'placeholder': 'Explain why this is the correct answer...'})
    points = IntegerField('Points', 
                         default=1,
                         validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Add Question')


class MultipleChoiceOptionForm(FlaskForm):
    
    option_text = StringField('Option Text', 
                             validators=[DataRequired(), Length(min=1, max=500)],
                             render_kw={'placeholder': 'Enter option text...'})
    is_correct = BooleanField('Correct Answer')
    submit = SubmitField('Add Option')


class TakeQuizForm(FlaskForm):
    
    answer = StringField('Your Answer', 
                        validators=[DataRequired(), Length(min=1, max=500)],
                        render_kw={'placeholder': 'Enter your answer...'})
    submit = SubmitField('Submit Answer')


class FlashcardReviewForm(FlaskForm):
    
    quality = SelectField('How well did you know this?',
                         choices=[
                             (0, '0 - Complete blackout'),
                             (1, '1 - Incorrect response; correct one remembered'),
                             (2, '2 - Incorrect response; where correct one seemed easy to recall'),
                             (3, '3 - Correct response after hesitation'),
                             (4, '4 - Correct response after brief hesitation'),
                             (5, '5 - Perfect response')
                         ],
                         coerce=int,
                         validators=[DataRequired()])
    submit = SubmitField('Submit Review')


class QuizSearchForm(FlaskForm):
    
    search_term = StringField('Search Quizzes', 
                             validators=[Optional(), Length(min=1, max=100)],
                             render_kw={'placeholder': 'Search by title or description...'})
    quiz_type = SelectField('Quiz Type',
                           choices=[
                               ('', 'All Types'),
                               ('multiple_choice', 'Multiple Choice'),
                               ('flashcards', 'Flashcards'),
                               ('practice_test', 'Practice Test'),
                               ('assessment', 'Assessment')
                           ],
                           default='',
                           validators=[Optional()])
    difficulty_level = SelectField('Difficulty',
                                  choices=[
                                      ('', 'All Levels'),
                                      ('easy', 'Easy'),
                                      ('medium', 'Medium'),
                                      ('hard', 'Hard')
                                  ],
                                  default='',
                                  validators=[Optional()])
    submit = SubmitField('Search')


class QuizSettingsForm(FlaskForm):
    
    auto_advance = BooleanField('Auto-advance to next question')
    show_explanations = BooleanField('Show explanations immediately')
    shuffle_questions = BooleanField('Shuffle questions')
    shuffle_options = BooleanField('Shuffle answer options')
    time_warning = IntegerField('Time warning (seconds before time limit)',
                               default=30,
                               validators=[Optional(), NumberRange(min=5, max=300)])
    submit = SubmitField('Save Settings')

