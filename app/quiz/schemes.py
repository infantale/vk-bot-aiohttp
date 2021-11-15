from marshmallow import Schema, fields, validates, ValidationError, post_load

from app.web.schemes import OkResponseSchema


class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Boolean(required=True)


class QuestionSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested(AnswerSchema, many=True)

    # @post_load
    # def check_items(self, item, **kwargs):
    #     correct_answer = 0
    #
    #     if len(item['answers']) <= 1:
    #         return HTTPUnprocessableEntity
    #
    #     for answer in item['answers']:
    #         if answer['is_correct'] == True:
    #             correct_answer += 1
    #
    #     if correct_answer != 1:
    #         return HTTPUnprocessableEntity
    #
    #     return self.handle_error()

    # @validates('answers')
    # def validate_one_correct(self, *args):
    #     print(self.answers, *args)
    #     accessor = QuizAccessor()
    #     exist_id = QuizAccessor.get_theme_by_id(id_=value)
    #     print(exist_id)
    #     if exist_id != value:
    #         raise ValidationError("Theme ID must be exist")


class ThemeListSchema(Schema):
    themes = fields.Nested(ThemeSchema, many=True)


class QuestionAddResponseSchema(OkResponseSchema):
    question = fields.Nested(QuestionSchema)


class ThemeListResponseSchema(OkResponseSchema):
    themes = fields.Nested(ThemeListSchema)


class ThemeIdSchema(Schema):
    pass


class ListQuestionSchema(Schema):
    questions = fields.Nested(QuestionSchema, many=True)


class ListQuestionResponseSchema(Schema):
    questions = fields.Nested(ListQuestionSchema)
