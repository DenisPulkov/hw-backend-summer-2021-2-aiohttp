from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest
from aiohttp_apispec import request_schema, response_schema, querystring_schema

from app.quiz.models import Answer
from app.quiz.schemes import (
    ThemeSchema, ThemeListSchema, QuestionSchema, ThemeIdSchema, ListQuestionSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


# TODO: добавить проверку авторизации для этого View
class ThemeAddView(AuthRequiredMixin, View):
    # TODO: добавить валидацию с помощью aiohttp-apispec и marshmallow-схем
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        title = self.data["title"]  # TODO: заменить на self.data["title"] после внедрения валидации
        # TODO: проверять, что не существует     темы с таким же именем, отдавать 409 если существует
        check_theme = await self.store.quizzes.get_theme_by_title(title=title)
        if not check_theme:
            theme = await self.store.quizzes.create_theme(title=title)
            return json_response(data=ThemeSchema().dump(theme))
        raise HTTPConflict


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListSchema)
    async def get(self):
        themes = await self.request.app.store.quizzes.list_themes()
        raw_themes = [ThemeSchema().dump(obj=theme) for theme in themes]
        return json_response(data={"themes": raw_themes})


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema, 200)
    async def post(self):
        title = self.data["title"]
        existing_title = await self.store.quizzes.get_question_by_title(title=title)
        if existing_title:
            raise HTTPConflict
        theme_id = self.data["theme_id"]
        theme = await self.store.quizzes.get_theme_by_id(id_=theme_id)
        if not theme:
            raise HTTPConflict
        answers = [Answer(title=answer["title"], is_correct=answer["is_correct"]) for answer in self.data["answers"]]
        correct_answer = [answer.is_correct for answer in answers]
        if sum(correct_answer) != 1:
            raise HTTPBadRequest
        if len(answers) < 2:
            raise HTTPBadRequest
        question = await self.store.quizzes.create_question(
            title=title,
            theme_id=theme_id,
            answers=answers,
        )
        return json_response(data=QuestionSchema().dump(question))
'''
        question = await self.request.json()
        if not await self.store.quizzes.get_question_by_title(question["title"]):
            if await self.store.quizzes.get_theme_by_id(question["theme_id"]):
                if len(question["answers"]) > 1:
                    check: int = 0
                    for ans in question["answers"]:
                        if ans["is_correct"]:
                            check += 1
                    if check == 1:
                        question = await self.store.quizzes.create_question(title=question["title"],
                                                                            theme_id=question["theme_id"],
                                                                            answers=question["answers"])
                        return json_response(data=QuestionSchema().dump(question))
                    else:
                        raise HTTPBadRequest
                else:
                    raise HTTPBadRequest
            else:
                raise HTTPConflict
        else:
            raise HTTPConflict
'''

class QuestionListView(AuthRequiredMixin, View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        list_theme_id = int(self.request.query["theme_id"])
        list_questions = await self.store.quizzes.list_questions(list_theme_id)
        raw_questions = [QuestionSchema().dump(obj=questions) for questions in list_questions]
        return json_response(data={"questions": raw_questions})
