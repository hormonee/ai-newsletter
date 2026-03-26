import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class SmtpEmailAdapter:
    def __init__(self, sender, password):
        self.sender = sender
        self.password = password
        self.logger = logging.getLogger(__name__)

    def send_report(self, receiver_list, content):
        """다중 수신자에게 BCC 방식으로 메일을 발송 (개별 수신인 표시 효과)"""
        now = datetime.now()
        subject = f"{now.month}월 {now.day}일 AI & 대한민국 트렌드 리포트"

        msg = MIMEMultipart()
        msg['From'] = self.sender
        # 수신인 목록 보호를 위해 To를 발신자(본인)로 표시
        msg['To'] = self.sender
        msg['Subject'] = subject
        # HTML 형식으로 본문 첨부
        msg.attach(MIMEText(content, 'html'))

        self.logger.info(f"📬 {len(receiver_list)}명에게 뉴스 리포트 발송을 시작합니다... (BCC 적용)")

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender, self.password)
                # BCC 발송을 위해 sendmail 사용 (수신자 목록을 직접 전달)
                server.sendmail(self.sender, receiver_list, msg.as_string())
            self.logger.info(f"✅ 총 {len(receiver_list)}명에게 메일 발송 성공!")
        except Exception as e:
            self.logger.error(f"❌ 메일 발송 중 오류 발생: {e}")
            raise e
