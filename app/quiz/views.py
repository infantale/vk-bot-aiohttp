from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound
from aiohttp_apispec import request_schema, response_schema, docs, querystring_schema

from app.quiz.schemes import (
    ThemeSchema, ThemeListSchema, ThemeListResponseSchema, QuestionSchema, QuestionAddResponseSchema,
    ListQuestionResponseSchema, ListQuestionSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.schemes import OkResponseSchema
from app.web.utils import json_response


# TODO: добавить проверку авторизации для этого View
class ThemeAddView(AuthRequiredMixin, View):
    @docs(tags=['quiz'], summary='Theme Add', discription='Add new quiz theme')
    @request_schema(ThemeSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        await super().auth_required()
        title = self.data['title']
        check_theme_exists = await self.store.quizzes.get_theme_by_title(title)
        if check_theme_exists:
            raise HTTPConflict
        else:
            theme = await self.store.quizzes.create_theme(title=title)
            return json_response(data=ThemeSchema().dump(theme))
            # ThemeSchema().dump(theme) == {'title': theme.title, 'id': str(theme.id)}


class ThemeListView(AuthRequiredMixin, View):
    @docs(tags=['quiz'], summary='Theme List', discription='Full list of themes')
    @response_schema(ThemeListResponseSchema, 200)
    async def get(self):
        await super().auth_required()
        themes = await self.store.quizzes.list_themes()
        if themes:
            raw_themes = [ThemeSchema().dump(theme) for theme in themes]
            return json_response(data={'themes': raw_themes})
        else:
            raw_themes = []
            return json_response(data={'themes': raw_themes})


class QuestionAddView(AuthRequiredMixin, View):
    @docs(tags=['quiz'], summary='Question Add', discription='Add new question with answers')
    @request_schema(QuestionSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        await super().auth_required()

        title = self.data['title']
        theme_id = self.data['theme_id']
        answers = self.data['answers']

        theme_in_db = await self.store.quizzes.get_theme_by_id(theme_id)
        title_in_db = await self.store.quizzes.get_question_by_title(title)

        if title_in_db is not None:
            raise HTTPNotFound

        if theme_in_db is None:
            raise HTTPNotFound

        question = await self.store.quizzes.create_question(title=title, theme_id=theme_id, answers=answers)
        # question.id
        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(View):
    @docs(tags=['quiz'], summary='Question List', discription='Question List with theme_id filter')
    @querystring_schema(ListQuestionResponseSchema)
    @response_schema(ListQuestionResponseSchema, 200)
    async def get(self):
        theme_id = self.request.query['theme_id']
        questions = await self.store.quizzes.list_questions(int(theme_id))
        if questions:
            raw_questions = [QuestionSchema().dump(question) for question in questions]
            return json_response(data={'questions': raw_questions})
        else:
            raise HTTPNotFound
