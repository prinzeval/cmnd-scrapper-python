from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
import uvicorn
import os
from dotenv import load_dotenv
from tools import tools

# Load environment variables
load_dotenv()

app = FastAPI()

@app.get("/cmnd-tools")
def cmnd_tools_endpoint():
    tools_response = [
        {
            "name": tool["name"],
            "description": tool["description"],
            "jsonSchema": tool["parameters"],
            "isDangerous": tool.get("isDangerous", False),
            "functionType": tool["functionType"],
            "isLongRunningTool": tool.get("isLongRunningTool", False),
            "preCallPrompt": tool.get("preCallPrompt"),
            "postCallPrompt": tool.get("postCallPrompt"),
            "rerun": tool["rerun"],
            "rerunWithDifferentParameters": tool["rerunWithDifferentParameters"],
        } for tool in tools
    ]
    return JSONResponse(content={"tools": tools_response})

@app.post("/run-cmnd-tool")
async def run_cmnd_tool_endpoint(request: Request):
    data = await request.json()
    tool_name = data.get('toolName')
    props = data.get('props', {})
    memory = data.get('memory')
    print(f"once arrived {memory}")
    
    tool = next((t for t in tools if t['name'] == tool_name), None)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    try:
        conversation_id = props["conversationId"]
        chatbot_conversation_id = props["chatbotConversationId"]
        del props["conversationId"] 
        del props["chatbotConversationId"] 
        print(f"before passing {type(memory)}")
        result = await tool["runCmd"](**props, memory=memory)
        print(f"memory value came from cmnd-server: {memory}")
        print(f"after passing {type(memory)}")
        print(f"content: {result}")
        return JSONResponse(content=result, media_type="application/json")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)