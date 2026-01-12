import os
from dotenv import load_dotenv

load_dotenv()
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
from sqlalchemy import select
from sqlalchemy.orm import Session
from uni.database.connection import get_db
from uni.utils.security import verify_password
from uni.database.connection import get_db, AsyncSessionLocal
from uni.models.users_table import User

from uni.models.students_table import Student
from fastapi import HTTPException, Depends
from uni.logics.students_logics import create
from datetime import datetime, date
from uni.schemas.students import StudentCreate
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
import chainlit as cl
from typing import List, Dict, Optional


gemini_api_key = os.getenv("GEMINI_API_KEY")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client,
)

config = RunConfig(model=model, model_provider=client)


# -------------------- Tools -------------------- #
@function_tool
async def get_my_profile(email: str):
    """Fetch ONLY the profile of the logged-in student using their email."""

    generator = None
    db = None

    try:
        generator = get_db()
        db = await anext(generator)

        stmt = (
            select(Student)
            .join(User, Student.user_id == User.user_id)
            .where(User.email == email)
        )

        result = await db.execute(stmt)
        student = result.scalar_one_or_none()

        if not student:
            return "No record found for this email."

        return {
            "student_id": student.student_id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "father_name": student.father_name,
            "mother_name": student.mother_name,
            "roll_number": student.roll_number,
            "batch_id": student.batch_id,
            "department_id": student.department_id,
            "date_of_birth": str(student.date_of_birth),
            "address": student.address,
            "phone_number": student.phone_number,
            "created_at": str(student.created_at),
            "updated_at": str(student.updated_at),
            "email": student.user.email,
            "user_id": student.user_id,
        }

    except Exception as e:
        return f"Error fetching profile: {str(e)}"

    finally:
        if db:
            await db.close()  # DB band kiya
        if generator:
            await generator.aclose()


@function_tool
async def add_student(
    first_name: str,
    last_name: str,
    father_name: str,
    mother_name: str,
    roll_number: str,
    batch_id: int,
    department_id: int,
    date_of_birth: date,
    address: str,
    phone_number: str,
    email: str,
    password: str,
):
    """Add a new student to the database."""

    try:
        async with AsyncSessionLocal() as db:
            student = StudentCreate(
                first_name=first_name,
                last_name=last_name,
                father_name=father_name,
                mother_name=mother_name,
                roll_number=roll_number,
                batch_id=batch_id,
                department_id=department_id,
                date_of_birth=date_of_birth,
                address=address,
                phone_number=phone_number,
                email=email,
                password=password,
            )

            await create(db, student)

            result_message = f"Student {first_name} {last_name} added successfully."

            return {"status": "success", "detail": result_message}

    except Exception as e:
        return {"status": "error", "detail": str(e)}


@function_tool
async def students_data():
    """Fetch all students from the Neon database with full details."""
    generator = None
    db = None
    try:
        generator = get_db()
        db = await anext(generator)
        data = []
        result = await db.execute(select(Student))
        for s in result.scalars().all():
            data.append(
                {
                    "student_id": s.student_id,
                    "first_name": s.first_name,
                    "last_name": s.last_name,
                    "father_name": s.father_name,
                    "mother_name": s.mother_name,
                    "roll_number": s.roll_number,
                    "batch_id": s.batch_id,
                    "department_id": s.department_id,
                    "date_of_birth": str(s.date_of_birth),
                    "address": s.address,
                    "phone_number": s.phone_number,
                    "created_at": str(s.created_at),
                    "updated_at": str(s.updated_at),
                    "email": s.user.email,
                    "user_id": s.user_id,
                }
            )
        return data

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching students: {str(e)}"
        )
    finally:
        if db:
            await db.close()
        if generator:
            await generator.aclose()


@cl.password_auth_callback
async def auth_callback(username: str, password: str):
    if username == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        return cl.User(
            identifier=username,
            metadata={
                "name": "Super Admin",
                "role": "admin",
                "email": ADMIN_EMAIL,
                "user_id": "admin_100",
            },
        )
    generator = None
    db = None

    try:
        generator = get_db()
        db = await anext(generator)
        result = await db.execute(select(User).where(User.email == username))
        user = result.scalar_one_or_none()

        if user and verify_password(password, user.password):
            return cl.User(
                identifier=user.email,
                metadata={
                    "name": user.user_name,
                    "role": user.user_role,
                    "email": user.email,
                    "user_id": str(user.user_id),
                },
            )
        return None

    except Exception as e:
        print(f"Login Error: {e}")
        return None
    finally:
        if db:
            await db.close()
        if generator:
            await generator.aclose()


final_instructions = ""
tools_list = []


@cl.on_chat_start
async def on_chat_start():
    user = cl.user_session.get("user")
    user_role = user.metadata.get("role", "student")
    user_name = user.metadata.get("name", "User")
    user_email = user.metadata.get("email", user.identifier)

    base_instructions = f"""
    You are a specialized Student Management System Agent talking to {user_name}.
    Current User Role: {user_role.upper()}.
    Your email/identifier is: {user_email}.

    🔴 **CRITICAL SYSTEM RULES (MUST FOLLOW):**
    1. **STRICT SCOPE:** You are NOT a general AI assistant. You are ONLY a database interface.
    2. **OFF-TOPIC REFUSAL:** If the user asks about anything unrelated to Student Records (e.g., weather, coding, general knowledge, jokes, writing emails), you MUST politely refuse.
       - *Example Response:* "I am restricted to Student Management tasks only."
    3. **ROLE ADHERENCE:** Do NOT perform any action that is not explicitly allowed for the role "{user_role.upper()}".
    4. **DATA PRIVACY:** Do NOT share or expose any sensitive data.
    5. RESPONSE FORMAT: Always reply in the same language, tone, and writing style as the user, never use Hindi, always use Roman Urdu unless the user writes pure Urdu (then you may reply in pure Urdu).
    6. ALWAYS think step-by-step before answering.
    7. ALWAYS use the tools provided to you to perform actions. Never assume you can do anything without using the tools.
    8. ALWAYS provide answers in a clear and structured format.
    9. Greet the user warmly using their first name, respond politely to casual conversation, and provide friendly reactions, while restricting all actions to Student Management tasks only.
    10. Display all  data in a clean, structured format with proper labels and line breaks, showing only the logged-in student's information, and respond in a friendly, readable style.
"""

    if user_role == "admin":
        specific_instructions = """
        You are a strict and reliable ADMIN. Follow these rules:
        1. Your responsibilities:
           - Add a student record
           - Show student records (All students allowed)
           - Update/Delete if requested.
        
        2. Before performing ANY action (add, update, delete):
           - Always ask for confirmation from the user.

        3. Collect all student details manually, requiring the user to enter First Name, Last Name, Father's Name, Mother's Name, Roll Number, Batch ID, Department ID, Date of Birth (YYYY-MM-DD), Address, Phone, Email, and Password; validate each field, do not allow adding the record if any field is missing or incorrect, show a clear summary for confirmation before addition, respond politely to greetings or casual chat, maintain role-based access restrictions, and always display the data in a clean, structured, and readable format.

        4. Date of Birth must always be stored in strict YYYY-MM-DD format.
        
        5. Never add a student without full details and explicit confirmation.
        6. Always confirm before deleting or updating  any student record.
        7. When showing student data, present it in a clear, structured format.
        """

        tools_list = [students_data, add_student]

    elif user_role == "student":
        specific_instructions = f"""
        You are a STUDENT. Your access is RESTRICTED.
        
        RULES:
        1. You can ONLY view your OWN student record.
        2. You are STRICTLY PROHIBITED from viewing other students' data.
        3. You CANNOT add, update, or delete any records.
        
        HOW TO SHOW DATA:
        - When fetching student data, you must filter the list.
        - ONLY show the record where the 'email' matches exactly with: "{user_email}".
        - If no record matches your email, say "No record found for your account."
        
        """

        tools_list = [get_my_profile]

    elif user_role == "teacher":
        specific_instructions = """
        You are a TEACHER.
        Currently, you do not have permission to access this system.
        Politely inform the user that Teacher access is coming soon.
        Do NOT run any tools.
        """

        tools_list = []

    else:
        specific_instructions = "You have no access."
        tools_list = []

    final_instructions = base_instructions + "\n" + specific_instructions

    agent = Agent(
        name="Student Management Agent",
        instructions=final_instructions,
        model=model,
        tools=tools_list,
    )
    cl.user_session.set("current_agent", agent)
    cl.user_session.set("history", [])

    await cl.Message(
        content=f"Welcome {user_name}! You are logged in as {user_role.upper()}. How can I help you?"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("history", [])

    history.append({"role": "user", "content": message.content})

    formatted_history = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "assistant"
        formatted_history.append({"role": role, "content": msg["content"]})

    current_agent = cl.user_session.get("current_agent")

    if not current_agent:
        await cl.Message(
            content="⚠️ Error: Agent rules not loaded. Please refresh the page."
        ).send()
        return

    result = Runner.run_streamed(current_agent, formatted_history)

    msg = cl.Message(content="")
    await msg.send()

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            token = event.data.delta

            await msg.stream_token(token)

    await msg.update()

    history.append({"role": "assistant", "content": msg.content})
    cl.user_session.set("history", history)
