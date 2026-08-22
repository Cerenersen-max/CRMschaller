"""Not: '4-) Telegram Bot: /status, /logs awstail, /scale up, /deploy prod gibi
komutlar ile yonetim. Bot -> Python telegram bot kutuphanesi, K8s API'ye
baglanir.' python-telegram-bot (v21+, async) ile CRM/ops yonetim botu."""
from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from app.bot.k8s_client import K8sClient
from app.config import get_settings
from app.mcp.observability import observability

logger = logging.getLogger("crmschaller.bot")


def _is_authorized(update: Update) -> bool:
    settings = get_settings()
    allowed = settings.telegram_allowed_chat_id_list
    if not allowed:
        # Whitelist tanimli degilse (gelistirme ortami) herkese izin ver.
        return True
    return update.effective_chat is not None and update.effective_chat.id in allowed


async def _guarded_reply(update: Update, text: str) -> None:
    if not _is_authorized(update):
        await update.message.reply_text("Bu botu kullanma yetkiniz yok.")
        return
    await update.message.reply_text(text)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    k8s = context.bot_data["k8s_client"]
    observability.log("bot.status", f"chat={update.effective_chat.id}")
    await _guarded_reply(update, k8s.status())


async def logs_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/logs <deployment> [tail] -- 'awstail' notuna karsilik gelen canli log takibi."""
    k8s = context.bot_data["k8s_client"]
    if not context.args:
        await _guarded_reply(update, "Kullanim: /logs <deployment> [tail_lines]")
        return
    deployment_name = context.args[0]
    tail_lines = int(context.args[1]) if len(context.args) > 1 else 100
    observability.log("bot.logs", f"deployment={deployment_name} tail={tail_lines}")
    await _guarded_reply(update, k8s.logs(deployment_name, tail_lines))


async def scale_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/scale <deployment> <replicas> -- notlardaki '/scale up' komutu."""
    k8s = context.bot_data["k8s_client"]
    if len(context.args) < 2:
        await _guarded_reply(update, "Kullanim: /scale <deployment> <replicas>")
        return
    deployment_name, replicas = context.args[0], int(context.args[1])
    observability.log("bot.scale", f"deployment={deployment_name} replicas={replicas}")
    await _guarded_reply(update, k8s.scale(deployment_name, replicas))


async def deploy_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/deploy <deployment> <image> -- notlardaki '/deploy prod' komutu."""
    k8s = context.bot_data["k8s_client"]
    if len(context.args) < 2:
        await _guarded_reply(update, "Kullanim: /deploy <deployment> <image>")
        return
    deployment_name, image = context.args[0], context.args[1]
    observability.log("bot.deploy", f"deployment={deployment_name} image={image}")
    await _guarded_reply(update, k8s.deploy(deployment_name, image))


def build_application() -> Application:
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN tanimli degil (.env dosyasina bakin)")

    application = Application.builder().token(settings.telegram_bot_token).build()
    application.bot_data["k8s_client"] = K8sClient()

    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("logs", logs_command))
    application.add_handler(CommandHandler("scale", scale_command))
    application.add_handler(CommandHandler("deploy", deploy_command))
    return application


def main() -> None:  # pragma: no cover - calistirma girisi
    logging.basicConfig(level=logging.INFO)
    application = build_application()
    application.run_polling()


if __name__ == "__main__":  # pragma: no cover
    main()
