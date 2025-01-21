
# app.py
import os
import logging
from quart import Quart
from dotenv import load_dotenv

load_dotenv()

# Базовая конфигурация логгера
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

from controllers.telegram_controller import telegram_bp
from controllers.umnico_controller import umnico_bp
from controllers.widget_controller import widget_bp
from controllers.admin_controller import admin_bp
from controllers.db_controller import db_bp
from controllers.tester_controller import tester_bp

# Инициализируем LLM Manager
from core.llm_manager import LLMManager

def create_app():
    app = Quart(__name__)

    LLMManager.init_all_llms()

    app.register_blueprint(telegram_bp, url_prefix="/api/v1/telegram")
    app.register_blueprint(umnico_bp, url_prefix="/api/v1/umnico")
    app.register_blueprint(widget_bp, url_prefix="/api/v1/widget")
    app.register_blueprint(admin_bp, url_prefix="/api/v1/admin")
    app.register_blueprint(db_bp, url_prefix="/api/v1/db/mongodb")
    app.register_blueprint(tester_bp, url_prefix="/api/v1/tester")

    return app

if __name__ == "__main__":
    quart_app = create_app()
    quart_app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8010)))