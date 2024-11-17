from tokenize import group

from fastapi import APIRouter, HTTPException

from project.infrastructure.postgres.repository.change_of_groups_repo import ChangeOfGroupsRepository
from project.infrastructure.postgres.repository.group_repo import GroupRepository
from project.infrastructure.postgres.repository.lesson_repo import LessonRepository
from project.infrastructure.postgres.repository.payment_repo import PaymentRepository
from project.infrastructure.postgres.repository.schedule_repo import ScheduleRepository
from project.infrastructure.postgres.repository.stream_repo import StreamRepository
from project.infrastructure.postgres.repository.teacher_repo import TeacherRepository
from project.infrastructure.postgres.repository.teachers_raiting_repo import TeachersRaitingRepository
from project.infrastructure.postgres.repository.user_repo import UserRepository
from project.infrastructure.postgres.repository.course_repo import CourseRepository
from project.infrastructure.postgres.repository.courses_raiting_repo import CoursesRaitingRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.infrastructure.postgres.repository.users_and_groups_repo import UsersAndGroupsRepository
from project.infrastructure.postgres.repository.users_has_schedule_repo import UsersHasScheduleRepository
from project.schemas.change_of_groups import ChangeOfGroupsSchema
from project.schemas.courses_raiting import CoursesRaitingSchema
from project.schemas.group import GroupSchema
from project.schemas.lesson import LessonSchema
from project.schemas.payment import PaymentSchema
from project.schemas.schedule import ScheduleSchema
from project.schemas.stream import StreamSchema
from project.schemas.teacher import TeacherSchema
from project.schemas.teachers_raiting import TeachersRaitingSchema
from project.schemas.user import UserSchema
from project.schemas.course import CourseSchema
from project.schemas.users_and_groups import UsersAndGroupsSchema
from project.schemas.users_has_schedule import UsersHasScheduleSchema

router = APIRouter()
@router.get("/all_users", response_model=list[UserSchema])
async def get_all_users() -> list[UserSchema]:
    user_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        all_users = await user_repo.get_all_users(session=session)

    return all_users

@router.get("/users/{id}", response_model=UserSchema)
async def get_user_by_id(id: int) -> UserSchema:
    user_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        user = await user_repo.get_user_by_id(session=session, id_user=id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/users", response_model=UserSchema)
async def insert_user(user: UserSchema) -> UserSchema:
    user_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        new_user = await user_repo.insert_user(session=session, age=user.age, email=user.email, password=user.password
                                               , first_name=user.first_name, second_name=user.second_name)

    if not new_user:
        raise HTTPException(status_code=500, detail="Failed to insert user")

    return new_user


@router.delete("/users/{id}", response_model=dict)
async def delete_user_by_id(id: int) -> dict:
    user_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        deleted = await user_repo.delete_user_by_id(session=session, id_user=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found or failed to delete")

    return {"message": "User deleted successfully"}


@router.put("/users/{id}", response_model=UserSchema)
async def update_user_by_id(id: int, users: UserSchema) -> UserSchema:
    user_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        updated_user = await user_repo.update_user_by_id(session=session, id_user=id, age=users.age, email=users.email, password=users.password, first_name=users.first_name, second_name=users.second_name)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found or failed to update")

    return updated_user



@router.get("/all_courses", response_model=list[CourseSchema])
async def get_all_courses() -> list[CourseSchema]:
    course_repo = CourseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await course_repo.check_connection(session=session)
        all_courses = await course_repo.get_all_courses(session=session)

    return all_courses

@router.get("/courses/{id}", response_model=CourseSchema)
async def get_course_by_id(id: int) -> CourseSchema:
    course_repo = CourseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await course_repo.check_connection(session=session)
        course = await course_repo.get_course_by_id(session=session, id_course=id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


@router.post("/courses", response_model=CourseSchema)
async def insert_course(course: CourseSchema) -> CourseSchema:
    course_repo = CourseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await course_repo.check_connection(session=session)
        new_course = await course_repo.insert_course(session=session, language=course.language, level=course.level)

    if not new_course:
        raise HTTPException(status_code=500, detail="Failed to insert course")

    return new_course


@router.delete("/courses/{id}", response_model=dict)
async def delete_course_by_id(id: int) -> dict:
    course_repo = CourseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await course_repo.check_connection(session=session)
        deleted = await course_repo.delete_course_by_id(session=session, id_course=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Course not found or failed to delete")

    return {"message": "Course deleted successfully"}


@router.put("/courses/{id}", response_model=CourseSchema)
async def update_course_by_id(id: int, course: CourseSchema) -> CourseSchema:
    course_repo = CourseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await course_repo.check_connection(session=session)
        updated_course = await course_repo.update_course_by_id(session=session, id_course=id, language=course.language,
                                                             level= course.level)

    if not updated_course:
        raise HTTPException(status_code=404, detail="Course not found or failed to update")

    return updated_course


@router.get("/all_groups", response_model=list[GroupSchema])
async def get_all_groups() -> list[GroupSchema]:
    group_repo = GroupRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await group_repo.check_connection(session=session)
        all_groups = await group_repo.get_all_groups(session=session)

    return all_groups

@router.get("/groups/{number}", response_model=GroupSchema)
async def get_group_by_number(number: int) -> GroupSchema:
    group_repo = GroupRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await group_repo.check_connection(session=session)
        group = await group_repo.get_group_by_number(session=session, number_group=number)

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    return group


@router.post("/groups", response_model=GroupSchema)
async def insert_group(group: GroupSchema) -> GroupSchema:
    group_repo = GroupRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await group_repo.check_connection(session=session)
        new_group = await group_repo.insert_group(session=session,number_group=group.group_number,
                                                  course_id=group.course_id)

    if not new_group:
        raise HTTPException(status_code=500, detail="Failed to insert group")

    return new_group


@router.delete("/groups/{number}", response_model=dict)
async def delete_group_by_number(number: int) -> dict:
    group_repo = GroupRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await group_repo.check_connection(session=session)
        deleted = await group_repo.delete_group_by_number(session=session, number_group=number)

    if not deleted:
        raise HTTPException(status_code=404, detail="Group not found or failed to delete")

    return {"message": "Group deleted successfully"}


@router.put("/groups/{number}", response_model=GroupSchema)
async def update_group_by_number(number: int, group: GroupSchema) -> GroupSchema:
    group_repo = GroupRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await group_repo.check_connection(session=session)
        updated_group = await group_repo.update_group_by_number(session=session, number_group=number,
                                                                course_id= group.course_id)

    if not updated_group:
        raise HTTPException(status_code=404, detail="Group not found or failed to update")

    return updated_group



@router.get("/all_teachers", response_model=list[TeacherSchema])
async def get_all_teachers() -> list[TeacherSchema]:
    teacher_repo = TeacherRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await teacher_repo.check_connection(session=session)
        all_teachers = await teacher_repo.get_all_teachers(session=session)

    return all_teachers

@router.get("/teachers/{id}", response_model=TeacherSchema)
async def get_teacher_by_id(id: int) -> TeacherSchema:
    teacher_repo = TeacherRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await teacher_repo.check_connection(session=session)
        teacher = await teacher_repo.get_teacher_by_id(session=session, id_teacher=id)

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return teacher


@router.post("/teachers", response_model=TeacherSchema)
async def insert_teacher(teacher: TeacherSchema) -> TeacherSchema:
    teacher_repo = TeacherRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await teacher_repo.check_connection(session=session)
        new_teacher = await teacher_repo.insert_teacher(session=session, age=teacher.age, experience=teacher.experience
                                                       , first_name=teacher.first_name, second_name=teacher.second_name)

    if not new_teacher:
        raise HTTPException(status_code=500, detail="Failed to insert teacher")

    return new_teacher


@router.delete("/teachers/{id}", response_model=dict)
async def delete_teacher_by_id(id: int) -> dict:
    teacher_repo = TeacherRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await teacher_repo.check_connection(session=session)
        deleted = await teacher_repo.delete_teacher_by_id(session=session, id_teacher=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Teacher not found or failed to delete")

    return {"message": "Teacher deleted successfully"}


@router.put("/teachers/{id}", response_model=TeacherSchema)
async def update_teacher(id: int, teacher: TeacherSchema) -> TeacherSchema:
    teacher_repo = TeacherRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await teacher_repo.check_connection(session=session)
        updated_teacher = await teacher_repo.update_teacher_by_id(session=session, id_teacher=id, age=teacher.age
                                                                 , experience=teacher.experience
                                                                 , first_name=teacher.first_name, second_name=teacher.second_name)

    if not updated_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found or failed to update")

    return updated_teacher



@router.get("/all_payments", response_model=list[PaymentSchema])
async def get_all_payments() -> list[PaymentSchema]:
    payment_repo = PaymentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await payment_repo.check_connection(session=session)
        all_payments = await payment_repo.get_all_payments(session=session)

    return all_payments

@router.get("/payments/{id}", response_model=PaymentSchema)
async def get_payment_by_id(id: int) -> PaymentSchema:
    payment_repo = PaymentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await payment_repo.check_connection(session=session)
        payment = await payment_repo.get_payment_by_id(session=session, id_payment=id)

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return payment


@router.post("/payments", response_model=PaymentSchema)
async def insert_payment(payment: PaymentSchema) -> PaymentSchema:
    payment_repo = PaymentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await payment_repo.check_connection(session=session)
        new_payment = await payment_repo.insert_payment(session=session, user_id=payment.user_id
                                                        , course_id=payment.course_id, pay_date=payment.pay_date)

    if not new_payment:
        raise HTTPException(status_code=500, detail="Failed to insert payment")

    return new_payment


@router.delete("/payments/{id}", response_model=dict)
async def delete_payment_by_id(id: int) -> dict:
    payment_repo = PaymentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await payment_repo.check_connection(session=session)
        deleted = await payment_repo.delete_payment_by_id(session=session, id_payment=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Payment not found or failed to delete")

    return {"message": "Payment deleted successfully"}


@router.put("/payments/{id}", response_model=PaymentSchema)
async def update_payment_by_id(id: int, payment: PaymentSchema) -> PaymentSchema:
    payment_repo = PaymentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await payment_repo.check_connection(session=session)
        updated_payment = await payment_repo.update_payment_by_id(session=session, id_payment=id
                                                                  , user_id=payment.user_id
                                                                  , course_id=payment.course_id
                                                                  , pay_date=payment.pay_date)

    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found or failed to update")

    return updated_payment



@router.get("/all_lessons", response_model=list[LessonSchema])
async def get_all_lessons() -> list[LessonSchema]:
    lesson_repo = LessonRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await lesson_repo.check_connection(session=session)
        all_lessons = await lesson_repo.get_all_lessons(session=session)

    return all_lessons

@router.get("/lessons/{id}", response_model=LessonSchema)
async def get_lesson_by_id(id: int) -> LessonSchema:
    lesson_repo = LessonRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await lesson_repo.check_connection(session=session)
        lesson = await lesson_repo.get_lesson_by_id(session=session, id_lesson=id)

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return lesson


@router.post("/lessons", response_model=LessonSchema)
async def insert_lesson(lesson: LessonSchema) -> LessonSchema:
    lesson_repo = LessonRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await lesson_repo.check_connection(session=session)
        new_lesson = await lesson_repo.insert_lesson(session=session, name=lesson.name, course_id=lesson.course_id)

    if not new_lesson:
        raise HTTPException(status_code=500, detail="Failed to insert lesson")

    return new_lesson


@router.delete("/lessons/{id}", response_model=dict)
async def delete_lesson_by_id(id: int) -> dict:
    lesson_repo = LessonRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await lesson_repo.check_connection(session=session)
        deleted = await lesson_repo.delete_lesson_by_id(session=session, id_lesson=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Lesson not found or failed to delete")

    return {"message": "Lesson deleted successfully"}


@router.put("/lessons/{id}", response_model=LessonSchema)
async def update_lesson(id: int, lesson: LessonSchema) -> LessonSchema:
    lesson_repo = LessonRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await lesson_repo.check_connection(session=session)
        updated_lesson = await lesson_repo.update_lesson_by_id(session=session, id_lesson=id, name=lesson.name
                                                               , course_id=lesson.course_id)

    if not updated_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found or failed to update")

    return updated_lesson



@router.get("/all_changes", response_model=list[ChangeOfGroupsSchema])
async def get_all_changes_of_groups() -> list[ChangeOfGroupsSchema]:
    change_of_groups_repo = ChangeOfGroupsRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await change_of_groups_repo.check_connection(session=session)
        all_changes = await change_of_groups_repo.get_all_changes_of_groups(session=session)

    return all_changes

@router.get("/changes_of_groups/{id}", response_model=ChangeOfGroupsSchema)
async def get_change_of_groups_by_id(id: int) -> ChangeOfGroupsSchema:
    change_of_groups_repo = ChangeOfGroupsRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await change_of_groups_repo.check_connection(session=session)
        change = await change_of_groups_repo.get_change_of_groups_by_id(session=session, id_change=id)

    if not change:
        raise HTTPException(status_code=404, detail="Change not found")

    return change


@router.post("/changes_of_groups", response_model=ChangeOfGroupsSchema)
async def insert_change_of_groups(change: ChangeOfGroupsSchema) -> ChangeOfGroupsSchema:
    change_of_groups_repo = ChangeOfGroupsRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await change_of_groups_repo.check_connection(session=session)
        new_change = await change_of_groups_repo.insert_change_of_groups(session=session, user_id=change.user_id
                                                                         , group_number_before=change.group_number_before
                                                                         , group_number_after=change.group_number_after
                                                                         , date=change.date)

    if not new_change:
        raise HTTPException(status_code=500, detail="Failed to insert change")

    return new_change


@router.delete("/changes_of_groups/{id}", response_model=dict)
async def delete_change_of_groups_by_id(id: int) -> dict:
    change_of_groups_repo = ChangeOfGroupsRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await change_of_groups_repo.check_connection(session=session)
        deleted = await change_of_groups_repo.delete_change_of_groups_by_id(session=session, id_change=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Change not found or failed to delete")

    return {"message": "Change deleted successfully"}


@router.put("/changes_of_groups/{id}", response_model=ChangeOfGroupsSchema)
async def update_change_of_groups_by_id(id: int, change: ChangeOfGroupsSchema) -> ChangeOfGroupsSchema:
    change_of_groups_repo = ChangeOfGroupsRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await change_of_groups_repo.check_connection(session=session)
        updated_change = await change_of_groups_repo.update_change_of_groups_by_id(session=session, id_change=id
                                                                                   , user_id=change.user_id
                                                                                   , group_number_before=change.group_number_before
                                                                                   , group_number_after=change.group_number_after
                                                                                   , date=change.date)

    if not updated_change:
        raise HTTPException(status_code=404, detail="Change not found or failed to update")

    return updated_change


@router.get("/all_schedules", response_model=list[ScheduleSchema])
async def get_all_schedules() -> list[ScheduleSchema]:
    schedule_repo = ScheduleRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await schedule_repo.check_connection(session=session)
        all_schedules = await schedule_repo.get_all_schedules(session=session)

    return all_schedules

@router.get("/schedule/{id}", response_model=ScheduleSchema)
async def get_schedule_by_id(id: int) -> ScheduleSchema:
    schedule_repo = ScheduleRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await schedule_repo.check_connection(session=session)
        schedule = await schedule_repo.get_schedule_by_id(session=session, id_schedule=id)

    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return schedule


@router.post("/schedules", response_model=ScheduleSchema)
async def insert_schedule(schedule: ScheduleSchema) -> ScheduleSchema:
    schedule_repo = ScheduleRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await schedule_repo.check_connection(session=session)
        new_schedule = await schedule_repo.insert_schedule(session=session, teacher_id=schedule.teacher_id
                                                           , group_number=schedule.group_number
                                                           , lesson_id=schedule.lesson_id
                                                           , start_lesson=schedule.start_lesson
                                                           , end_lesson=schedule.end_lesson)

    if not new_schedule:
        raise HTTPException(status_code=500, detail="Failed to insert schedule")

    return new_schedule


@router.delete("/schedules/{id}", response_model=dict)
async def delete_schedule_by_id(id: int) -> dict:
    schedule_repo = ScheduleRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await schedule_repo.check_connection(session=session)
        deleted = await schedule_repo.delete_schedule_by_id(session=session, id_schedule=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Schedule not found or failed to delete")

    return {"message": "Schedule deleted successfully"}


@router.put("/schedules/{id}", response_model=ScheduleSchema)
async def update_schedule_by_id(id: int, schedule: ScheduleSchema) -> ScheduleSchema:
    schedule_repo = ScheduleRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await schedule_repo.check_connection(session=session)
        updated_schedule = await schedule_repo.update_schedule_by_id(session=session, id_schedule=id
                                                                     , teacher_id=schedule.teacher_id
                                                                     , group_number=schedule.group_number
                                                                     , lesson_id=schedule.lesson_id
                                                                     , start_lesson=schedule.start_lesson
                                                                     , end_lesson=schedule.end_lesson)

    if not updated_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found or failed to update")

    return updated_schedule


@router.get("/all_streams", response_model=list[StreamSchema])
async def get_all_streams() -> list[StreamSchema]:
    stream_repo = StreamRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await stream_repo.check_connection(session=session)
        all_streams = await stream_repo.get_all_streams(session=session)

    return all_streams

@router.get("/streams/{number}", response_model=StreamSchema)
async def get_stream_by_number(number: int) -> StreamSchema:
    stream_repo = StreamRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await stream_repo.check_connection(session=session)
        stream = await stream_repo.get_stream_by_number(session=session, number_stream=number)

    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    return stream


@router.post("/streams", response_model=StreamSchema)
async def insert_stream(stream: StreamSchema) -> StreamSchema:
    stream_repo = StreamRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await stream_repo.check_connection(session=session)
        new_stream = await stream_repo.insert_stream(session=session, course_id=stream.course_id)

    if not new_stream:
        raise HTTPException(status_code=500, detail="Failed to insert stream")

    return new_stream


@router.delete("/streams/{number}", response_model=dict)
async def delete_stream_by_number(number: int) -> dict:
    stream_repo = StreamRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await stream_repo.check_connection(session=session)
        deleted = await stream_repo.delete_stream_by_number(session=session, number_stream=number)

    if not deleted:
        raise HTTPException(status_code=404, detail="Stream not found or failed to delete")

    return {"message": "Stream deleted successfully"}


@router.put("/streams/{number}", response_model=StreamSchema)
async def update_stream_by_number(number: int, stream: StreamSchema) -> StreamSchema:
    stream_repo = StreamRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await stream_repo.check_connection(session=session)
        updated_stream = await stream_repo.update_stream_by_number(session=session, number_stream=number
                                                                   , course_id=stream.course_id)

    if not updated_stream:
        raise HTTPException(status_code=404, detail="Stream not found or failed to update")

    return updated_stream



@router.get("/all_courses_raiting", response_model=list[CoursesRaitingSchema])
async def get_all_courses_raiting() -> list[CoursesRaitingSchema]:
    courses_raiting_repo = CoursesRaitingRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await courses_raiting_repo.check_connection(session=session)
        all_courses_raiting = await courses_raiting_repo.get_all_courses_raiting(session=session)

    return all_courses_raiting

@router.get("/courses_raiting/{course_id}", response_model=CoursesRaitingSchema)
async def get_courses_raiting_by_id(id: int) -> CoursesRaitingSchema:
    courses_raiting_repo = CoursesRaitingRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await courses_raiting_repo.check_connection(session=session)
        course_raiting = await courses_raiting_repo.get_courses_raiting_by_id(session=session, course_id=id)

    if not course_raiting:
        raise HTTPException(status_code=404, detail="Course_raiting not found")

    return course_raiting


@router.post("/courses_raiting", response_model=CoursesRaitingSchema)
async def insert_courses_raiting(course: CoursesRaitingSchema) -> CoursesRaitingSchema:
    course_raiting_repo = CoursesRaitingRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await course_raiting_repo.check_connection(session=session)
        new_course_raiting = await course_raiting_repo.insert_courses_raiting(session=session,course_id=course.course_id
                                                                              , raiting=course.raiting
                                                                              , actually_date=course.actually_date)

    if not new_course_raiting:
        raise HTTPException(status_code=500, detail="Failed to insert course_raiting")

    return new_course_raiting


@router.delete("/courses_raiting/{course_id}", response_model=dict)
async def delete_courses_raiting_by_id(id: int) -> dict:
    course_raiting_repo = CoursesRaitingRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await course_raiting_repo.check_connection(session=session)
        deleted = await course_raiting_repo.delete_courses_raiting_by_id(session=session, course_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Course_raiting not found or failed to delete")

    return {"message": "Course_raiting deleted successfully"}


@router.put("/courses_raiting/{course_id}", response_model=CoursesRaitingSchema)
async def update_courses_raiting_by_id(id: int, course: CoursesRaitingSchema) -> CoursesRaitingSchema:
    course_raiting_repo = CoursesRaitingRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await course_raiting_repo.check_connection(session=session)
        updated_course_raiting = await course_raiting_repo.update_courses_raiting_by_id(session=session
                                                                                         ,course_id=id
                                                                                         , raiting=course.raiting
                                                                                         ,actually_date=course.actually_date)

    if not updated_course_raiting:
        raise HTTPException(status_code=404, detail="Course_raiting not found or failed to update")

    return updated_course_raiting



@router.get("/all_teachers_raiting", response_model=list[TeachersRaitingSchema])
async def get_all_teachers_raiting() -> list[TeachersRaitingSchema]:
    teachers_raiting_repo = TeachersRaitingRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await teachers_raiting_repo.check_connection(session=session)
        all_teachers_raiting = await teachers_raiting_repo.get_all_teachers_raiting(session=session)

    return all_teachers_raiting

@router.get("/teachers_raiting/{teacher_id}", response_model=TeachersRaitingSchema)
async def get_teachers_raiting_by_id(id: int) -> TeachersRaitingSchema:
    teachers_raiting_repo = TeachersRaitingRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await teachers_raiting_repo.check_connection(session=session)
        teacher_raiting = await teachers_raiting_repo.get_teachers_raiting_by_id(session=session, teacher_id=id)

    if not teacher_raiting:
        raise HTTPException(status_code=404, detail="Teacher_raiting not found")

    return teacher_raiting


@router.post("/teachers_raiting", response_model=TeachersRaitingSchema)
async def insert_teachers_raiting(teacher: TeachersRaitingSchema) -> TeachersRaitingSchema:
    teacher_raiting_repo = TeachersRaitingRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await teacher_raiting_repo.check_connection(session=session)
        new_teacher_raiting = await teacher_raiting_repo.insert_teachers_raiting(session=session
                                                                                 , teacher_id=teacher.teacher_id
                                                                                 , raiting=teacher.raiting
                                                                                 , actually_date=teacher.actually_date)

    if not new_teacher_raiting:
        raise HTTPException(status_code=500, detail="Failed to insert teacher_raiting")

    return new_teacher_raiting


@router.delete("/teachers_raiting/{teacher_id}", response_model=dict)
async def delete_teachers_raiting_by_id(id: int) -> dict:
    teacher_raiting_repo = TeachersRaitingRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await teacher_raiting_repo.check_connection(session=session)
        deleted = await teacher_raiting_repo.delete_teachers_raiting_by_id(session=session, teacher_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Teacher_raiting not found or failed to delete")

    return {"message": "Teacher_raiting deleted successfully"}


@router.put("/teachers_raiting/{teacher_id}", response_model=TeachersRaitingSchema)
async def update_teachers_raiting_by_id(id: int, teacher: TeachersRaitingSchema) -> TeachersRaitingSchema:
    teacher_raiting_repo = TeachersRaitingRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await teacher_raiting_repo.check_connection(session=session)
        updated_teacher_raiting = await teacher_raiting_repo.update_teachers_raiting_by_id(session=session
                                                                                         ,teacher_id=id
                                                                                         , raiting=teacher.raiting
                                                                                         ,actually_date=teacher.actually_date)

    if not updated_teacher_raiting:
        raise HTTPException(status_code=404, detail="Teacher_raiting not found or failed to update")

    return updated_teacher_raiting


@router.get("/all_users_and_groups", response_model=list[UsersAndGroupsSchema])
async def get_all_users_and_groups() -> list[UsersAndGroupsSchema]:
    users_and_groups_repo = UsersAndGroupsRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await users_and_groups_repo.check_connection(session=session)
        all_users_and_groups = await users_and_groups_repo.get_all_users_and_groups(session=session)

    return all_users_and_groups

@router.get("/users_and_groups/{user_id}", response_model=UsersAndGroupsSchema)
async def get_users_and_groups_by_id(id: int) -> UsersAndGroupsSchema:
    users_and_groups_repo = UsersAndGroupsRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await users_and_groups_repo.check_connection(session=session)
        users_and_groups = await users_and_groups_repo.get_users_and_groups_by_id(session=session, user_id=id)

    if not users_and_groups:
        raise HTTPException(status_code=404, detail="User in group not found")

    return users_and_groups


@router.post("/users_and_groups", response_model=UsersAndGroupsSchema)
async def insert_users_and_groups(user: UsersAndGroupsSchema) -> UsersAndGroupsSchema:
    users_and_groups_repo = UsersAndGroupsRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await users_and_groups_repo.check_connection(session=session)
        new_users_and_groups = await users_and_groups_repo.insert_users_and_groups(session=session
                                                                                   , user_id=user.user_id
                                                                                   , group_number=user.group_number
                                                                                   , stream_number=user.stream_number)

    if not new_users_and_groups:
        raise HTTPException(status_code=500, detail="Failed to insert user in group")

    return new_users_and_groups


@router.delete("/users_and_groups/{user_id}", response_model=dict)
async def delete_user_and_groups_by_id(id: int) -> dict:
    users_and_groups_repo = UsersAndGroupsRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await users_and_groups_repo.check_connection(session=session)
        deleted = await users_and_groups_repo.delete_users_and_groups_by_id(session=session, user_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User in group not found or failed to delete")

    return {"message": "User in group deleted successfully"}


@router.put("/users_and_groups/{user_id}", response_model=UsersAndGroupsSchema)
async def update_users_and_groups_by_id(id: int, user: UsersAndGroupsSchema) -> UsersAndGroupsSchema:
    users_and_groups_repo = UsersAndGroupsRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await users_and_groups_repo.check_connection(session=session)
        updated_users_and_groups = await users_and_groups_repo.update_users_and_groups_by_id(session=session
                                                                                             ,user_id=id
                                                                                             , group_number=user.group_number
                                                                                             ,stream_number=user.stream_number)

    if not updated_users_and_groups:
        raise HTTPException(status_code=404, detail="User in group not found or failed to update")

    return updated_users_and_groups



@router.get("/all_users_has_schedule", response_model=list[UsersHasScheduleSchema])
async def get_all_users_has_schedule() -> list[UsersHasScheduleSchema]:
    users_has_schedule_repo = UsersHasScheduleRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await users_has_schedule_repo.check_connection(session=session)
        all_users_has_schedule = await users_has_schedule_repo.get_all_users_has_schedule(session=session)

    return all_users_has_schedule

@router.get("/user_has_schedule/{user_id}", response_model=UsersHasScheduleSchema)
async def get_users_has_schedule_by_id(id: int) -> UsersHasScheduleSchema:
    users_has_schedule_repo = UsersHasScheduleRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await users_has_schedule_repo.check_connection(session=session)
        users_has_schedule = await users_has_schedule_repo.get_user_has_schedule_by_id(session=session, user_id=id)

    if not users_has_schedule:
        raise HTTPException(status_code=404, detail="User has schedule not found")

    return users_has_schedule


@router.post("/user_has_schedule", response_model=UsersHasScheduleSchema)
async def insert_user_has_schedule(user: UsersHasScheduleSchema) -> UsersHasScheduleSchema:
    users_has_schedule_repo = UsersHasScheduleRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await users_has_schedule_repo.check_connection(session=session)
        new_user_has_schedule = await users_has_schedule_repo.insert_user_has_schedule(session=session
                                                                                      , user_id=user.user_id
                                                                                      , schedule_id=user.schedule_id
                                                                                      , attendance=user.attendance
                                                                                      , mark=user.mark)

    if not new_user_has_schedule:
        raise HTTPException(status_code=500, detail="Failed to insert user has schedule")

    return new_user_has_schedule


@router.delete("/user_has_schedule/{user_id}", response_model=dict)
async def delete_user_has_schedule_by_id(id: int) -> dict:
    users_has_schedule_repo = UsersHasScheduleRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await users_has_schedule_repo.check_connection(session=session)
        deleted = await users_has_schedule_repo.delete_user_has_schedule_by_id(session=session, user_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User has schedule not found or failed to delete")

    return {"message": "User has schedule deleted successfully"}


@router.put("/user_has_schedule/{user_id}", response_model=UsersHasScheduleSchema)
async def update_user_has_schedule_by_id(id: int, user: UsersHasScheduleSchema) -> UsersHasScheduleSchema:
    users_has_schedule_repo = UsersHasScheduleRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await users_has_schedule_repo.check_connection(session=session)
        updated_users_has_schedule = await users_has_schedule_repo.update_user_has_schedule_by_id(session=session
                                                                                                 , user_id=user.user_id
                                                                                                 , schedule_id=user.schedule_id
                                                                                                 , attendance=user.attendance
                                                                                                 , mark=user.mark)

    if not updated_users_has_schedule:
        raise HTTPException(status_code=404, detail="User has schedule not found or failed to update")

    return updated_users_has_schedule