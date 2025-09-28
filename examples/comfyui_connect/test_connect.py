import asyncio
import websockets
import json
import uuid
from urllib.parse import urlparse

# ComfyUI的HTTP基础地址（确保能正常访问）
COMFYUI_BASE_URL = "http://home.chrissong.top:3818/"

client_id = str(uuid.uuid4())
async def test_comfyui_ws():
    # 1. 生成正确的WebSocket地址（关键：替换http为ws，添加/ws路径）
    parsed_url = urlparse(COMFYUI_BASE_URL)
    ws_scheme = "wss" if parsed_url.scheme == "https" else "ws"
    ws_url = f"{ws_scheme}://{parsed_url.netloc}/ws?clientId={client_id}"
    print(f"尝试连接WebSocket: {ws_url}")

    try:
        # 2. 连接WebSocket（使用标准库，自动处理握手头）
        async with websockets.connect(
            ws_url,
            # 显式指定 Origin 头（解决部分跨域场景）
            extra_headers={"Origin": COMFYUI_BASE_URL},
        ) as websocket:
            print("✅ WebSocket连接成功！")

            # 3. 发送测试消息（验证通信）
            test_msg = {"type": "ping"}  # ComfyUI支持的ping类型消息
            await websocket.send(json.dumps(test_msg))
            print(f"发送测试消息: {test_msg}")

            # 4. 接收响应
            response = await websocket.recv()
            print(f"收到响应: {json.loads(response)}")

    except websockets.exceptions.InvalidStatusCode as e:
        # 捕获400错误并显示详细信息
        print(f"❌ 握手失败，状态码: {e.status_code}")
        print("可能原因：")
        if e.status_code == 400:
            print("- 路径错误（必须是/ws）")
            print("- 协议不匹配（http→ws，https→wss）")
            print("- 跨域限制未解除")
    except Exception as e:
        print(f"❌ 连接错误: {str(e)}")


if __name__ == "__main__":
    # 启动前请确保：
    # 1. ComfyUI已启动，且HTTP可访问（如http://localhost:8188）
    # 2. 启动参数已添加跨域允许：python main.py --cors-allow-origins "*"
    asyncio.run(test_comfyui_ws())
