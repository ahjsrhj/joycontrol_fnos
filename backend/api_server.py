#!/usr/bin/env python3
"""
FastAPI server for JoyControl web interface
"""
import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Optional, List

from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import joycontrol.logging_default as log
from joycontrol.controller import Controller
from joycontrol.controller_state import ControllerState, button_push, button_press, button_release
from joycontrol.memory import FlashMemory
from joycontrol.protocol import controller_protocol_factory
from joycontrol.server import create_hid_server
from joycontrol.nfc_tag import NFCTag
from joycontrol.device import HidDevice

logger = logging.getLogger(__name__)

app = FastAPI(title="JoyControl API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
controller_state: Optional[ControllerState] = None
transport = None
protocol = None
connection_task: Optional[asyncio.Task] = None
is_connected = False
is_pairing = False
paired_switch_address: Optional[str] = None
CONFIG_FILE = Path.home() / ".joycontrol_config.json"
# 优先使用环境变量指定的目录，否则使用 /amiibo（Docker 环境）或 ~/amiibo（本地环境）
AMIIBO_DIR = Path(os.getenv("AMIIBO_DIR", "/amiibo"))


# Pydantic models
class ButtonPressRequest(BaseModel):
    buttons: List[str]


class ButtonReleaseRequest(BaseModel):
    buttons: List[str]


class StickRequest(BaseModel):
    stick: str  # 'l' or 'r'
    x: int  # -32768 to 32767
    y: int  # -32768 to 32767


class PairRequest(BaseModel):
    reconnect: bool = False


def load_config():
    """加载配置"""
    global paired_switch_address
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                paired_switch_address = config.get('paired_switch_address')
                return config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
    return {}


def save_config():
    """保存配置"""
    try:
        config = {
            'paired_switch_address': paired_switch_address
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except Exception as e:
        logger.error(f"Error saving config: {e}")


def check_paired():
    """检查是否已配对"""
    try:
        hid = HidDevice()
        switches = hid.get_paired_switches()
        if switches:
            global paired_switch_address
            if not paired_switch_address:
                # 从已配对的设备中获取地址
                paired_switch_address = hid.get_address_of_paired_path(switches[0])
                save_config()
            return True
        return False
    except Exception as e:
        logger.error(f"Error checking paired status: {e}")
        return False


async def connect_controller(reconnect: bool = False):
    """连接控制器"""
    global controller_state, transport, protocol, is_connected, is_pairing
    
    if is_pairing or is_connected:
        return
    
    is_pairing = True
    
    try:
        controller = Controller.PRO_CONTROLLER
        spi_flash = FlashMemory()
        
        reconnect_addr = None
        if reconnect and paired_switch_address:
            reconnect_addr = paired_switch_address
        elif reconnect:
            reconnect_addr = 'auto'
        
        factory = controller_protocol_factory(controller, spi_flash=spi_flash, reconnect=reconnect_addr)
        ctl_psm, itr_psm = 17, 19
        
        transport, protocol = await create_hid_server(
            factory,
            reconnect_bt_addr=reconnect_addr,
            ctl_psm=ctl_psm,
            itr_psm=itr_psm,
            capture_file=None,
            device_id=None,
            interactive=False
        )
        
        controller_state = protocol.get_controller_state()
        
        # 等待连接完成
        await controller_state.connect()
        
        is_connected = True
        logger.info("Controller connected successfully")
        
    except Exception as e:
        logger.error(f"Error connecting controller: {e}")
        raise
    finally:
        is_pairing = False


async def disconnect_controller():
    """断开控制器连接"""
    global controller_state, transport, protocol, is_connected
    
    try:
        if transport:
            await transport.close()
        controller_state = None
        transport = None
        protocol = None
        is_connected = False
        logger.info("Controller disconnected")
    except Exception as e:
        logger.error(f"Error disconnecting controller: {e}")


@app.on_event("startup")
async def startup():
    """启动时加载配置"""
    load_config()
    log.configure(console_level=logging.INFO)


@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok"}


@app.get("/api/status")
async def get_status():
    """获取状态"""
    paired = check_paired()
    return {
        "paired": paired,
        "connected": is_connected,
        "pairing": is_pairing,
        "paired_switch_address": paired_switch_address
    }


@app.post("/api/pair")
async def pair(request: PairRequest, background_tasks: BackgroundTasks):
    """配对或连接"""
    global paired_switch_address
    
    if is_pairing:
        raise HTTPException(status_code=400, detail="Already pairing")
    
    if is_connected and not request.reconnect:
        raise HTTPException(status_code=400, detail="Already connected")
    
    try:
        if request.reconnect:
            # 重新连接
            if not paired_switch_address:
                raise HTTPException(status_code=400, detail="No paired switch found")
            await disconnect_controller()
            background_tasks.add_task(connect_controller, reconnect=True)
        else:
            # 新配对
            await disconnect_controller()
            background_tasks.add_task(connect_controller, reconnect=False)
            
            # 保存配对信息
            if not paired_switch_address:
                try:
                    hid = HidDevice()
                    switches = hid.get_paired_switches()
                    if switches:
                        paired_switch_address = hid.get_address_of_paired_path(switches[0])
                        save_config()
                except Exception:
                    pass
        
        return {"success": True, "message": "Pairing started"}
    except Exception as e:
        logger.error(f"Error in pair: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/connect")
async def connect(background_tasks: BackgroundTasks):
    """连接已配对的设备"""
    if not check_paired():
        raise HTTPException(status_code=400, detail="No paired switch found")
    
    if is_connected:
        return {"success": True, "message": "Already connected"}
    
    if is_pairing:
        raise HTTPException(status_code=400, detail="Already pairing")
    
    try:
        background_tasks.add_task(connect_controller, reconnect=True)
        return {"success": True, "message": "Connecting..."}
    except Exception as e:
        logger.error(f"Error in connect: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/disconnect")
async def disconnect():
    """断开连接"""
    await disconnect_controller()
    return {"success": True, "message": "Disconnected"}


@app.post("/api/button/press")
async def press_button(request: ButtonPressRequest):
    """按下按钮"""
    logger.info(f"Received press button request: buttons={request.buttons}")
    if not is_connected or not controller_state:
        raise HTTPException(status_code=400, detail="Controller not connected")
    
    try:
        # 确保控制器已连接（参考 run_controller_cli.py）
        await controller_state.connect()
        await button_press(controller_state, *request.buttons)
        return {"success": True}
    except Exception as e:
        logger.error(f"Error pressing button: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/button/release")
async def release_button(request: ButtonReleaseRequest):
    """释放按钮"""
    logger.info(f"Received release button request: buttons={request.buttons}")
    if not is_connected or not controller_state:
        raise HTTPException(status_code=400, detail="Controller not connected")
    
    try:
        # 确保控制器已连接（参考 run_controller_cli.py）
        await controller_state.connect()
        await button_release(controller_state, *request.buttons)
        return {"success": True}
    except Exception as e:
        logger.error(f"Error releasing button: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/button/click")
async def click_button(request: ButtonPressRequest):
    """点击按钮（按下后立即释放）"""
    if not is_connected or not controller_state:
        raise HTTPException(status_code=400, detail="Controller not connected")
    
    try:
        await button_push(controller_state, *request.buttons)
        return {"success": True}
    except Exception as e:
        logger.error(f"Error clicking button: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/stick")
async def set_stick(request: StickRequest):
    """设置摇杆位置"""
    if not is_connected or not controller_state:
        raise HTTPException(status_code=400, detail="Controller not connected")
    
    try:
        if request.stick == 'l':
            if not controller_state.l_stick_state:
                raise HTTPException(status_code=400, detail="Left stick not available")
            controller_state.l_stick_state.set_center()
            controller_state.l_stick_state.set_x(request.x)
            controller_state.l_stick_state.set_y(request.y)
        elif request.stick == 'r':
            if not controller_state.r_stick_state:
                raise HTTPException(status_code=400, detail="Right stick not available")
            controller_state.r_stick_state.set_center()
            controller_state.r_stick_state.set_x(request.x)
            controller_state.r_stick_state.set_y(request.y)
        else:
            raise HTTPException(status_code=400, detail="Invalid stick, use 'l' or 'r'")
        
        await controller_state.send()
        return {"success": True}
    except Exception as e:
        logger.error(f"Error setting stick: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/nfc/files")
async def list_nfc_files():
    """列出 amiibo 文件"""
    amiibo_files = []
    
    if not AMIIBO_DIR.exists():
        return {"files": []}
    
    try:
        # 递归查找所有 .bin 文件
        for bin_file in AMIIBO_DIR.rglob("*.bin"):
            relative_path = bin_file.relative_to(AMIIBO_DIR)
            amiibo_files.append({
                "path": str(bin_file),
                "name": bin_file.name,
                "relative_path": str(relative_path),
                "size": bin_file.stat().st_size
            })
        
        # 按路径排序
        amiibo_files.sort(key=lambda x: x["relative_path"])
        
        return {"files": amiibo_files}
    except Exception as e:
        logger.error(f"Error listing NFC files: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/nfc/load")
async def load_nfc(file_path: str = Query(..., description="Path to the amiibo file")):
    """加载 NFC/Amiibo"""
    if not is_connected or not controller_state:
        raise HTTPException(status_code=400, detail="Controller not connected")
    
    if controller_state.get_controller() == Controller.JOYCON_L:
        raise HTTPException(status_code=400, detail="NFC not available for JOYCON_L")
    
    try:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        nfc_tag = NFCTag.load_amiibo(file_path)
        controller_state.set_nfc(nfc_tag)
        logger.info(f"Loaded NFC: {file_path}")
        return {"success": True, "message": f"Loaded NFC: {os.path.basename(file_path)}"}
    except Exception as e:
        logger.error(f"Error loading NFC: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/nfc/remove")
async def remove_nfc():
    """移除 NFC"""
    if not is_connected or not controller_state:
        raise HTTPException(status_code=400, detail="Controller not connected")
    
    try:
        controller_state.set_nfc(None)
        logger.info("Removed NFC")
        return {"success": True, "message": "NFC removed"}
    except Exception as e:
        logger.error(f"Error removing NFC: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/nfc/status")
async def get_nfc_status():
    """获取 NFC 状态"""
    if not is_connected or not controller_state:
        return {"loaded": False}
    
    nfc = controller_state.get_nfc()
    return {
        "loaded": nfc is not None,
        "source": nfc.source if nfc else None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=13821)

