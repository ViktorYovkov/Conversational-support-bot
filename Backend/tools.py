from database import create_ticket

ESCALATE_TOOL = {
    "type": "function",
    "function": {
        "name": "escalate_to_human",
        "description": "Извикай тази функция, когато AI не може да отговори на въпроса"
        ", или когато потребителят поиска да говори с жив оператор.",
        "parameters": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "Уникално ID на сесията на потребителя."
                },
                "reason": {
                    "type": "string",
                    "description": "Кратко описание на проблема или въпроса, който потребителят има, което изисква намесата на жив оператор."
                }
            },
            "required": ["session_id", "reason"]
        }
    }
}

agent_tools = [ESCALATE_TOOL]

def execute_tool(tool_name: str, session_id: str, reason: str):
    if tool_name == "escalate_to_human":
        session = arguments.get("session_id")
        reason = arguments.get("reason")
        create_ticket(session_id, reason)
        return f"Съжалявам, но не мога да отговоря на въпроса ви. Вашият проблем е прехвърлен към жив оператор. Очаквайте скоро отговор."
    else:
        return f"Инструментът ви не е разпознат."