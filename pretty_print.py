from typing import List
from langchain_core.messages import BaseMessage

def     print_langchain_messages(messages: List[BaseMessage], width: int = 80):
    """
    Takes a list of LangChain BaseMessage objects and prints them in a formatted terminal style.
    """
    for msg in messages:
        # LangChain messages have a built-in '.type' attribute (e.g., 'human', 'ai', 'tool')
        msg_type = msg.type 
        
        # 1. Format Human Messages
        if msg_type == "human":
            print(f" Human Message ".center(width, "="))
            print(msg.content)
            
        # 2. Format AI Messages
        elif msg_type == "ai":
            print(f" Ai Message ".center(width, "="))
            if msg.content:
                print(msg.content)
                
            # LangChain's AIMessage stores tool calls in a structured list of dictionaries
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                print("Tool Calls:")
                for tc in msg.tool_calls:
                    name = tc.get("name", "")
                    call_id = tc.get("id", "")
                    args = tc.get("args", {})
                    
                    print(f"  {name} ({call_id})")
                    print(f" Call ID: {call_id}")
                    print("  Args:")
                    for k, v in args.items():
                        print(f"    {k}: {v}")
                        
        # 3. Format Tool Messages
        elif msg_type == "tool":
            print(f" Tool Message ".center(width, "="))
            # ToolMessages typically have a 'name' attribute, though it might occasionally be blank
            name = getattr(msg, "name", "") or "unknown"
            print(f"Name: {name}\n")
            print(msg.content)
            
        # 4. Format System Messages
        elif msg_type == "system":
            print(f" System Message ".center(width, "="))
            print(msg.content)
            
        # 5. Format Generic Chat Messages or custom types
        else:
            # For ChatMessage, the role is defined by the user (e.g., "supervisor", "assistant")
            role_name = getattr(msg, "role", msg_type).title()
            print(f" {role_name} Message ".center(width, "="))
            print(msg.content)