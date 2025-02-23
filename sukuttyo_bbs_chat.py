import os
import sys
import time
import threading
import uuid

class SukuttyoBBS:
    def __init__(self, username):
        self.username = username if username else 'O'
        self.session_id = str(uuid.uuid4())
        self.readme_file = 'README.md'
        self.running = True

    def send_message(self, message):
        """メッセージをREADMEに送信"""
        try:
            # READMEの現在の内容を読み込み
            try:
                with open(self.readme_file, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
            except FileNotFoundError:
                existing_content = "# SUKUTTYO@BBS チャットログ\n\n"

            # 新しいメッセージを追加
            log_message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {self.username}> {message}\n\n"
            
            # READMEを更新
            with open(self.readme_file, 'w', encoding='utf-8') as f:
                f.write(existing_content + log_message)
            
            # 標準出力に直接表示
            print(log_message.strip(), flush=True)
        except Exception as e:
            print(f"メッセージ送信エラー: {e}", flush=True)

    def start_chat(self, initial_message=None):
        """チャットセッションの開始"""
        # 開始メッセージ
        self.send_message("SUKUTTYOセッションを開始します")
        
        # 初期メッセージがある場合は送信
        if initial_message:
            self.send_message(initial_message)

        # 6時間の制限
        start_time = time.time()
        max_duration = 6 * 60 * 60  # 6時間

        print(f"SUKUTTYO@BBS - {self.username}としてログイン", flush=True)
        print("メッセージを入力 (exitで終了)", flush=True)

        while time.time() - start_time < max_duration:
            try:
                # 標準入力から読み取り
                message = input(f"{self.username}> ")
                
                if message.lower() in ['exit', 'quit']:
                    self.send_message("セッションを終了します")
                    break
                
                if message:
                    self.send_message(message)
            
            except EOFError:
                # GitHub Actionsでの入力制限に対応
                break
            except KeyboardInterrupt:
                break

        # 終了処理
        self.send_message("セッションを終了します")
        self.running = False

def main():
    username = os.environ.get('USERNAME', 'O')
    initial_message = os.environ.get('INITIAL_MESSAGE', None)
    
    bbs = SukuttyoBBS(username)
    bbs.start_chat(initial_message)

if __name__ == "__main__":
    main()
