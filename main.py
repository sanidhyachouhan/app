from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

class MCQQuizApp(App):
    def build(self):
        self.num_questions = 0
        self.correct_marks = 0
        self.incorrect_marks = 0
        self.questions = []
        self.correct_answers = []
        self.selected_answers = []
        self.main_layout = BoxLayout(orientation='vertical')
        self.ask_number_of_questions()
        return self.main_layout

    def ask_number_of_questions(self):
        self.main_layout.clear_widgets()

        # Number of questions input
        self.main_layout.add_widget(Label(text="Enter number of questions:"))
        self.num_questions_input = TextInput(multiline=False)
        self.main_layout.add_widget(self.num_questions_input)

        # Marks for correct answers
        self.main_layout.add_widget(Label(text="Enter marks for correct answer:"))
        self.correct_marks_input = TextInput(multiline=False)
        self.main_layout.add_widget(self.correct_marks_input)

        # Marks for incorrect answers
        self.main_layout.add_widget(Label(text="Enter negative marks for incorrect answer:"))
        self.incorrect_marks_input = TextInput(multiline=False)
        self.main_layout.add_widget(self.incorrect_marks_input)

        # Proceed button
        proceed_button = Button(text="Proceed", size_hint=(1, 0.2))
        proceed_button.bind(on_press=self.setup_questions)
        self.main_layout.add_widget(proceed_button)

    def setup_questions(self, instance):
        try:
            self.num_questions = int(self.num_questions_input.text)
            self.correct_marks = int(self.correct_marks_input.text)
            self.incorrect_marks = int(self.incorrect_marks_input.text)
        except ValueError:
            self.main_layout.clear_widgets()
            self.main_layout.add_widget(Label(text="Please enter valid numbers for all inputs!"))
            retry_button = Button(text="Retry", size_hint=(1, 0.2))
            retry_button.bind(on_press=lambda x: self.ask_number_of_questions())
            self.main_layout.add_widget(retry_button)
            return

        self.main_layout.clear_widgets()
        self.show_mcq_screen()

    def show_mcq_screen(self):
        self.main_layout.clear_widgets()
        scrollview = ScrollView()
        content = GridLayout(cols=1, spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # Create MCQs
        for i in range(self.num_questions):
            question_row = GridLayout(cols=6, size_hint_y=None, height=40)

            question_label = Label(text=f"Q{i + 1}", size_hint_x=0.1)
            question_row.add_widget(question_label)

            # Checkboxes for options
            for option in ['A', 'B', 'C', 'D']:
                box = BoxLayout(orientation='horizontal', size_hint_x=0.2)
                checkbox = CheckBox(group=f"question_{i}")
                checkbox.bind(active=self.on_checkbox_active)
                box.add_widget(checkbox)
                box.add_widget(Label(text=option))
                question_row.add_widget(box)

            content.add_widget(question_row)

        scrollview.add_widget(content)
        self.main_layout.add_widget(scrollview)

        submit_button = Button(text="Submit", size_hint=(1, 0.2))
        submit_button.bind(on_press=self.ask_correct_answers)
        self.main_layout.add_widget(submit_button)

    def on_checkbox_active(self, checkbox, value):
        if value:
            question_idx = int(checkbox.group.split('_')[1])
            selected_option = checkbox.parent.children[0].text
            if len(self.selected_answers) <= question_idx:
                self.selected_answers.append(selected_option)
            else:
                self.selected_answers[question_idx] = selected_option

    def ask_correct_answers(self, instance):
        self.main_layout.clear_widgets()
        self.correct_answers = []

        self.main_layout.add_widget(Label(text="Enter correct answers (A, B, C, D):"))
        self.correct_inputs = []

        for i in range(self.num_questions):
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            row.add_widget(Label(text=f"Q{i + 1}:"))
            correct_input = TextInput(multiline=False, hint_text="Correct Answer")
            self.correct_inputs.append(correct_input)
            row.add_widget(correct_input)
            self.main_layout.add_widget(row)

        submit_button = Button(text="Calculate Score", size_hint=(1, 0.2))
        submit_button.bind(on_press=self.calculate_results)
        self.main_layout.add_widget(submit_button)

    def calculate_results(self, instance):
        for correct_input in self.correct_inputs:
            self.correct_answers.append(correct_input.text.strip().upper())

        score = 0
        correct_count = 0
        incorrect_count = 0

        for i, correct_answer in enumerate(self.correct_answers):
            if i < len(self.selected_answers) and self.selected_answers[i] == correct_answer:
                score += self.correct_marks
                correct_count += 1
            else:
                score += self.incorrect_marks
                incorrect_count += 1

        self.show_results(score, correct_count, incorrect_count)

    def show_results(self, score, correct_count, incorrect_count):
        self.main_layout.clear_widgets()
        result_text = f"Correct Answers: {correct_count}\nIncorrect Answers: {incorrect_count}\nTotal Score: {score}"
        self.main_layout.add_widget(Label(text=result_text))

        quit_button = Button(text="Quit", size_hint=(1, 0.2))
        quit_button.bind(on_press=self.stop)
        self.main_layout.add_widget(quit_button)

if __name__ == "__main__":
    MCQQuizApp().run()
