import os
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

load_dotenv()

DOWNLOAD_DIR = "./downloads"
PROFILE_DIR = "./topmediai_user_data"
EMAIL = os.getenv("EMAIL_TOP_MEDIA")
PASSWORD = os.getenv("TOP_MEDIA_PASSWORD")


class TopMediaIAgent:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.context = None
        self.page = None

    def start_browser(self):
        # Удаляем SingletonLock, если остался
        lock_file = os.path.join(PROFILE_DIR, "SingletonLock")
        if os.path.exists(lock_file):
            print("⚠️ Найден SingletonLock — удаляем...")
            os.remove(lock_file)

        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            # executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            headless=True,
            # headless=False,#DEBUG
            args=[
                "--window-size=1600,1200",
                "--force-device-scale-factor=1",
                # "--start-maximized",
            ],
            accept_downloads=True
        )
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()

    def is_logged_in(self) -> bool:
        self.page.goto("https://topmediai.com/app/ai-music/", wait_until="domcontentloaded", timeout=60000)
        try:
            # Попробуем найти кнопку Log in. Если нашли — НЕ залогинен.
            self.page.wait_for_selector("button:has-text('Log in')", timeout=5000)
            return False
        except PlaywrightTimeoutError:
            return True

    def login_if_needed(self):
        print("🔍 Проверяем активную сессию...")
        self.start_browser()

        if self.is_logged_in():
            print("✅ Сессия активна, вход не требуется.")
            return
        else:

            print("🔑 Выполняем вход...")
            self.page.goto("https://topmediai.com/app/ai-music/", wait_until="domcontentloaded")

            try:
                try:
                    self.page.wait_for_selector(".cookie-notices-btn.btn-accept", timeout=5000)
                    self.page.click(".cookie-notices-btn.btn-accept")
                except:
                    print("⚠️ Cookie баннер не появился (или уже принят)")
                    # ✅ нажимаем кнопку "Log in"
                self.page.wait_for_timeout(1000)

                # self.page.wait_for_selector("button.unlogin-block", timeout=10000)
                self.page.locator("button.unlogin-block")
                button = self.page.locator("button.unlogin-block")
                print("🟡 Кнопка видна?", button.is_visible())
                print("🟢 Кнопка активна?", button.is_enabled())
                button.scroll_into_view_if_needed()
                button.dispatch_event("click")
                self.page.wait_for_timeout(500)

                # Ждём появления input перед вводом
                self.page.wait_for_selector("input.el-input__inner[type='text']", timeout=10000)
                self.page.wait_for_selector("input.el-input__inner[type='password']", timeout=10000)

                self.page.fill("input.el-input__inner[type='text']", EMAIL)
                self.page.fill("input.el-input__inner[type='password']", PASSWORD)

                self.page.click("button.login-btn:has-text('Login')")

                # Подтверждение входа: исчезновение кнопки Log in или появление "Update Plan"
                self.page.wait_for_selector("span.update-btn", timeout=30000)
                from dotenv import set_key

                for cookie in self.context.cookies():
                    if cookie["name"] == "userToken":
                        token = cookie["value"]
                        print(f"🔐 Найден userToken: {token}")
                        dotenv_path = ".env"
                        set_key(dotenv_path, "TOPMEDIAI_TOKEN", token)
                        os.environ["TOPMEDIAI_TOKEN"] = token
                        break
                else:
                    print("❌ Cookie 'userToken' не найден!")
                print("✅ Вход выполнен и сессия сохранена.")
            except PlaywrightTimeoutError:
                print("❌ Ошибка при логине — возможно, структура изменилась.")
                raise

    def get_music_save(self, title: str) -> str | None:
        print("🎵 Переход к странице AI Music...")
        self.page.goto("https://topmediai.com/app/ai-music/", wait_until="domcontentloaded", timeout=60000)

        try:
            self.page.wait_for_selector("div.text-ellipsis", timeout=10000)
        except PlaywrightTimeoutError:
            print("❌ Не удалось загрузить список треков.")
            return None

        selector = f"div.music-item:has(div.text-ellipsis:has-text('{title}'))"
        cards = self.page.locator(selector)

        if cards.count() == 0:
            print("❌ Карточек не найдено.")
            return None

        cards.nth(0).click()
        print("✅ Клик по карточке")

        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1500)
        self.page.locator("button:has(svg use[href='#icon-musicHome-icon-download'])").click()

        try:
            with self.page.expect_download(timeout=10000) as download_info:
                self.page.locator("p:has-text('Download Original Song')").click()
        except PlaywrightTimeoutError:
            print("❌ Не удалось начать загрузку.")
            return None

        download = download_info.value
        file_name = download.suggested_filename
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        final_path = os.path.join(DOWNLOAD_DIR, file_name)
        download.save_as(final_path)

        print(f"✅ Файл сохранён в: {final_path}")
        return final_path

    def stop(self):
        if self.context:
            self.context.close()
        self.playwright.stop()


if __name__ == "__main__":
    agent = TopMediaIAgent()
    try:
        agent.login_if_needed()
        path = agent.get_music_save("song-cec66f89")
        if path:
            print("✅ Загрузка завершена.")
        else:
            print("❌ Файл не найден или не загружен.")
    finally:
        agent.stop()
