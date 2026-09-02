import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from vector_db import search_faq
from database import get_chat_history, create_ticket
from tools import agent_tools, execute_tool

load_dotenv()

client = OpenAI(api_key=os.getenv("OpenAI_API_KEY"))

def generate_response(session_id: str, user_input: str) -> str:
    chat_history = get_chat_history(session_id, limit=10)
    search_query = user_input

    if chat_history and len(user_input.split()) <= 2:
        last_bot_message = chat_history[-1]["content"]
        search_query = f"{last_bot_message} {user_input}"
    
    rag_context = search_faq(search_query, n_results=3)

    system_prompt = (
        "Ти се казваш Eliza и си мил AI асистент, който помага на потребителите да решат техните проблеми."
        "Предоставяш точни и полезни отговори на въпросите им."
        "Помагаш им да научат повече за фирмата и нейната дейност."
        "АБСОЛЮТНО ЗАБРАНЕНО: Строго ти е забранено да отговаряш на въпроси извън контекста на Sirma.\n "
        "Дори и да знаеш отговора, НИКОГА не използвай външни знания. Отговаряй САМО въз основа на предоставения контекст.\n"
        "Ако потребителят поиска контакт на фирмата, кажи му, че може да се обърне към екипа на Sirma и му предостави имейла: customer_support@sirma.com\n"
        "Ако смяташ, че въпросът е извън твоята компетеност, признай си и пренасочи към имейл за връзка с фирмата\n"
        "Когато прецениш, че е необходимо, можеш да подкрепиш отговора си с кейс стъди\n"
        "Важно е винаги да отговаряш на потребителите на езика, на който са задали въпроса си!"
        "Следвай контекста и отговаряй на езика, на който е зададен ПОСЛЕДНИЯ въпрос\n\n"
    )

    if rag_context:
        system_prompt += (
            "Имаме следната информация от нашата база данни, която може да ти помогне да отговориш на въпроса:\n"
            f"{rag_context}\n\n"
        )
    
    if not rag_context:
        system_prompt += (
            "Ако не успееш да намериш отговор в нашата база данни, не си измисляй информация."
            "Вместо това се извини учтиво, обясни, че не можеш да отговаряш на въпроси извън услугите на Sirma\n\n"
        )
    
    messages = [
        {"role": "system", "content": system_prompt},]
    
    messages.extend(chat_history)

    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3,
            max_tokens=1000,
            tools=agent_tools
        )
    
        response_message = response.choices[0].message
    
        if response_message.tool_calls:
            tool_call = response_message.tool_calls[0]
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            tool_response = execute_tool(tool_name, session_id, reason)
            return tool_response

        return response_message.content

    except Exception as e:
        print(f"Грешка при генериране на отговор: {e}")
        return "Съжалявам, възникна грешка при обработката на вашия въпрос. Моля, опитайте отново по-късно."
    
if __name__ == "__main__":
    test_session_id = "test_session_123"
    test_user_input = "Поддържате ли cloud/hybrid deployment?"
    response = generate_response(test_session_id, test_user_input)
    print(f"Отговор на AI: {response}")