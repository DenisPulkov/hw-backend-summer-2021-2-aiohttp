from typing import Optional

from aiohttp.web_exceptions import HTTPConflict, HTTPBadRequest, HTTPNotFound

from app.base.base_accessor import BaseAccessor
from app.quiz.models import Theme, Question, Answer


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = Theme(id=self.app.database.next_theme_id, title=str(title))
        self.app.database.themes.append(theme)
        return theme

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        for theme in self.app.database.themes:
            if theme.title == title:
                return theme

    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
        for theme in self.app.database.themes:
            if theme.id == id_:
                return theme

    async def list_themes(self) -> list[Theme]:
        return self.app.database.themes

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        for question in self.app.database.questions:
            if question.title == title:
                return question

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        self.check_question(title, theme_id, answers)
        question = Question(
            id=self.app.database.next_question_id,
            title=title,
            theme_id=theme_id,
            answers=answers,
        )
        self.app.database.questions.append(question)
        return question

    async def list_questions(self, theme_id: Optional[int] = None) -> list[Question]:
        list_q: [Question] = []
        for question in self.app.database.questions:
            if theme_id is None:
                list_q.append(question)
            else:
                if question.theme_id == theme_id:
                    list_q.append(question)
        return list_q

    def check_question(self, title: str, theme_id: int, answers: list[Answer]) -> None:
        correct_answers = [answer.is_correct for answer in answers]
        if sum(correct_answers) != 1:
            raise HTTPBadRequest  # 400
        if len(answers) < 2:
            raise HTTPBadRequest  # 400
        if title in [question.title for question in self.app.database.questions]:
            raise HTTPConflict  # 409
        if theme_id not in [theme.id for theme in self.app.database.themes]:
            raise HTTPNotFound  # 404